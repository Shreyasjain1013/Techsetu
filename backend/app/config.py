import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root or backend directory
root_dir = Path(__file__).resolve().parent.parent.parent
env_paths = [root_dir / ".env", Path(__file__).resolve().parent.parent / ".env"]
for env_path in env_paths:
    if env_path.exists():
        load_dotenv(env_path)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("LLM_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_PUBLISHABLE_KEY = os.getenv("SUPABASE_PUBLISHABLE_KEY") or os.getenv("SUPABASE_ANON_KEY", "")
PORT = int(os.getenv("PORT", "8000"))
HOST = os.getenv("HOST", "0.0.0.0")
