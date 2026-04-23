import json
from pathlib import Path

from app.renderers.gutenberg_renderer import GutenbergRenderer
from app.schemas.blueprint import PageBlueprint


def test_renderer_outputs_hero_lead_standard_modules():
    data = json.loads(Path("tests/fixtures/blueprints/cio_article.json").read_text())
    blueprint = PageBlueprint.model_validate(data)

    renderer = GutenbergRenderer()
    markup = renderer.render_page(blueprint)

    assert "york-hero-banner" in markup
    assert "york-lead" in markup
    assert "york-standard-content" in markup
    assert "<!-- wp:" in markup
