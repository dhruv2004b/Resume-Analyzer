"""
controllers/ai_service.py
─────────────────────────
All AI business logic using Ollama Local AI.
"""

import os
import streamlit as st

try:
    import ollama
    _OLLAMA_AVAILABLE = True
except ModuleNotFoundError:
    ollama = None
    _OLLAMA_AVAILABLE = False

MODEL_NAME = os.environ.get("OLLAMA_MODEL", "llama3")

_SYSTEM_PROMPT = """
You are an elite ATS (Applicant Tracking System) Resume Analyzer, 
Resume Optimizer, and Senior HR Specialist with 15+ years of experience 
in technical recruitment at top companies like Google, Amazon, and Microsoft.

Your job is to:
- Deeply analyze resumes for ATS compatibility
- Identify gaps, weaknesses, and missing keywords
- Provide actionable, specific improvement suggestions
- Generate professional, job-winning resume content
- Score resumes fairly and consistently based on actual content quality

You always respond with structured, well-formatted JSON. 
You never add commentary outside the JSON. 
You never hallucinate skills or experience not present in the resume.
"""


# ── Low-level AI call ────────────────────────────────────────────────────────

def ask_ai(prompt: str) -> str:
    if not _OLLAMA_AVAILABLE:
        st.error(
            "❌ The Ollama Python package is not installed. "
            "Install it with `pip install ollama` and restart the app."
        )
        return "AI response generation failed."

    try:
        st.info("🤖 Ollama Local AI is analyzing your resume…")
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user",   "content": prompt},
            ],
        )
        st.success("✅ Analysis complete!")
        return response["message"]["content"]
    except Exception as exc:
        st.error(f"❌ Ollama Error: {exc}")
        return "AI response generation failed."


# ── General Resume Analysis ──────────────────────────────────────────────────

def general_analysis(resume_text: str) -> str:
    prompt = f"""
Analyze the resume below and return ONLY a valid JSON object.
No extra text. No markdown. No code fences. Start with {{ end with }}.

ATS Scoring Rules (be consistent, base score purely on resume content):
  - Beginner / minimal content  : 40–60
  - Average fresher             : 60–72
  - Good fresher                : 72–82
  - Strong / experienced        : 82–92
  - Exceptional                 : 92–98

Return exactly this JSON structure (all keys required):

{{
  "ats_score": <integer 0-100>,

  "quick_resume_snapshot": {{
    "candidate_name"   : "<name from resume or 'Not Found'>",
    "current_role"     : "<current or target role>",
    "total_experience" : "<e.g. Fresher / 2 years / 5+ years>",
    "education"        : "<highest degree and college>",
    "top_tech_skills"  : ["<skill1>", "<skill2>", "<skill3>"],
    "resume_strength"  : "<one-line verdict e.g. 'Solid fresher resume with good projects'>"
  }},

  "top_strengths": [
    "<specific strength 1>",
    "<specific strength 2>",
    "<specific strength 3>"
  ],

  "weaknesses": [
    "<specific weakness 1>",
    "<specific weakness 2>",
    "<specific weakness 3>"
  ],

  "missing_skills": [
    "<skill missing from resume that is commonly expected for this role 1>",
    "<skill 2>",
    "<skill 3>"
  ],

  "important_ats_keywords_missing": [
    "<keyword 1>",
    "<keyword 2>",
    "<keyword 3>",
    "<keyword 4>",
    "<keyword 5>"
  ],

  "improvement_suggestions": [
    "<actionable suggestion 1 — be specific>",
    "<actionable suggestion 2>",
    "<actionable suggestion 3>",
    "<actionable suggestion 4>"
  ],

  "improved_professional_summary": "<Write a powerful 3-4 sentence ATS-optimized professional summary for this candidate. Include their role, key skills, notable achievements, and career goal.>"
}}

Resume:
{resume_text}
"""
    return ask_ai(prompt)


# ── Company Specific Analysis ────────────────────────────────────────────────

