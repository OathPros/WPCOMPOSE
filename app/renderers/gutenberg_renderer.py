from __future__ import annotations

import re

from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.schemas.blueprint import ModuleType, PageBlueprint

MODULE_TEMPLATE_MAP = {
    ModuleType.HERO_BANNER: "modules/hero_banner.jinja",
    ModuleType.LEAD_PARAGRAPH: "modules/lead_paragraph.jinja",
    ModuleType.ON_THIS_PAGE_NAV: "modules/on_this_page_nav.jinja",
    ModuleType.STANDARD_CONTENT_SECTION: "modules/standard_content_section.jinja",
    ModuleType.TWO_COLUMN_SECTION: "modules/two_column_section.jinja",
    ModuleType.THREE_CARD_GRID: "modules/three_card_grid.jinja",
    ModuleType.CALLOUT_BAND: "modules/callout_band.jinja",
    ModuleType.FAQ_ACCORDION: "modules/faq_accordion.jinja",
    ModuleType.KADENCE_TABS: "modules/kadence_tabs.jinja",
    ModuleType.KADENCE_ACCORDION: "modules/kadence_accordion.jinja",
    ModuleType.CTA_BLOCK: "modules/cta_block.jinja",
    ModuleType.RELATED_LINKS: "modules/related_links.jinja",
}


def _to_anchor(value: str) -> str:
    lowered = value.lower().strip()
    normalized = lowered.replace("&", " and ")
    collapsed = re.sub(r"\s+", "-", normalized)
    stripped = re.sub(r"[^a-z0-9\-_]", "", collapsed)
    return stripped.strip("-") or "tab"


class GutenbergRenderer:
    def __init__(self, template_dir: str = "app/templates") -> None:
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(default=False),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.env.filters["to_anchor"] = _to_anchor

    def render_section(self, section) -> str:
        template_path = MODULE_TEMPLATE_MAP.get(section.module_type, f"modules/{section.module_type.value}.jinja")
        template = self.env.get_template(template_path)
        return template.render(section=section)

    def render_page(self, blueprint: PageBlueprint) -> str:
        header = self.env.get_template("page_wrapper.jinja").render(title=blueprint.title)
        rendered_sections = [self.render_section(section) for section in blueprint.sections]
        return "\n".join([header, *rendered_sections]).strip()
