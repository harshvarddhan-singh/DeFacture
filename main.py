"""
DeFacture - News Analysis Prototype
-----------------------------------
A streamlined tool for analyzing news articles and checking factual accuracy.

This module contains the main Streamlit application with a modular structure:
- UI components in separate modules
- Analysis tools for different aspects of news articles
- Clean separation of concerns for maintainability
"""

import streamlit as st
import json
from pathlib import Path

# Import UI components
from ui_components.header import render_header
from ui_components.sidebar import render_sidebar
from ui_components.article_input import render_article_input
from ui_components.analysis_tabs import render_analysis_tabs

# Import analysis tools
from tools.analysis import (
    mock_summarization_chain,
    mock_context_analysis_chain,
    mock_related_articles_chain,
    mock_fact_check_chain
)

# Import config for LangChain API
from config.config import USE_LANGCHAIN_API

# ===== Page Configuration =====
st.set_page_config(
    page_title="DeFacture - News Analysis Prototype",
    page_icon="",
    layout="wide"
)

# Apply custom CSS
def load_css():
    """Load custom CSS from the assets directory"""
    css_path = Path(__file__).parent / "assets" / "styles.css"
    with open(css_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # Load Font Awesome for consistent icons
    st.markdown(
        """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        """,
        unsafe_allow_html=True
    )

try:
    load_css()
except Exception as e:
    st.warning(f"Could not load custom CSS: {str(e)}")

# ===== Main Application =====
def main():
    """Main application function with modular components"""
    
    # Initialize application metrics if they don't exist
    if 'metrics' not in st.session_state:
        st.session_state.metrics = {
            'articles_analyzed': 0,
            'sources_tracked': 0,
            'fact_checks': 0
        }
        
    # Load metrics from data file if it exists (simulated here)
    # In a real app, this would load from a database or file
    try:
        # This is just a placeholder - in a real app you'd load from a file or database
        # For demo purposes, we'll set some initial values if they don't exist
        if st.session_state.metrics['articles_analyzed'] == 0:
            # Set some initial demo values
            st.session_state.metrics.update({
                'articles_analyzed': 12,  # Demo value
                'sources_tracked': 8,    # Demo value
                'fact_checks': 6        # Demo value
            })
    except Exception as e:
        st.error(f"Error loading metrics: {str(e)}")
    
    # 1. Render the sidebar
    sidebar_options = render_sidebar()

    # 2. Render the header
    render_header()


    # 2.5. Ultra-tight Hero Section
    st.markdown(
        """
        <div style="margin: 0.5rem 0; padding: 0.5rem 1rem; border-radius: 8px; background: linear-gradient(120deg, #e3f0fc 0%, #f8fafc 100%); box-shadow: 0 1px 4px rgba(180,180,200,0.04); text-align: center;">
            <h2 style="font-size: 1.25rem; font-family: 'Inter', 'Segoe UI', sans-serif; color: #234e52; margin-bottom: 0.2rem; line-height: 1.2;">Welcome to DeFacture!</h2>
            <p style="font-size: 0.85rem; color: #1e293b; font-weight: 500; margin-bottom: 0.25rem; line-height: 1.3;">Your streamlined tool for news analysis and fact-checking.</p>
            <a href="#article-input" style="display: inline-block; background: linear-gradient(90deg, #2563eb 0%, #1e40af 100%); color: white; padding: 0.25rem 0.75rem; border-radius: 6px; font-size: 0.75rem; font-weight: 600; text-decoration: none; box-shadow: 0 1px 3px rgba(37, 99, 235, 0.2);">Get started by selecting an article below!</a>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # 3. Article Input Section
    article_data = render_article_input()
    
    # 4. Analysis Section (only shown when in analysis mode)
    if article_data and st.session_state.get('analysis_mode', False):
        # Run analysis (would connect to actual analysis in a real app)
        with st.spinner("Analyzing article..."):
            # Update metrics when an article is analyzed
            # Only increment for new articles (check if already analyzed)
            article_id = article_data.get('id', '')
            if 'analyzed_articles' not in st.session_state:
                st.session_state.analyzed_articles = set()
                
            if article_id and article_id not in st.session_state.analyzed_articles:
                # Increment the articles analyzed counter
                st.session_state.metrics['articles_analyzed'] += 1
                
                # Track this article as analyzed
                st.session_state.analyzed_articles.add(article_id)
                
                # Track the source if available
                source = article_data.get('source_name', '')
                if source and 'tracked_sources' not in st.session_state:
                    st.session_state.tracked_sources = set()
                    
                if source and source not in st.session_state.get('tracked_sources', set()):
                    st.session_state.tracked_sources.add(source)
                    st.session_state.metrics['sources_tracked'] += 1
            
            # Here we're just passing the article data to the tabs component
            render_analysis_tabs(article_data)
            
            # Increment fact checks when using fact check tab
            if st.session_state.get('used_fact_check_tab', False):
                st.session_state.metrics['fact_checks'] += 1
                # Reset the flag
                st.session_state.used_fact_check_tab = False
    
# Run the application
if __name__ == "__main__":
    main()
