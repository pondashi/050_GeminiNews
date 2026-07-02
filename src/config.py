import os

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

TARGET_THEME = os.environ.get("TARGET_THEME", "半導体")
TARGET_TICKERS = os.environ.get("TARGET_TICKERS", "NVDA,TSM,6920.T")

def validate_config():
    missing = []
    if not GEMINI_API_KEY:
        missing.append("GEMINI_API_KEY")
    if not WEBHOOK_URL:
        missing.append("WEBHOOK_URL")
    
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
