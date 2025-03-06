## Resume parsing logic # app/resume_parser.py

from PyPDF2 import PdfReader
from docx import Document
import spacy
from spacy.matcher import PhraseMatcher
import io

nlp = spacy.load("en_core_web_sm")

SKILL_PATTERNS = {
    "Software Engineer": [
        "Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust",
        "React", "Angular", "Vue.js", "Node.js", "Django", "Flask", 
        "SQL", "NoSQL", "Git", "Docker", "AWS", "Azure", "CI/CD",
        "Data Structures", "Algorithms", "System Design", "Testing"
    ],
    "Data Scientist": [
        "Python", "R", "SQL", "Machine Learning", "Deep Learning", 
        "TensorFlow", "PyTorch", "Pandas", "NumPy", "SciPy", "Scikit-learn",
        "Data Visualization", "Statistical Analysis", "Big Data",
        "Hadoop", "Spark", "NLP", "Computer Vision"
    ],
    "Frontend Developer": [
        "HTML", "CSS", "JavaScript", "TypeScript", "React", "Angular", 
        "Vue.js", "Redux", "Webpack", "Babel", "SASS/SCSS", "Responsive Design",
        "UI/UX", "Jest", "Cypress", "GraphQL", "REST APIs"
    ],
    "Backend Developer": [
        "Python", "Java", "C#", "Node.js", "Go", "Ruby", "PHP",
        "Django", "Flask", "Express", "Spring Boot", "ASP.NET",
        "SQL", "NoSQL", "MongoDB", "PostgreSQL", "MySQL", "Redis",
        "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Microservices"
    ],
    "DevOps Engineer": [
        "Linux", "Bash", "Python", "Docker", "Kubernetes", "CI/CD",
        "Jenkins", "GitLab CI", "GitHub Actions", "AWS", "Azure", "GCP",
        "Terraform", "Ansible", "Chef", "Puppet", "Monitoring", "Logging",
        "Security", "Networking"
    ]
}

def parse_resume(file_content: bytes, content_type: str) -> dict:
    text = ""

    # Extract text based on file type
    if content_type == "application/pdf":
        text = extract_text_from_pdf(file_content)
    elif content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text = extract_text_from_docx(file_content)

    # # Perform analysis with spaCy (e.g., skill extraction)
    # doc = nlp(text)
    # skills = [ent.text for ent in doc.ents if ent.label_ in ["SKILL", "QUALIFICATION"]]
    skills = extract_skills(text)
    return {"text": text, "skills": skills}

def extract_text_from_pdf(file_content: bytes) -> str:
    pdf_reader = PdfReader(io.BytesIO(file_content))
    text = " ".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
    return text

def extract_text_from_docx(file_content: bytes) -> str:
    doc = Document(io.BytesIO(file_content))
    text = " ".join([para.text for para in doc.paragraphs])
    return text

def extract_skills(text):
    # Create a matcher with the vocabulary of the language model
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    
    # Convert skill patterns to spaCy Doc objects
    patterns = [nlp(skill) for skill in SKILL_PATTERNS]
    
    # Add patterns to the matcher
    matcher.add("SKILLS", None, *patterns)
    
    doc = nlp(text)
    matches = matcher(doc)
    
    # Extract matched skills
    skills = set()
    for match_id, start, end in matches:
        span = doc[start:end]
        skills.add(span.text)
    
    return list(skills)