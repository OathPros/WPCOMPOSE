from __future__ import annotations

import re

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

            if section.module_type == ModuleType.KADENCE_TABS:
                tabs = section.content.tabs
                if len(tabs) < 2:
                    errors.append("kadence_tabs must include at least 2 tabs.")
                if len(tabs) > 6:
                    errors.append("kadence_tabs supports a maximum of 6 tabs.")

                seen_titles: set[str] = set()
                for idx, tab in enumerate(tabs, start=1):
                    title = tab.title.strip()
                    heading = (tab.heading or "").strip()
                    body = (tab.body or "").strip()

                    if not title:
                        errors.append(f"kadence_tabs tab {idx} title cannot be empty.")
                    normalized_title = self._normalize_label(title)
                    if normalized_title in seen_titles:
                        errors.append("kadence_tabs tab titles must be unique after normalization.")
                    seen_titles.add(normalized_title)

                    if not heading and not body:
                        errors.append(f"kadence_tabs tab {idx} must include heading or body.")

            if section.module_type == ModuleType.KADENCE_ACCORDION:
                items = section.content.items
                if len(items) < 1:
                    errors.append("kadence_accordion must include at least 1 item.")
                if len(items) > 8:
                    errors.append("kadence_accordion supports a maximum of 8 items.")

                seen_titles: set[str] = set()
                for idx, item in enumerate(items, start=1):
                    title = item.title.strip()
                    body = item.body.strip()

                    if not title:
                        errors.append(f"kadence_accordion item {idx} title cannot be empty.")
                    if not body:
                        errors.append(f"kadence_accordion item {idx} body cannot be empty.")

                    normalized_title = self._normalize_label(title)
                    if normalized_title in seen_titles:
                        errors.append("kadence_accordion item titles must be unique after normalization.")
                    seen_titles.add(normalized_title)

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

    @staticmethod
    def _normalize_label(value: str) -> str:
        lowered = value.lower().strip()
        collapsed = re.sub(r"\s+", " ", lowered)
        return re.sub(r"[^a-z0-9]", "", collapsed)
