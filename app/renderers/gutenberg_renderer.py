from __future__ import annotations

from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.schemas.blueprint import PageBlueprint


class GutenbergRenderer:
    def __init__(self, template_dir: str = "app/templates") -> None:
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(default=False),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def render_section(self, section) -> str:
        template = self.env.get_template(f"modules/{section.module_type.value}.jinja")
        return template.render(section=section)

    def render_page(self, blueprint: PageBlueprint) -> str:
        header = self.env.get_template("page_wrapper.jinja").render(title=blueprint.title)
        rendered_sections = [self.render_section(section) for section in blueprint.sections]
        return "\n".join([header, *rendered_sections]).strip()
