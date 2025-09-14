"""
Article input component for DeFacture

This module contains the code for the article input section:
- Sample article selection
- URL input
- Article content preview
"""

import streamlit as st
import json
from pathlib import Path

def render_article_input():
    """
    Renders the article input section
    
    Returns:
    --------
    dict or None
        The selected article data if an article is selected, None otherwise
    """
    st.subheader("Select an Article")
    
    # Input method tabs
    input_tab1, input_tab2 = st.tabs(["Sample Articles", "Enter URL"])
    
    article_data = None
    
    # Sample Articles tab
    with input_tab1:
        try:
            # Load sample articles from JSON file
            sample_articles_path = Path(__file__).parent.parent / "data" / "sample_articles.json"
            with open(sample_articles_path, "r") as f:
                data = json.load(f)
                sample_articles = data["articles"]
            
            # Create dropdown for sample articles
            selected_article = st.selectbox(
                "Select a sample article:",
                options=[article["title"] for article in sample_articles],
                index=None,
                placeholder="Choose an article..."
            )
            
            if selected_article:
                # Find the selected article
                selected_article_data = next((article for article in sample_articles if article["title"] == selected_article), None)
                st.success(f"Selected: {selected_article}")
                
                if st.button("Analyze Article", type="primary"):
                    article_data = selected_article_data
                
        except Exception as e:
            st.error(f"Error loading sample articles: {e}")
    
    # Enter URL tab
    with input_tab2:
        url = st.text_input("Enter a news article URL:", placeholder="https://...")
        if url:
            if st.button("Fetch Article"):
                # This will be implemented to actually fetch the article
                st.info(f"Fetching article from: {url}")
                article_data = {"title": "Article from URL", "url": url}
    
    # Preview section if article is selected
    if article_data:
        st.divider()
        st.subheader("Article Preview")
        st.write("Article preview will appear here.")
    
    return article_data