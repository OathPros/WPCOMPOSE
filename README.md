# York AI Web Composer (MVP)

York AI Web Composer is a local prototype for York web editors to transform source material into structured, copy-pastable Gutenberg markup through a controlled pipeline:

`Raw content -> structured page blueprint -> module renderer -> validation -> Gutenberg output`

## Features

- FastAPI backend and minimal server-rendered frontend
- Ingestion supports pasted text + multiple uploads (`.pdf`, `.docx`, `.txt`, `.md`)
- Extraction via PyMuPDF and python-docx
- OpenAI Responses API blueprint generation with structured JSON schema
- Deterministic Gutenberg rendering via Jinja2 templates (no direct freeform markup generation)
- Rules engine for page-type/module eligibility
- Validation for anchors, required modules, cards, headings, and basic markup checks
- Tests for extraction, schema validation, rendering, anchors, and rules enforcement

## Supported page types

1. `cio_article`
2. `initiative_page`
3. `uit_service_page`

## Supported modules (MVP)

- `hero_banner`
- `lead_paragraph`
- `on_this_page_nav`
- `standard_content_section`
- `two_column_section`
- `three_card_grid`
- `callout_band`
- `faq_accordion`
- `cta_block`
- `related_links`

## Project structure

```text
app/
  main.py
  routes/
  services/
  schemas/
  rules/
  renderers/
  templates/
  validators/
  static/
tests/
```

## Setup

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Set `OPENAI_API_KEY` in `.env`.

## Run locally

```bash
uvicorn app.main:app --reload
```

Open: http://127.0.0.1:8000

## Usage

1. Paste text and/or upload files.
2. Choose page type.
3. Optionally set audience and tone.
4. Click **Generate**.
5. Review:
   - Summary
   - Outline
   - Editor Notes
   - Final Markup (copy button)

## Key design notes

- OpenAI calls are isolated in `app/services/blueprint_service.py`.
- Rendering is deterministic and template-driven in `app/renderers/gutenberg_renderer.py` + `app/templates/modules/`.
- Rules and validation are deterministic Python logic (`app/rules/`, `app/validators/`).
- Where exact York markup is unknown, placeholder Gutenberg-compatible patterns are isolated in templates with easy replacement points.

## Tests

```bash
pytest
```

## Fixtures

- Blueprint fixtures by page type:
  - `tests/fixtures/blueprints/cio_article.json`
  - `tests/fixtures/blueprints/initiative_page.json`
  - `tests/fixtures/blueprints/uit_service_page.json`
- Example rendered markup:
  - `tests/fixtures/outputs/sample_markup.txt`
- Example input files:
  - `tests/fixtures/inputs/sample.txt`
  - `tests/fixtures/inputs/sample.md`

## API implementation note

This MVP uses the OpenAI **Responses API** with structured JSON schema output for blueprint generation.

## Future enhancements (post-MVP)

- Add auth and role-based access
- Add richer editor QA checks
- Add persistence
- Expand module templates and page-type constraints
