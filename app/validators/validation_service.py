from __future__ import annotations

from app.rules.page_rules import PAGE_RULES
from app.schemas.blueprint import ModuleType, PageBlueprint


class ValidationService:
    def validate_blueprint(self, blueprint: PageBlueprint) -> list[str]:
        errors: list[str] = []

        if not blueprint.title.strip():
            errors.append("Exactly one H1 title is required.")

        rules = PAGE_RULES[blueprint.page_type]
        allowed = set(rules["allowed_modules"])
        present = [section.module_type for section in blueprint.sections]

        for module in present:
            if module not in allowed:
                errors.append(f"Module {module.value} is not allowed for {blueprint.page_type.value}.")

        for required in rules["required_sections"]:
            if required not in present:
                errors.append(f"Required module missing: {required.value}.")

        section_ids = {s.section_id for s in blueprint.sections}
        for section in blueprint.sections:
            if not section.heading.strip():
                errors.append(f"Heading is empty for section {section.section_id}.")

            if section.module_type == ModuleType.THREE_CARD_GRID:
                cards = section.content.cards
                if len(cards) > 3:
                    errors.append("three_card_grid supports a maximum of 3 cards.")
                for card in cards:
                    if not card.title.strip() or not card.body.strip():
                        errors.append("three_card_grid card titles and bodies cannot be empty.")

            if section.module_type == ModuleType.ON_THIS_PAGE_NAV:
                for anchor in section.content.anchors:
                    anchor_id = anchor.lstrip("#")
                    if anchor_id not in section_ids:
                        errors.append(f"on_this_page_nav anchor '{anchor}' does not match any section_id.")

        has_placeholder = "TODO" in blueprint.intro or any("TODO" in note for note in blueprint.editor_notes)
        if has_placeholder and not blueprint.editor_notes:
            errors.append("Editor notes must surface missing content or placeholders.")

        return errors

    def validate_rendered_markup(self, markup: str) -> list[str]:
        errors: list[str] = []
        if "<!-- wp:" not in markup:
            errors.append("Rendered output is missing Gutenberg block markers.")
        if "<h1" not in markup:
            errors.append("Rendered output must include one H1.")
        return errors
