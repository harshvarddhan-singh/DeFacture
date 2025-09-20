"""
Configuration settings for DeFacture

This module contains configuration settings for the application.
"""

# Import required modules
import os
from pathlib import Path

# Paths and directories
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"

# API usage toggle
# True  => use real summarizer for URL articles
# False => always use mock
USE_LANGCHAIN_API = True

# API keys and credentials (in a real app, these would be loaded from environment variables)
API_KEYS = {
    "langchain": os.environ.get("LANGCHAIN_API_KEY", ""),
}

# Model configuration
HF_SUMMARIZATION_MODEL = "facebook/bart-large-cnn"
HF_MAX_LENGTH = 1024
HF_MIN_LENGTH = 128

# Content configuration
CONTENT_CONFIG = {
    "max_article_length": 10000,
    "summary_length": 200,
    "max_summary_length": 200,
    "default_language": "en",
    "max_sources_per_query": 5,
    "max_related_articles": 5,
    "min_similarity_score": 0.7,
    "max_context_items": 5
}

# UI configuration
UI_CONFIG = {
    "theme": "light",
    "accent_color": "#2B6CB0",
    "show_metrics": True,
    "glassmorphism": True
}

# Models configuration
MODELS = {
    "summarization": "gpt-3.5-turbo",
    "fact_checking": "gpt-4",
    "embedding": "text-embedding-3-small",
    "huggingface": HF_SUMMARIZATION_MODEL,
    "openai": {
        "model": "gpt-3.5-turbo",
        "temperature": 0.7
    }
}

# Cache configuration
CACHE_CONFIG = {
    "ttl": 3600,  # Time to live in seconds (1 hour)
    "max_entries": 100,
    "enabled": True,
    "expiry": 24,  # Cache expiry in hours
    "size": 100    # Cache size in MB
}