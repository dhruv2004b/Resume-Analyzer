from dotenv import load_dotenv
import os

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

MODELS = [
    "deepseek/deepseek-v4-flash:free",
    "google/gemma-2-9b-it:free",
    "meta-llama/llama-3.3-8b-instruct:free",
    "mistralai/mistral-7b-instruct:free",
    "poolside/laguna-xs.2:free",
    "poolside/laguna-m.1:free",
    "moonshotai/kimi-k2.6:free",
    "google/gemma-4-31b-it:free",
    "nvidia/nemotron-3-super-120b-a12b:free",
    "nvidia/llama-nemotron-embed-vl-1b-v2:free",
    "minimax/minimax-m2.5:free",
    "liquid/lfm-2.5-1.2b-thinking:free",
    "liquid/lfm-2.5-1.2b-instruct:free",
    "nvidia/nemotron-3-nano-30b-a3b:free",
    
]

REQUEST_TIMEOUT = 60