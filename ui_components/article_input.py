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



    st.markdown(
        """
        <div class="card" style="background: linear-gradient(120deg, #38b2ac 0%, #e3f0fc 100%); border-radius: 18px; box-shadow: 0 4px 16px rgba(180,180,200,0.10); padding: 1.5rem; margin-bottom: 2rem; text-align: center;">
            <h2 style="color: #234e52; font-family: 'Inter', 'Segoe UI', sans-serif; font-size: 1.5rem; margin-bottom: 0.5rem;">Select an Article</h2>
            <span style="color: #234e52; font-size: 1.1rem; font-weight: 500;">Choose a sample or enter a URL to analyze.</span>
        </div>
        """,
        unsafe_allow_html=True
    )

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