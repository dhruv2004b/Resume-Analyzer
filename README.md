# 🚀 AI Resume Analyzer

An AI-powered ATS resume analyzer built with **Streamlit** and **OpenRouter**.  
Upload a PDF or DOCX resume to get an instant ATS score, gap analysis, and a fully optimized version ready to download.

---

## Features

- **General analysis** — ATS score, strengths, weaknesses, missing keywords, improved summary
- **Company-specific analysis** — match percentage against a job description + optimized resume sections
- **One-click export** — download the improved resume as `.docx` or `.pdf`
- **Model fallback** — tries multiple free LLMs in order; always gets a result

---

## Project Structure (MVC)

```
ai_resume_analyzer/
├── app.py                  # Entry point — thin orchestrator only
├── config/
│   └── settings.py         # API key, model list, timeouts
├── models/
│   ├── resume.py           # PDF / DOCX text extraction
│   └── exporter.py         # DOCX + PDF file generation
├── controllers/
│   └── ai_service.py       # OpenRouter API calls & prompt logic
├── views/
│   ├── upload_view.py      # Upload widget & input forms
│   └── analysis_view.py    # Results display & download buttons
└── utils/
    └── json_parser.py      # Safe JSON extraction from AI responses
```

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/your-username/ai-resume-analyzer.git
cd ai-resume-analyzer

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your API key (choose one method)

# Option A — environment variable (recommended)
export OPENROUTER_API_KEY="sk-or-v1-..."

# Option B — Streamlit secrets (for Streamlit Cloud)
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# then edit secrets.toml with your real key

# 4. Run
streamlit run app.py
```

---

## Deploying to Streamlit Cloud

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Select your repo, branch, and `app.py` as the entry file.
4. Under **Advanced settings → Secrets**, add:
   ```toml
   OPENROUTER_API_KEY = "sk-or-v1-..."
   ```
5. Click **Deploy**.

> ⚠️ Never commit your real API key. The `config/settings.py` falls back to an env variable; the hard-coded key in that file is a dev placeholder only.

---

## Environment Variables

| Variable | Description |
|---|---|
| `OPENROUTER_API_KEY` | Your [OpenRouter](https://openrouter.ai) API key |

---

## Tech Stack

| Layer | Library |
|---|---|
| UI | Streamlit |
| PDF parsing | pdfplumber |
| DOCX parsing | python-docx |
| AI backend | OpenRouter (multiple free models) |
| PDF export | ReportLab |
| DOCX export | python-docx |
