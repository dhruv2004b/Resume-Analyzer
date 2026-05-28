"""
views/analysis_view.py
──────────────────────
Streamlit rendering for the analysis results panel.
Receives a parsed dict (or raw string) — no AI calls here.
"""

import streamlit as st

from utils import try_parse_json
from models import create_docx, create_pdf
from controllers import generate_improved_resume


def _format_value(value):
    if value is None:
        return "N/A"
    if isinstance(value, dict):
        lines = []
        for key, item in value.items():
            lines.append(f"**{key.replace('_', ' ').title()}:** {item}")
        return "<br>".join(lines)
    if isinstance(value, list):
        items = [f"• {item}" for item in value]
        return "<br>".join(items)
    return str(value)


def _render_banner(parsed: dict) -> None:
    ats_score = parsed.get("ats_score") or parsed.get("ats_match_percentage")
    if ats_score is None:
        return

    st.markdown(
        f"""
        <div class='analysis-banner'>
            <div>
                <h2>Resume Analysis</h2>
                <div class='score'>{ats_score}%</div>
                <div class='subtext'>Detailed ATS insights with strengths, weaknesses, missing skills, and keyword gaps.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_analysis_cards(parsed: dict) -> None:
    items = [
        ("Top Strengths", ["top_strengths", "optimized_skills_section"]),
        ("Weaknesses", ["weaknesses", "resume_weaknesses"]),
        ("Missing Skills", ["missing_skills"]),
        ("Keywords Missing", ["important_ats_keywords_missing", "missing_keywords"]),
        ("Improvement Suggestions", ["improvement_suggestions", "important_improvements"]),
        ("Improved Summary", ["improved_professional_summary", "optimized_resume_summary"]),
        ("Improved Skills", ["optimized_skills_section", "improved_skills"]),
        ("Recommendations", ["recommendations", "recommendation", "resume_recommendations"]),
    ]

    for label, keys in items:
        value = next((parsed[k] for k in keys if parsed.get(k)), None)
        if not value:
            continue

        html = [f"<div class='card'><h4>{label}</h4>"]
        if isinstance(value, str):
            html.append(f"<p>{value}</p>")
        elif isinstance(value, list):
            html.append("<ul class='bullet-list'>")
            for item in value:
                if isinstance(item, dict):
                    for inner_key, inner_value in item.items():
                        html.append(f"<li><strong>{inner_key.replace('_', ' ').title()}:</strong> {inner_value}</li>")
                else:
                    html.append(f"<li>{item}</li>")
            html.append("</ul>")
        elif isinstance(value, dict):
            html.append("<ul class='bullet-list'>")
            for key, item in value.items():
                if isinstance(item, list):
                    html.append(f"<li><strong>{key.replace('_', ' ').title()}:</strong></li>")
                    for entry in item:
                        html.append(f"<li style='margin-left:14px;'>- {entry}</li>")
                else:
                    html.append(f"<li><strong>{key.replace('_', ' ').title()}:</strong> {item}</li>")
            html.append("</ul>")
        html.append("</div>")

        st.markdown("".join(html), unsafe_allow_html=True)


def _render_resume_section(label: str, value) -> None:
    if not value:
        return

    st.markdown(f"### {label}")

    if isinstance(value, str):
        st.markdown(value)
        return

    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(item, list):
                st.markdown(f"**{key.replace('_', ' ').title()}:**")
                for entry in item:
                    st.markdown(f"- {entry}")
            else:
                st.markdown(f"**{key.replace('_', ' ').title()}:** {item}")
        return

    if isinstance(value, list):
        for item in value:
            if isinstance(item, dict):
                title = item.get("title") or item.get("role") or item.get("name")
                if title:
                    st.markdown(f"**{title}**")
                for field, detail in item.items():
                    if field == "title":
                        continue
                    if isinstance(detail, list):
                        for line in detail:
                            st.markdown(f"- {line}")
                    else:
                        st.markdown(f"- **{field.replace('_', ' ').title()}:** {detail}")
            else:
                st.markdown(f"- {item}")


def _render_final_resume(improved_text: str) -> None:
    parsed = try_parse_json(improved_text)
    if not parsed:
        st.error("Could not parse the improved resume JSON. Showing raw text instead.")
        st.code(improved_text)
        return

    resume = None
    if isinstance(parsed, dict):
        resume = parsed.get("final_resume") or parsed.get("final_ats_optimized_resume")
        if not resume and all(key in parsed for key in ["name", "title"]):
            resume = parsed

    if not resume or not isinstance(resume, dict):
        st.error("Improved resume JSON does not contain a valid resume object.")
        st.code(improved_text)
        return

    name = resume.get("name")
    title = resume.get("title") or resume.get("objective")
    contact = resume.get("contact") or resume.get("contact_info")

    if name:
        st.markdown(f"# {name}")
    if title and title != name:
        st.markdown(f"**{title}**")
    if contact:
        if isinstance(contact, list):
            st.markdown(" | ".join(contact))
        else:
            st.markdown(contact)

    _render_resume_section("Objective", resume.get("objective"))
    _render_resume_section("Education", resume.get("education"))
    _render_resume_section("Technical Skills", resume.get("technical_skills"))
    _render_resume_section("Tools & Platforms", resume.get("tools_and_platforms"))
    _render_resume_section("Projects", resume.get("projects"))
    _render_resume_section("Experience", resume.get("experience"))
    _render_resume_section("Certifications", resume.get("certifications"))
    _render_resume_section("Achievements", resume.get("achievements"))


def render_analysis(analysis_text: str, resume_text: str) -> None:
    """Display analysis results and wire up the 'Apply Changes' workflow."""
    st.subheader("📊 Resume Analysis")

    parsed = try_parse_json(analysis_text)

    if parsed:
        _render_banner(parsed)
        cols = st.columns([2, 1], gap="large")
        with cols[0]:
            _render_analysis_cards(parsed)
        with cols[1]:
            _render_summary_card(parsed)
    else:
        st.error("Unable to parse the resume analysis. Check the raw AI output below.")
        st.code(analysis_text, language="json")

    st.markdown("---")
    _render_apply_changes(resume_text, analysis_text)


def _render_summary_card(parsed: dict) -> None:
    """Render a small analysis summary card with the most important metrics."""
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h4>Quick Resume Snapshot</h4>", unsafe_allow_html=True)

    ats_score = parsed.get("ats_score") or parsed.get("ats_match_percentage")
    if ats_score is not None:
        st.markdown(f"<div class='summary-item'><strong>ATS Score:</strong> {ats_score}%</div>", unsafe_allow_html=True)

    summary_items = [
        ("Top Strengths", parsed.get("top_strengths")),
        ("Weaknesses", parsed.get("weaknesses")),
        ("Missing Skills", parsed.get("missing_skills")),
        ("Keywords Missing", parsed.get("important_ats_keywords_missing") or parsed.get("missing_keywords")),
    ]

    for label, value in summary_items:
        if value:
            formatted = _format_value(value)
            st.markdown(
                f"<div class='summary-item'><strong>{label}:</strong><br>{formatted}</div>",
                unsafe_allow_html=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)


# ── Private helpers ───────────────────────────────────────────────────────────


# ── Private helpers ────────────────────────────────────────────────────────────

def _render_parsed(parsed: dict) -> None:
    """Render the seven standard analysis fields from a parsed JSON dict."""
    fields = [
        ("ATS Score", ["ats_score", "ats_match_percentage"]),
        ("Top Strengths", ["top_strengths", "optimized_skills_section"]),
        ("Weaknesses", ["weaknesses", "resume_weaknesses"]),
        ("Missing Skills", ["missing_skills"]),
        ("Keywords Missing", ["important_ats_keywords_missing", "missing_keywords"]),
        ("Improvement Suggestions", ["improvement_suggestions", "important_improvements"]),
        ("Improved Summary", ["improved_professional_summary", "optimized_resume_summary"]),
    ]

    for label, keys in fields:
        value = next((parsed[k] for k in keys if parsed.get(k)), None)
        if value is None:
            continue

        formatted = _format_value(value)
        st.markdown(
            f"<div class='card'><h4>{label}</h4><div class='content'>{formatted}</div></div>",
            unsafe_allow_html=True,
        )


def _render_apply_changes(resume_text: str, analysis_text: str) -> None:
    """Render the 'Apply Changes' button and the download section."""
    if st.button("Apply Changes & Generate Resume"):
        with st.spinner("Generating ATS Optimized Resume..."):
            st.session_state.improved_resume = generate_improved_resume(
                resume_text, analysis_text
            )

    if "improved_resume" not in st.session_state:
        return

    st.subheader("🔥 Final ATS Optimized Resume")
    _render_final_resume(st.session_state.improved_resume)

    with st.expander("Show raw improved resume JSON"):
        st.code(st.session_state.improved_resume, language="json")

    export_format = st.selectbox(
        "Choose download format",
        ["DOCX", "PDF"],
        key="export_format",
    )

    improved = st.session_state.improved_resume

    if export_format == "DOCX":
        st.download_button(
            label="⬇ Download Improved Resume (.docx)",
            data=create_docx(improved),
            file_name="ATS_Optimized_Resume.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    else:
        st.download_button(
            label="⬇ Download Improved Resume (.pdf)",
            data=create_pdf(improved),
            file_name="ATS_Optimized_Resume.pdf",
            mime="application/pdf",
        )
