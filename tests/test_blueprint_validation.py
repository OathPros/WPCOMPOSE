import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from app.schemas.blueprint import PageBlueprint
from app.validators.validation_service import ValidationService


def load_fixture(name: str) -> PageBlueprint:
    data = json.loads(Path(f"tests/fixtures/blueprints/{name}.json").read_text())
    return PageBlueprint.model_validate(data)


def test_blueprint_schema_validation():
    bp = load_fixture("cio_article")
    assert bp.title == "York Technology Update"
    assert len(bp.sections) >= 3


def test_anchor_validation():
    bp = load_fixture("uit_service_page")
    errors = ValidationService().validate_blueprint(bp)
    assert not errors

    bp.sections[1].content.anchors = ["#not-real"]
    errors = ValidationService().validate_blueprint(bp)
    assert any("does not match" in e for e in errors)


def test_page_type_rules_enforced():
    bp = load_fixture("initiative_page")
    bp.sections = [s for s in bp.sections if s.module_type.value != "cta_block"]
    errors = ValidationService().validate_blueprint(bp)
    assert any("Required module missing: cta_block" in e for e in errors)


def test_kadence_tabs_validation_rules():
    bp = load_fixture("uit_service_page_kadence")
    tabs_section = next(section for section in bp.sections if section.module_type.value == "kadence_tabs")

    tabs_section.content.tabs[1].title = " What   support includes "
    tabs_section.content.tabs[2].heading = ""
    tabs_section.content.tabs[2].body = ""

    errors = ValidationService().validate_blueprint(bp)

    assert any("must be unique after normalization" in e for e in errors)
    assert any("must include heading or body" in e for e in errors)


def test_kadence_accordion_validation_rules():
    bp = load_fixture("uit_service_page_kadence")
    accordion_section = next(section for section in bp.sections if section.module_type.value == "kadence_accordion")

    accordion_section.content.items.append(accordion_section.content.items[0].model_copy(deep=True))
    accordion_section.content.items[0].body = ""
    accordion_section.content.items[1].title = "  can uit build my docker image?  "

    errors = ValidationService().validate_blueprint(bp)

    assert any("body cannot be empty" in e for e in errors)
    assert any("must be unique after normalization" in e for e in errors)


def test_kadence_raw_html_fields_are_rejected():
    fixture = json.loads(Path("tests/fixtures/blueprints/uit_service_page_kadence.json").read_text())
    tabs_section = next(section for section in fixture["sections"] if section["module_type"] == "kadence_tabs")
    tabs_section["content"]["tabs"][0]["html"] = "<div>unsupported</div>"

    with pytest.raises(ValidationError):
        PageBlueprint.model_validate(fixture)
