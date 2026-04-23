from __future__ import annotations

from fastapi import UploadFile

from app.services.extraction_service import ExtractionService


class IngestionService:
    def __init__(self, extraction_service: ExtractionService) -> None:
        self.extraction_service = extraction_service

    async def ingest(self, raw_text: str | None, files: list[UploadFile] | None) -> dict:
        extracted = []

        if raw_text and raw_text.strip():
            extracted.append({"source": "pasted_text", "type": "text", "text": self.extraction_service.normalize_text(raw_text)})

        if files:
            for upload in files:
                data = await upload.read()
                extracted.append(self.extraction_service.extract_text(upload.filename or "unknown", data))

        deduped_texts = self.extraction_service.deduplicate_chunks([item["text"] for item in extracted])
        source_refs = [f"{item['source']} ({item['type']})" for item in extracted]

        normalized_content = "\n\n".join(deduped_texts)
        return {
            "normalized_content": normalized_content,
            "sources": source_refs,
        }
