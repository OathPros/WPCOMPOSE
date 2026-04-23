from __future__ import annotations

import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from app.rules.page_rules import PAGE_RULES
from app.schemas.blueprint import PageBlueprint, PageType

load_dotenv()


class BlueprintService:
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def _build_prompt(self, page_type: PageType, content: str, audience: str | None, tone: str | None) -> str:
        rules = PAGE_RULES[page_type]
        return (
            f"You are generating a structured York webpage blueprint for {page_type.value}. "
            f"Allowed modules: {[m.value for m in rules['allowed_modules']]}. "
            f"Required modules: {[m.value for m in rules['required_sections']]}. "
            f"Default tone: {rules['default_tone']}.\n"
            f"Audience: {audience or 'general York audience'}.\n"
            f"Tone override: {tone or 'none'}.\n"
            "Return valid JSON matching the schema only."
            f"\n\nSource content:\n{content}"
        )

    def generate_blueprint(self, page_type: PageType, normalized_content: str, audience: str | None, tone: str | None) -> PageBlueprint:
        if not self.client:
            raise RuntimeError("OPENAI_API_KEY is not configured")

        prompt = self._build_prompt(page_type, normalized_content, audience, tone)

        response = self.client.responses.create(
            model=self.model,
            input=[{"role": "user", "content": prompt}],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "page_blueprint",
                    "schema": PageBlueprint.model_json_schema(),
                    "strict": True,
                }
            },
        )

        raw = response.output_text
        data = json.loads(raw)
        return PageBlueprint.model_validate(data)
