import json
import re
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

    assert '<!-- wp:group {"tagName":"section"' not in markup
    assert "<!-- wp:html -->" in markup
    assert '<section id="hero" class="york-hero-banner">' in markup
    assert "<h2>Technology at York</h2>" in markup
    assert "Spring update" in markup
    assert '<section id="details" class="york-standard-content">' in markup
    assert "<h2>Details</h2>" in markup
    assert "Networks and labs are being refreshed." in markup
    assert "york-lead" in markup
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



def test_renderer_outputs_valid_related_links_and_on_page_nav_markup():
    blueprint = PageBlueprint.model_validate(
        {
            "page_type": "uit_service_page",
            "title": "Test",
            "intro": "Intro",
            "sections": [
                {
                    "section_id": "on-this-page",
                    "module_type": "on_this_page_nav",
                    "heading": "On this page",
                    "content": {"anchors": ["overview", "#service-details"]},
                },
                {
                    "section_id": "related-services",
                    "module_type": "related_links",
                    "heading": "Related Services",
                    "content": {
                        "links": [
                            {"title": "Service A", "url": "https://example.edu/a"},
                            {"title": "Service B", "url": "https://example.edu/b"},
                        ]
                    },
                },
            ],
            "cta": {"label": "Contact", "url": "https://example.edu/contact"},
        }
    )

    renderer = GutenbergRenderer()
    markup = renderer.render_page(blueprint)

    assert '<section id="related-services" class="york-related-links">' in markup
    assert "<!-- wp:group" not in markup
    assert "<!-- wp:list {\"className\":\"york-related-links\"} -->" not in markup
    assert "<!-- wp:html -->" in markup
    assert "<h2>Related Services</h2>" in markup
    assert "<ul>" in markup
    assert "<a href=\"#overview\">Overview</a>" in markup
    assert "<a href=\"#service-details\">Service Details</a>" in markup
    assert 'href="overview"' not in markup



def test_renderer_avoids_empty_custom_sections_and_uses_html_callout_wrapper():
    blueprint = PageBlueprint.model_validate(
        {
            "page_type": "uit_service_page",
            "title": "Test",
            "intro": "Intro",
            "sections": [
                {
                    "section_id": "callout-1",
                    "module_type": "callout_band",
                    "heading": "Important Notice",
                    "content": {"text": "Docker is not automatically approved for production hosting."},
                }
            ],
            "cta": {"label": "Contact", "url": "https://example.edu/contact"},
        }
    )

    renderer = GutenbergRenderer()
    markup = renderer.render_page(blueprint)

    assert '<section id="callout-1" class="york-callout-band">' in markup
    assert "<!-- wp:quote" not in markup
    assert "<!-- wp:html -->" in markup
    assert "Important Notice" in markup
    assert "Docker is not automatically approved for production hosting." in markup
    assert re.search(r"<section\\b[^>]*>\\s*</section>", markup) is None
