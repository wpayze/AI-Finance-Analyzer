import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """
    Application settings loaded from environment variables.
    """
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    """The API key for the Groq service."""

settings = Settings()
