"""Extract plain text from PDF, Word (.docx) and Excel (.xlsx) files."""

import docx
import pandas as pd
from pypdf import PdfReader


def extract_text(file) -> str:
    """Dispatch to the right reader based on file extension."""
    name = file.name.lower()
    if name.endswith(".pdf"):
        return _read_pdf(file)
    if name.endswith(".docx"):
        return _read_docx(file)
    if name.endswith((".xlsx", ".xls")):
        return _read_excel(file)
    raise ValueError(f"Unsupported file type: {file.name}")


def _read_pdf(file) -> str:
    reader = PdfReader(file)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def _read_docx(file) -> str:
    doc = docx.Document(file)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def _read_excel(file) -> str:
    sheets = pd.read_excel(file, sheet_name=None)
    parts = []
    for sheet_name, df in sheets.items():
        parts.append(f"Sheet: {sheet_name}\n{df.to_csv(index=False)}")
    return "\n\n".join(parts)