def company_analysis(
    resume_text: str,
    company_name: str,
    job_role: str,
    job_description: str,
    company_profile: str,
) -> str:
    prompt = f"""
Analyze how well this resume matches the given job and company.
Return ONLY a valid JSON object. No extra text. No markdown. No code fences.
Start with {{ end with }}.

ATS Match % Rules:
  - Poor match  : 20–45
  - Average     : 45–65
  - Good match  : 65–80
  - Strong match: 80–92
  - Near-perfect: 92–99

Return exactly this JSON structure:

{{
  "ats_match_percentage": <integer 0-100>,

  "quick_resume_snapshot": {{
    "candidate_name"   : "<name from resume or 'Not Found'>",
    "applying_for"     : "{job_role} at {company_name}",
    "total_experience" : "<Fresher / X years>",
    "education"        : "<highest degree>",
    "match_summary"    : "<one-line match verdict>"
  }},

  "missing_skills": [
    "<skill required by JD but not on resume 1>",
    "<skill 2>",
    "<skill 3>"
  ],

  "missing_keywords": [
    "<ATS keyword from JD not present in resume 1>",
    "<keyword 2>",
    "<keyword 3>",
    "<keyword 4>"
  ],

  "resume_weaknesses": "<paragraph describing the main gaps between resume and this specific job>",

  "important_improvements": "<paragraph with the most critical changes needed to pass ATS for this role>",

  "optimized_resume_summary": "<3-4 sentence professional summary tailored specifically for {job_role} at {company_name}, using keywords from the JD>",

  "optimized_skills_section": "<rewritten skills section as a comma-separated list, adding missing but learnable skills the candidate should highlight or add>",

  "optimized_project_descriptions": "<rewrite 2-3 existing projects with stronger action verbs, metrics, and keywords from the JD to make them ATS-friendly>"
}}

Resume:
{resume_text}

Company Name: {company_name}
Job Role: {job_role}
Job Description: {job_description}
Company Profile: {company_profile}
"""
    return ask_ai(prompt)


# ── Generate Improved Resume ─────────────────────────────────────────────────

def generate_improved_resume(original_resume: str, analysis: str) -> str:
    prompt = f"""
You are a world-class ATS Resume Writer.
Using the original resume and the analysis provided, write a complete, 
fully ATS-optimized, recruiter-ready resume.

Return ONLY a valid JSON object. No extra text. No markdown. No code fences.
Start with {{ end with }}.

Return exactly this JSON structure:

{{
  "final_resume": {{

    "name"    : "<candidate full name>",
    "title"   : "<professional title e.g. 'Full Stack Developer | Python | React'>",
    "contact" : {{
      "email"    : "<email or 'Not provided'>",
      "phone"    : "<phone or 'Not provided'>",
      "linkedin" : "<linkedin url or 'Not provided'>",
      "github"   : "<github url or 'Not provided'>",
      "location" : "<city, country or 'Not provided'>"
    }},

    "objective": "<Write a powerful 4-5 sentence ATS-optimized career objective. Include role, key skills, top achievements, and what value the candidate brings. Use action words and quantify where possible.>",

    "technical_skills": {{
      "languages"          : ["<lang1>", "<lang2>", "<lang3>"],
      "frameworks_libraries": ["<fw1>", "<fw2>", "<fw3>"],
      "databases"          : ["<db1>", "<db2>"],
      "concepts"           : ["<concept1>", "<concept2>", "<concept3>"]
    }},

    "tools_and_platforms": ["<tool1>", "<tool2>", "<tool3>", "<tool4>", "<tool5>"],

    "projects": [
      {{
        "name"       : "<Project Name>",
        "tech_stack" : "<comma-separated technologies used>",
        "description": "<2-3 sentence description with action verbs and impact. Quantify results where possible e.g. 'Reduced load time by 40%'>",
        "highlights" : ["<key achievement 1>", "<key achievement 2>"]
      }},
      {{
        "name"       : "<Project 2 Name>",
        "tech_stack" : "<tech stack>",
        "description": "<description>",
        "highlights" : ["<achievement 1>", "<achievement 2>"]
      }}
    ],

    "experience": [
      {{
        "role"        : "<Job Title>",
        "company"     : "<Company Name>",
        "duration"    : "<Start Month Year – End Month Year or Present>",
        "location"    : "<City or Remote>",
        "achievements": [
          "<Achievement with action verb and metric e.g. 'Increased API performance by 30% by implementing caching'>",
          "<Achievement 2>",
          "<Achievement 3>"
        ]
      }}
    ],

    "education": [
      {{
        "degree"     : "<Degree Name>",
        "institution": "<College / University Name>",
        "year"       : "<Graduation Year or Expected Year>",
        "score"      : "<CGPA / Percentage or 'Not mentioned'>"
      }}
    ],

    "certifications": [
      "<Certification 1 — Issuer — Year>",
      "<Certification 2 — Issuer — Year>"
    ],

    "achievements": [
      "<Notable achievement or award 1>",
      "<Notable achievement 2>"
    ]
  }}
}}

Original Resume:
{original_resume}

Analysis:
{analysis}
"""
    return ask_ai(prompt)
