# app/main.py

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from app.resume_parser import parse_resume
from app.job_skills import JOB_SKILLS

app = FastAPI()

@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...), 
    job_roles: str = Form(...)
):
    if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        return JSONResponse(content={"error": "Unsupported file type"}, status_code=400)

    # Parse the resume
    file_content = await file.read()
    parsed_data = parse_resume(file_content, file.content_type)
    resume_skills = set(parsed_data.get("skills", []))

    # Parse job roles from the form input (comma-separated)
    selected_jobs = job_roles.split(",")
    matched_skills = {}
    missing_skills = {}

    # Match skills with job requirements
    for job in selected_jobs:
        required_skills = set(JOB_SKILLS.get(job, []))
        matched = resume_skills & required_skills
        missing = required_skills - resume_skills
        matched_skills[job] = list(matched)
        missing_skills[job] = list(missing)

    return {
        "parsed_data": parsed_data,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }
