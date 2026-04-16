from dotenv import load_dotenv
import os
from functools import lru_cache


load_dotenv()

class Settings:
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.langchain_tracing_v2 = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
        self.langchain_api_key = os.getenv("LANGCHAIN_API_KEY")
        self.langchain_project = os.getenv("LANGCHAIN_PROJECT")
        self.webhook_secret = os.getenv("WEBHOOK_SECRET")
        self.redis_url = os.getenv("REDIS_URL")
    
@lru_cache()
def get_settings():
    return Settings()