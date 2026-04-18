"""
Configuration settings for the News Credibility Agent.
Set your API keys in environment variables or .env file.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# LLM Configuration
# Supported: groq, openrouter, huggingface
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")

# API Keys (set these in your .env file)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")

# Model selection
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-70b-instruct")

# RAG Configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Lightweight sentence transformer
FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH", "rag/data/faiss_index")
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K_RETRIEVAL = 3  # Number of documents to retrieve per claim

# Agent Configuration
MAX_CLAIMS_TO_ANALYZE = 5  # Limit claims for faster processing
CONFIDENCE_THRESHOLD_HIGH = 70
CONFIDENCE_THRESHOLD_LOW = 40

# UI Configuration
UI_TITLE = "News Credibility Analyzer"
UI_DESCRIPTION = "AI-powered misinformation detection and fact-checking system"


def get_llm_config():
    """Return LLM configuration based on provider."""
    if LLM_PROVIDER == "groq" and GROQ_API_KEY:
        return {
            "provider": "groq",
            "api_key": GROQ_API_KEY,
            "model": GROQ_MODEL,
            "temperature": 0.1,  # Low temperature for factual analysis
        }
    elif LLM_PROVIDER == "openrouter" and OPENROUTER_API_KEY:
        return {
            "provider": "openrouter",
            "api_key": OPENROUTER_API_KEY,
            "model": OPENROUTER_MODEL,
            "temperature": 0.1,
        }
    else:
        # Default to Groq if available
        return {
            "provider": "groq",
            "api_key": GROQ_API_KEY or "",
            "model": GROQ_MODEL,
            "temperature": 0.1,
        }
