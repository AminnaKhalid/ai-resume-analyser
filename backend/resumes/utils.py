import PyPDF2
import io
import json
import os
from groq import Groq
from decouple import config

GROQ_API_KEY = config('GROQ_API_KEY')

client = Groq(api_key=GROQ_API_KEY)

def extract_text_from_pdf(file):
    try:
        text = ""
        # File reading logic
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
        
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        
        return text.strip()
    except Exception as e:
        print(f"PDF Extraction Error: {str(e)}")
        return ""

def analyze_resume_with_ai(raw_text):
    # Agar text khali hai toh AI ko mat bhejo
    if not raw_text:
        return {
            "overall_score": 0,
            "ats_score": 0,
            "skills_found": [],
            "skills_missing": [],
            "experience_check": "Empty or unreadable PDF.",
            "suggestions": ["Please upload a valid text-based PDF."]
        }

    prompt = f"""
    You are a world-class ATS (Applicant Tracking System) and Senior HR Recruiter.
    Your task is to perform a deep-dive analysis of the provided resume text.

    CRITICAL INSTRUCTIONS:
    - Respond ONLY with a valid JSON object.
    - Do NOT include any conversational text, explanations, or markdown formatting (no ```json tags).
    - Be strict and honest with scores; only give 90+ if the resume is truly exceptional.

    JSON STRUCTURE:
    {{
        "overall_score": 0,
        "ats_score": 0,
        "skills_found": [],
        "skills_missing": [],
        "experience_check": "",
        "suggestions": []
    }}

    RESUME TEXT:
    {raw_text}
    """

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )

        result = response.choices[0].message.content.strip()

        # JSON Cleaning Logic
        if result.startswith('{'):
            json_str = result
        else:
            start = result.find('{')
            end = result.rfind('}') + 1
            json_str = result[start:end]

        return json.loads(json_str)

    except json.JSONDecodeError:
        return {
            "overall_score": 0,
            "ats_score": 0,
            "skills_found": [],
            "skills_missing": [],
            "experience_check": "Could not analyze resume format.",
            "suggestions": ["The AI output was not in correct format. Please try again."]
        }

    except Exception as e:
        return {
            "overall_score": 0,
            "ats_score": 0,
            "skills_found": [],
            "skills_missing": [],
            "experience_check": f"AI service error: {str(e)}",
            "suggestions": ["Check your internet or API key."]
        }

def extract_text_from_pdf(file):
    try:
        text = ""
        # File reading logic
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
        
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        
        return text.strip()
    except Exception as e:
        print(f"PDF Extraction Error: {str(e)}")
        return ""

def match_resume_with_jd(raw_text, job_description):
    prompt = f"""
You are a highly experienced ATS (Applicant Tracking System) and HR expert.

Analyze the resume against the job description and return a STRICT JSON response only.
Do NOT include any explanation, text, or formatting outside JSON.

Evaluation Rules:
- Consider skills, technologies, experience, projects, and education.
- Match both exact keywords and similar/related terms.
- Be realistic and critical (do NOT give very high scores unless it's truly a strong match).
- If important requirements are missing, clearly mention them in weak points.

Return ONLY this JSON format:
{{
    "match_percentage": number (0-100),
    "matching_keywords": ["relevant matched skills/technologies"],
    "missing_keywords": ["important skills missing from resume"],
    "strong_points": ["2-4 concise strengths"],
    "weak_points": ["2-4 clear gaps or weaknesses"],
    "recommendation": "Apply / Improve then apply / Not recommended"
}}

Resume:
\"\"\"{raw_text}\"\"\"

Job Description:
\"\"\"{job_description}\"\"\"
"""

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )

        result = response.choices[0].message.content

        if result.strip().startswith('{'):
            parsed = json.loads(result)
        else:
            start = result.find('{')
            end = result.rfind('}') + 1
            json_str = result[start:end]
            parsed = json.loads(json_str)

        return parsed

    except json.JSONDecodeError:
        return {
            "match_percentage": 0,
            "matching_keywords": [],
            "missing_keywords": [],
            "strong_points": [],
            "weak_points": [],
            "recommendation": "Could not analyze. Please try again."
        }

    except Exception as e:
        return {
            "match_percentage": 0,
            "matching_keywords": [],
            "missing_keywords": [],
            "strong_points": [],
            "weak_points": [],
            "recommendation": f"Service error: {str(e)}"
        }