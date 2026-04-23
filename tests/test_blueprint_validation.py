import json
from pathlib import Path

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
