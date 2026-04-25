from __future__ import annotations

import copy
import json
import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

from app.rules.page_rules import PAGE_RULES
from app.schemas.blueprint import PageBlueprint, PageType

load_dotenv()


def make_openai_schema_strict(schema: dict[str, Any]) -> dict[str, Any]:
    """
    Convert Pydantic's JSON schema into the stricter/smaller JSON Schema subset
    accepted by OpenAI structured outputs.

    Fixes:
    - every object must include additionalProperties: false
    - every object with properties must list all properties in required
    - oneOf is not permitted, so convert oneOf to anyOf
    """
    strict_schema = copy.deepcopy(schema)

    def walk(node: Any) -> None:
        if not isinstance(node, dict):
            return

        # OpenAI structured outputs do not allow oneOf in this context.
        # Convert it to anyOf, which is accepted more broadly.
        if "oneOf" in node:
            one_of_value = node.pop("oneOf")
            existing_any_of = node.get("anyOf")

            if isinstance(existing_any_of, list):
                node["anyOf"] = existing_any_of + one_of_value
            else:
                node["anyOf"] = one_of_value

        if node.get("type") == "object":
            properties = node.get("properties")

            node["additionalProperties"] = False

            if isinstance(properties, dict):
                node["required"] = list(properties.keys())

                for property_schema in properties.values():
                    walk(property_schema)

        items = node.get("items")
        if isinstance(items, dict):
            walk(items)

        for key in ("$defs", "definitions"):
            definitions = node.get(key)
            if isinstance(definitions, dict):
                for definition_schema in definitions.values():
                    walk(definition_schema)

        for key in ("anyOf", "allOf"):
            variants = node.get(key)
            if isinstance(variants, list):
                for variant_schema in variants:
                    walk(variant_schema)

    walk(strict_schema)
    return strict_schema


class BlueprintService:
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def _build_prompt(
        self,
        page_type: PageType,
        content: str,
        audience: str | None,
        tone: str | None,
    ) -> str:
        rules = PAGE_RULES[page_type]

        return (
            f"You are generating a structured York webpage blueprint for {page_type.value}.\n"
            f"Allowed modules: {[module.value for module in rules['allowed_modules']]}.\n"
            f"Required modules: {[module.value for module in rules['required_sections']]}.\n"
            f"Module guidance: {rules.get('module_guidance', 'Use modules conservatively and intentionally.')}.\n"
            f"Default tone: {rules['default_tone']}.\n"
            f"Audience: {audience or 'general York audience'}.\n"
            f"Tone override: {tone or 'none'}.\n\n"
            "Instructions:\n"
            "- Return JSON only.\n"
            "- Match the supplied schema exactly.\n"
            "- Do not include markdown.\n"
            "- Do not include commentary outside the JSON.\n"
            "- Do not invent facts, URLs, dates, contacts, service details, or claims.\n"
            "- Use only the source content provided.\n"
            "- If required information is missing, add a clear editor note.\n"
            "- Prefer concise, polished York web copy.\n\n"
            f"Source content:\n{content}"
        )

    def generate_blueprint(
        self,
        page_type: PageType,
        normalized_content: str,
        audience: str | None,
        tone: str | None,
    ) -> PageBlueprint:
        if not self.client:
            raise RuntimeError("OPENAI_API_KEY is not configured")

        prompt = self._build_prompt(
            page_type=page_type,
            content=normalized_content,
            audience=audience,
            tone=tone,
        )

        schema = make_openai_schema_strict(PageBlueprint.model_json_schema())

        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "page_blueprint",
                    "schema": schema,
                    "strict": True,
                }
            },
        )

        raw_output = response.output_text

        try:
            data = json.loads(raw_output)
        except json.JSONDecodeError as exc:
            raise ValueError(f"OpenAI returned invalid JSON: {raw_output}") from exc

        return PageBlueprint.model_validate(data)
