"""Extracts plain text from an uploaded MOM file (PDF, DOCX, or TXT)."""

import io


def extract_text(uploaded_file) -> str:
    """
    uploaded_file: a Streamlit UploadedFile object (has .name and behaves like a file).
    Returns plain text content.
    """
    name = uploaded_file.name.lower()
    raw = uploaded_file.read()

    if name.endswith(".txt"):
        return raw.decode("utf-8", errors="ignore")

    if name.endswith(".pdf"):
        return _extract_pdf(raw)

    if name.endswith(".docx"):
        return _extract_docx(raw)

    raise ValueError(f"Unsupported file type: {name}. Please upload a .txt, .pdf, or .docx file.")


def _extract_pdf(raw_bytes: bytes) -> str:
    import pdfplumber
    text_parts = []
    with pdfplumber.open(io.BytesIO(raw_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return "\n".join(text_parts)


def _extract_docx(raw_bytes: bytes) -> str:
    from docx import Document
    doc = Document(io.BytesIO(raw_bytes))
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
