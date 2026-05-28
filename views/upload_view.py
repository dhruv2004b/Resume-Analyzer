"""
views/upload_view.py
────────────────────
Streamlit rendering for the upload panel and company-specific input form.
Returns data to app.py; no AI calls here.
"""

import streamlit as st


def render_upload_section():
    """
    Render the file-uploader widget.

    Returns
    -------
    UploadedFile | None
    """
    st.subheader("Upload Your Resume")
    st.markdown(
        "Upload a PDF or DOCX file and let the analyzer extract key resume details for ATS scoring."
    )
    return st.file_uploader(
        "Choose a resume file",
        type=["pdf", "docx"],
        help="Supported formats: PDF, DOCX",
    )


def render_analysis_type_selector() -> str:
    """
    Render the analysis-type radio and return the selected value.

    Returns
    -------
    str  "General" or "Company Specific"
    """

    st.subheader("Choose Analysis Type")

    return st.radio(
        "Select Analysis",
        ["General", "Company Specific"],
        label_visibility="collapsed",
        horizontal=True,
    )

def render_company_inputs() -> dict:
    """
    Render text inputs for company-specific analysis.

    Returns
    -------
    dict  with keys: company_name, job_role, job_description, company_profile
    """
    return {
        "company_name": st.text_input("Company Name"),
        "job_role": st.text_input("Job Role"),
        "job_description": st.text_area("Job Description", height=200),
        "company_profile": st.text_area("Company Profile", height=150),
    }
