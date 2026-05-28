"""
app.py
──────
Entry point for the Streamlit app.
This file is intentionally thin — it only orchestrates the MVC layers:

  View   →  collects user input
  Controller →  runs AI analysis
  View   →  renders results
"""

import streamlit as st

from models import extract_text
from controllers import general_analysis, company_analysis
from views import (
    render_upload_section,
    render_analysis_type_selector,
    render_company_inputs,
    render_analysis,
)

# ── Page config ────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🚀",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
    }
    .title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #94a3b8;
        margin-top: 0;
        margin-bottom: 1.5rem;
    }
    .stButton>button {
        background-color: #2563eb;
        color: white;
        border-color: transparent;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
        color: white;
    }
    .card {
        background: #0f172a;
        border: 1px solid #1f2937;
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 20px;
    }
    .summary-item {
        margin-bottom: 14px;
        line-height: 1.5rem;
    }
    .content {
        color: #cbd5e1;
        line-height: 1.7rem;
    }
    .stMetric {
        background-color: #12263b;
        border-radius: 18px;
        padding: 18px;
    }
    .analysis-banner {
        background: linear-gradient(180deg, #111b2f 0%, #0b1324 100%);
        border: 1px solid #1f2a40;
        border-radius: 22px;
        padding: 32px;
        margin-bottom: 24px;
    }
    .analysis-banner h2 {
        margin: 0;
        color: #ffffff;
        font-size: 2rem;
        letter-spacing: 0.02em;
    }
    .analysis-banner .score {
        font-size: 3rem;
        font-weight: 700;
        margin-top: 0.5rem;
        color: #ffffff;
    }
    .analysis-banner .subtext {
        color: #94a3b8;
        margin-top: 0.5rem;
        font-size: 0.95rem;
    }
    .card h4 {
        color: #ffffff;
        margin-bottom: 14px;
    }
    .bullet-list {
        margin: 0;
        padding-left: 20px;
        color: #cbd5e1;
    }
    .bullet-list li {
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='title'>🚀 AI Resume Analyzer</div>", unsafe_allow_html=True)
st.markdown(
    "<p class='subtitle'>Upload your resume, compare it with hiring criteria, and get a polished ATS-ready version.</p>",
    unsafe_allow_html=True,
)

st.markdown("---")

# ── Upload ─────────────────────────────────────────────────────────────────────

uploaded_file = render_upload_section()

if uploaded_file is None:
    st.stop()

resume_text = extract_text(uploaded_file)
st.success("✅ Resume uploaded successfully!")

# ── Analysis type ──────────────────────────────────────────────────────────────

analysis_type = render_analysis_type_selector()

company_inputs: dict = {}
if analysis_type == "Company Specific":
    company_inputs = render_company_inputs()

# ── Analyze ────────────────────────────────────────────────────────────────────

if st.button("Analyze Resume"):
    with st.spinner("Analyzing resume…"):
        if analysis_type == "General":
            st.session_state.analysis = general_analysis(resume_text)
        else:
            st.session_state.analysis = company_analysis(
                resume_text,
                company_inputs.get("company_name", ""),
                company_inputs.get("job_role", ""),
                company_inputs.get("job_description", ""),
                company_inputs.get("company_profile", ""),
            )

# ── Results ────────────────────────────────────────────────────────────────────

if "analysis" in st.session_state:
    render_analysis(st.session_state.analysis, resume_text)
