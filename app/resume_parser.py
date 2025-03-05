## Resume parsing logic # app/resume_parser.py

from PyPDF2 import PdfReader
from docx import Document
import spacy
import io

nlp = spacy.load("en_core_web_sm")

def parse_resume(file_content: bytes, content_type: str) -> dict:
    text = ""

    # Extract text based on file type
    if content_type == "application/pdf":
        text = extract_text_from_pdf(file_content)
    elif content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text = extract_text_from_docx(file_content)

    # Perform analysis with spaCy (e.g., skill extraction)
    doc = nlp(text)
    skills = [ent.text for ent in doc.ents if ent.label_ in ["SKILL", "QUALIFICATION"]]

    return {"text": text, "skills": skills}

def extract_text_from_pdf(file_content: bytes) -> str:
    pdf_reader = PdfReader(io.BytesIO(file_content))
    text = " ".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
    return text

def extract_text_from_docx(file_content: bytes) -> str:
    doc = Document(io.BytesIO(file_content))
    text = " ".join([para.text for para in doc.paragraphs])
    return text
