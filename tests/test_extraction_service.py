from pathlib import Path

import docx
import fitz

from app.services.extraction_service import ExtractionService


def test_extract_txt_file():
    service = ExtractionService()
    data = Path("tests/fixtures/inputs/sample.txt").read_bytes()
    result = service.extract_text("sample.txt", data)
    assert "York AI Web Composer" in result["text"]


def test_extract_pdf_file(tmp_path):
    service = ExtractionService()
    pdf_path = tmp_path / "sample.pdf"
    with fitz.open() as pdf:
        page = pdf.new_page()
        page.insert_text((72, 72), "PDF content for York")
        pdf.save(pdf_path)

    result = service.extract_text("sample.pdf", pdf_path.read_bytes())
    assert "PDF content for York" in result["text"]


def test_extract_docx_file(tmp_path):
    service = ExtractionService()
    docx_path = tmp_path / "sample.docx"
    d = docx.Document()
    d.add_paragraph("DOCX content for York")
    d.save(docx_path)

    result = service.extract_text("sample.docx", docx_path.read_bytes())
    assert "DOCX content for York" in result["text"]
