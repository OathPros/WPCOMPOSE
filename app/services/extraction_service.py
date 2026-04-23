from __future__ import annotations

import io
import re
from difflib import SequenceMatcher
from pathlib import Path

import docx
import fitz


class ExtractionService:
    supported_extensions = {".pdf", ".docx", ".txt", ".md"}

    def extract_text(self, filename: str, data: bytes) -> dict:
        ext = Path(filename).suffix.lower()
        if ext not in self.supported_extensions:
            raise ValueError(f"Unsupported file type: {ext}")

        if ext == ".pdf":
            text = self._extract_pdf(data)
        elif ext == ".docx":
            text = self._extract_docx(data)
        else:
            text = data.decode("utf-8", errors="ignore")

        normalized = self.normalize_text(text)
        return {
            "source": filename,
            "type": ext,
            "text": normalized,
        }

    def _extract_pdf(self, data: bytes) -> str:
        with fitz.open(stream=data, filetype="pdf") as pdf:
            return "\n".join(page.get_text("text") for page in pdf)

    def _extract_docx(self, data: bytes) -> str:
        file_obj = io.BytesIO(data)
        document = docx.Document(file_obj)
        return "\n".join(p.text for p in document.paragraphs)

    def normalize_text(self, text: str) -> str:
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def deduplicate_chunks(self, chunks: list[str], threshold: float = 0.93) -> list[str]:
        unique: list[str] = []
        for chunk in chunks:
            if not chunk.strip():
                continue
            if any(SequenceMatcher(None, chunk, existing).ratio() >= threshold for existing in unique):
                continue
            unique.append(chunk)
        return unique
