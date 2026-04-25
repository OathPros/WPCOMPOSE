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

    assert "<!-- wp:group {\"tagName\":\"section\"" in markup
    assert "class=\"wp-block-group york-hero-banner\"" in markup
    assert "york-lead" in markup
    assert "class=\"wp-block-group york-standard-content\"" in markup
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


def test_renderer_outputs_core_spacer_sizes():
    blueprint = PageBlueprint.model_validate(
        {
            "page_type": "cio_article",
            "title": "Spacing Test",
            "intro": "Intro",
            "sections": [
                {
                    "section_id": "spacer-small",
                    "module_type": "core_spacer",
                    "heading": "Spacer",
                    "content": {"size": "small"},
                },
                {
                    "section_id": "spacer-medium",
                    "module_type": "core_spacer",
                    "heading": "Spacer",
                    "content": {"size": "medium"},
                },
                {
                    "section_id": "spacer-large",
                    "module_type": "core_spacer",
                    "heading": "Spacer",
                    "content": {"size": "large"},
                },
            ],
            "cta": {"label": "Read", "url": "https://example.edu"},
        }
    )

    renderer = GutenbergRenderer()
    markup = renderer.render_page(blueprint)

    assert "<!-- wp:spacer {\"height\":\"25px\"} -->" in markup
    assert "<div style=\"height:25px\" aria-hidden=\"true\" class=\"wp-block-spacer\"></div>" in markup
    assert "<!-- wp:spacer {\"height\":\"50px\"} -->" in markup
    assert "<div style=\"height:50px\" aria-hidden=\"true\" class=\"wp-block-spacer\"></div>" in markup
    assert "<!-- wp:spacer -->" in markup
    assert "<div style=\"height:100px\" aria-hidden=\"true\" class=\"wp-block-spacer\"></div>" in markup
    assert "spacer small" not in markup.lower()
    assert "spacer medium" not in markup.lower()
    assert "spacer large" not in markup.lower()


def test_renderer_outputs_spacers_with_kadence_modules():
    blueprint = load_blueprint("uit_service_page_with_spacers")

    renderer = GutenbergRenderer()
    markup = renderer.render_page(blueprint)

    assert "<!-- wp:spacer {\"height\":\"50px\"} -->" in markup
    assert "<div style=\"height:50px\" aria-hidden=\"true\" class=\"wp-block-spacer\"></div>" in markup
    assert "<!-- wp:spacer -->" in markup
    assert "<div style=\"height:100px\" aria-hidden=\"true\" class=\"wp-block-spacer\"></div>" in markup
    assert "<!-- wp:kadence/tabs" in markup
    assert "<!-- wp:kadence/accordion" in markup


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

    assert "<!-- wp:group {\"tagName\":\"section\",\"anchor\":\"related-services\",\"className\":\"york-related-links\"} -->" in markup
    assert "<!-- wp:list {\"className\":\"york-related-links\"} -->" not in markup
    assert "<!-- wp:list -->" in markup
    assert "<a href=\"#overview\">Overview</a>" in markup
    assert "<a href=\"#service-details\">Service Details</a>" in markup
    assert 'href="overview"' not in markup
