"""
models/resume.py
────────────────
Data-layer helpers: extract plain text from PDF and DOCX uploads.
No Streamlit imports here — pure I/O logic.
"""

from io import BytesIO

import pdfplumber
from docx import Document


def extract_pdf_text(pdf_file: BytesIO) -> str:
    """Return concatenated text from every page of a PDF file-like object."""
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def extract_docx_text(docx_file: BytesIO) -> str:
    """Return newline-joined paragraph text from a DOCX file-like object."""
    doc = Document(docx_file)
    return "\n".join(para.text for para in doc.paragraphs)


def extract_text(uploaded_file) -> str:
    """
    Dispatch to the correct extractor based on file extension.

    Parameters
    ----------
    uploaded_file : Streamlit UploadedFile

    Returns
    -------
    str  Raw resume text, or empty string if type is unsupported.
    """
    ext = uploaded_file.name.rsplit(".", 1)[-1].lower()
    if ext == "pdf":
        return extract_pdf_text(uploaded_file)
    if ext == "docx":
        return extract_docx_text(uploaded_file)
    return ""
