"""Generate Word, PDF or Excel documents in memory from a text string.

Supported formats: 'docx', 'pdf', 'xlsx'.
Returns (bytes, filename, mime_type).
"""

import io


def _parse_blocks(text: str):
    """Yield (is_heading, content) from text; lines starting with '# ' are headings."""
    for line in text.splitlines():
        stripped = line.rstrip()
        if stripped.startswith("# "):
            yield True, stripped[2:].strip()
        elif stripped.strip():
            yield False, stripped.strip()


def _fpdf_safe(s: str) -> str:
    """Encode to Latin-1 for compatibility with fpdf 1.x (drops chars outside Latin-1)."""
    return s.encode("latin-1", errors="replace").decode("latin-1")


def _to_docx(text: str) -> bytes:
    import docx
    doc = docx.Document()
    for is_heading, content in _parse_blocks(text):
        if is_heading:
            doc.add_heading(content, level=1)
        else:
            doc.add_paragraph(content)
    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()


def _to_pdf(text: str) -> bytes:
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    for is_heading, content in _parse_blocks(text):
        safe = _fpdf_safe(content)
        if is_heading:
            pdf.set_font("Helvetica", "B", 14)
            pdf.multi_cell(0, 9, safe)
            pdf.ln(2)
        else:
            pdf.set_font("Helvetica", size=11)
            pdf.multi_cell(0, 7, safe)
            pdf.ln(1)
    raw = pdf.output(dest="S")
    return raw.encode("latin-1") if isinstance(raw, str) else bytes(raw)


def _to_xlsx(text: str) -> bytes:
    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if any("|" in ln for ln in lines):
        for line in lines:
            row = [c.strip() for c in line.split("|") if c.strip()]
            if row:
                ws.append(row)
    else:
        for line in lines:
            ws.append([line])
    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


def generate_document(text: str, fmt: str) -> tuple[bytes, str, str]:
    """Generate a document and return (bytes, filename, mime_type)."""
    if fmt == "pdf":
        return _to_pdf(text), "documento.pdf", "application/pdf"
    if fmt == "xlsx":
        mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        return _to_xlsx(text), "documento.xlsx", mime
    mime = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    return _to_docx(text), "documento.docx", mime
