import os
from dotenv import load_dotenv

# Load .env file, or fallback to env if that file is present.
load_dotenv()
load_dotenv("env", override=False)

# Gemini accepts GOOGLE_API_KEY or GEMINI_API_KEY in most environments.
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")