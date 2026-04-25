import json
from pathlib import Path

from app.renderers.gutenberg_renderer import GutenbergRenderer
from app.schemas.blueprint import PageBlueprint


def load_blueprint(name: str) -> PageBlueprint:
    data = json.loads(Path(f"tests/fixtures/blueprints/{name}.json").read_text())
    return PageBlueprint.model_validate(data)


def test_renderer_outputs_hero_lead_standard_modules():
    blueprint = load_blueprint("cio_article")

    renderer = GutenbergRenderer()
    markup = renderer.render_page(blueprint)

    assert "york-hero-banner" in markup
    assert "york-lead" in markup
    assert "york-standard-content" in markup
    assert "<!-- wp:" in markup


def test_renderer_outputs_kadence_tabs_and_accordion_modules():
    blueprint = load_blueprint("uit_service_page_kadence")

    renderer = GutenbergRenderer()
    markup = renderer.render_page(blueprint)

    assert "<!-- wp:kadence/tabs" in markup
    assert "<!-- wp:kadence/tab" in markup
    assert "wp-block-kadence-tabs" in markup
    assert "kt-tabs-title-list" in markup
    assert "kt-tabs-content-wrap" in markup
    assert "What support includes" in markup
    assert "What is out of scope" in markup
    assert "Before you request support" in markup

    assert "<!-- wp:kadence/accordion" in markup
    assert "<!-- wp:kadence/pane" in markup
    assert "wp-block-kadence-accordion" in markup
    assert "kt-accordion-wrap" in markup
    assert "kt-accordion-inner-wrap" in markup
    assert "Can UIT build my Docker image?" in markup
    assert "Can I use Docker for production hosting?" in markup
