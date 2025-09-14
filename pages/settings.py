"""
Settings page for the DeFacture news analysis system.
"""

import streamlit as st
import json
from pathlib import Path
from typing import Dict

from config.config import (
    DATA_DIR, CONTENT_CONFIG, MODELS,
    UI_CONFIG, CACHE_CONFIG
)

def load_user_settings() -> Dict:
    """Load user-specific settings from JSON file."""
    settings_file = DATA_DIR / "user_settings.json"
    if not settings_file.exists():
        return {}
    
    try:
        with open(settings_file, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        st.error("Error loading settings file.")
        return {}

def save_user_settings(settings: Dict):
    """Save user-specific settings to JSON file."""
    settings_file = DATA_DIR / "user_settings.json"
    try:
        with open(settings_file, 'w') as f:
            json.dump(settings, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving settings: {str(e)}")
        return False

def main():
    st.title("DeFacture Settings")
    
    st.info(
        """
        ℹ️ **Prototype Settings**
        
        These settings are provided to demonstrate configuration capabilities.
        In a production system, additional validation, persistence, and security
        measures would be implemented.
        """
    )
    
    st.markdown("Configure analysis parameters and display preferences")
    
    # Load current settings
    user_settings = load_user_settings()
    
    # Content Analysis Settings
    st.markdown("### Content Analysis Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        max_summary = st.number_input(
            "Maximum Summary Length",
            min_value=100,
            max_value=1000,
            value=user_settings.get('max_summary_length', 
                                  CONTENT_CONFIG['max_summary_length'])
        )
        
        max_related = st.number_input(
            "Maximum Related Articles",
            min_value=1,
            max_value=10,
            value=user_settings.get('max_related_articles',
                                  CONTENT_CONFIG['max_related_articles'])
        )
    
    with col2:
        min_similarity = st.slider(
            "Minimum Similarity Score",
            min_value=0.0,
            max_value=1.0,
            value=user_settings.get('min_similarity_score',
                                  CONTENT_CONFIG['min_similarity_score'])
        )
        
        max_context = st.number_input(
            "Maximum Context Items",
            min_value=1,
            max_value=10,
            value=user_settings.get('max_context_items',
                                  CONTENT_CONFIG['max_context_items'])
        )
    
    # Model Settings
    st.markdown("### Model Settings")
    
    summarization_model = st.selectbox(
        "Summarization Model",
        options=["Falconsai/text_summarization", 
                "facebook/bart-large-cnn",
                "t5-small"],
        index=0
    )
    
    openai_model = st.selectbox(
        "OpenAI Model",
        options=["gpt-3.5-turbo", "gpt-4"],
        index=0
    )
    
    temperature = st.slider(
        "Model Temperature",
        min_value=0.0,
        max_value=1.0,
        value=user_settings.get('temperature', 
                              MODELS['openai']['temperature'])
    )
    
    # Cache Settings
    st.markdown("### Cache Settings")
    
    cache_enabled = st.toggle(
        "Enable Caching",
        value=user_settings.get('cache_enabled', 
                              CACHE_CONFIG.get('enabled', True))
    )
    
    if cache_enabled:
        cache_expiry = st.number_input(
            "Cache Expiry (hours)",
            min_value=1,
            max_value=168,
            value=user_settings.get('cache_expiry', 24)
        )
        
        cache_size = st.number_input(
            "Maximum Cache Size (MB)",
            min_value=10,
            max_value=1000,
            value=user_settings.get('cache_size', 100)
        )
    
    # Save Settings
    if st.button("Save Settings", type="primary"):
        new_settings = {
            'max_summary_length': max_summary,
            'max_related_articles': max_related,
            'min_similarity_score': min_similarity,
            'max_context_items': max_context,
            'summarization_model': summarization_model,
            'openai_model': openai_model,
            'temperature': temperature,
            'cache_enabled': cache_enabled,
            'cache_expiry': cache_expiry if cache_enabled else 24,
            'cache_size': cache_size if cache_enabled else 100
        }
        
        if save_user_settings(new_settings):
            st.success("Settings saved successfully!")
            st.rerun()
    
    # Reset to Defaults
    if st.button("Reset to Defaults", type="secondary"):
        if save_user_settings({}):
            st.success("Settings reset to defaults!")
            st.rerun()

if __name__ == "__main__":
    main()
