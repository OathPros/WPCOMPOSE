from __future__ import annotations

from fastapi import APIRouter, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.renderers.gutenberg_renderer import GutenbergRenderer
from app.schemas.blueprint import PageType
from app.services.blueprint_service import BlueprintService
from app.services.extraction_service import ExtractionService
from app.services.ingestion_service import IngestionService
from app.validators.validation_service import ValidationService

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

ingestion_service = IngestionService(ExtractionService())
blueprint_service = BlueprintService()
renderer = GutenbergRenderer()
validation_service = ValidationService()


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "page_types": [pt.value for pt in PageType],
            "result": None,
            "error": None,
        },
    )


@router.post("/compose", response_class=HTMLResponse)
async def compose(
    request: Request,
    raw_text: str = Form(default=""),
    page_type: PageType = Form(...),
    audience: str = Form(default=""),
    tone: str = Form(default=""),
    files: list[UploadFile] | None = File(default=None),
):
    try:
        valid_files: list[UploadFile] = []

        for file in files or []:
            if file is None:
                continue
            if file.filename is None:
                continue
            if file.filename.strip() == "":
                continue

            valid_files.append(file)

        ingested = await ingestion_service.ingest(raw_text, valid_files)

        blueprint = blueprint_service.generate_blueprint(
            page_type=page_type,
            normalized_content=ingested["normalized_content"],
            audience=audience or None,
            tone=tone or None,
        )

        blueprint_errors = validation_service.validate_blueprint(blueprint)
        markup = renderer.render_page(blueprint)
        markup_errors = validation_service.validate_rendered_markup(markup)

        result = {
            "summary": f"Generated {blueprint.page_type.value} blueprint with {len(blueprint.sections)} sections.",
            "outline": [f"{sec.heading} ({sec.module_type.value})" for sec in blueprint.sections],
            "editor_notes": blueprint.editor_notes,
            "markup": markup,
            "blueprint": blueprint.model_dump_json(indent=2),
            "validation_errors": blueprint_errors + markup_errors,
            "sources": ingested["sources"],
        }

        return templates.TemplateResponse(
            "index.html",
            {"request": request, "page_types": [pt.value for pt in PageType], "result": result, "error": None},
        )
    except Exception as exc:  # noqa: BLE001
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "page_types": [pt.value for pt in PageType], "result": None, "error": str(exc)},
        )
