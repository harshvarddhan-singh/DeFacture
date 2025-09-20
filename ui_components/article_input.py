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
from tools.fetcher import fetch_article_with_newspaper

def render_article_input():
    # Increase tab label and selectbox label font size
    st.markdown("""
        <style>
        div[data-testid='stTabs'] button {
            font-size: 3rem !important;
            padding: 1.1rem 2.0rem !important;
        }
        label[for^='Select a sample article:'] {
            font-size: 2.0rem !important;
        }
        label[for^='Enter a news article URL:'] {
            font-size: 2.0rem !important;
        }
        </style>
    """, unsafe_allow_html=True)
    """
    Renders the article input section
    
    Returns:
    --------
    dict or None
        The selected article data if an article is selected, None otherwise
    """



    st.markdown(
        """
        <div class="card" style="background: linear-gradient(120deg, #38b2ac 0%, #e3f0fc 100%); border-radius: 14px; box-shadow: 0 2px 8px rgba(180,180,200,0.08); padding: 0.8rem; margin-bottom: 1.2rem; text-align: center;">
            <h2 style="color: #234e52; font-family: 'Inter', 'Segoe UI', sans-serif; font-size: 1.1rem; margin-bottom: 0.3rem;">Select an Article</h2>
            <span style="color: #234e52; font-size: 0.95rem; font-weight: 500;">Scroll down the page and choose a sample or enter a URL to analyze.</span>
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
                index=None
            )

            if selected_article:
                # Find the selected article
                selected_article_data = next((article for article in sample_articles if article["title"] == selected_article), None)
                st.success(f"Selected: {selected_article}")

                if st.button("Analyze Article", type="primary"):
                    st.markdown("""
                        <style>
                        .stButton > button {
                            font-size: 3.5rem !important;
                            padding: 0.8rem 2.2rem !important;
                        }
                        </style>
                    """, unsafe_allow_html=True)
                    selected_article_data["source"] = "sample"
                    article_data = selected_article_data
                
        except Exception as e:
            st.error(f"Error loading sample articles: {e}")
    
    # Enter URL tab
    with input_tab2:
        url = st.text_input("Enter a news article URL:", placeholder="https://...")
        if url:
            if st.button("Fetch Article"):
                st.markdown("""
                    <style>
                    .stButton > button {
                        font-size: 1.15rem !important;
                        padding: 0.8rem 2.2rem !important;
                    }
                    </style>
                """, unsafe_allow_html=True)
                st.info(f"Fetching article from: {url}")
                url_article_data = fetch_article_with_newspaper(url)
                if url_article_data:
                    article_data = url_article_data
    
    # Preview section if article is selected
    if article_data:
        st.divider()
        
        # Beautiful header for preview section
        st.markdown(
            """
            <div style="text-align: center; margin-bottom: 1.5rem;">
                <h2 style="background: linear-gradient(90deg, #234e52 0%, #38b2ac 100%); background-clip: text; -webkit-background-clip: text; color: transparent; font-size: 1.8rem; font-family: 'Inter', 'Segoe UI', sans-serif; margin-bottom: 0.3rem;">📖 Article Preview</h2>
                <span style="color: #1e293b; font-size: 1rem; font-weight: 500;">Extracted content from your selected article</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Article title card
        if "title" in article_data and article_data["title"]:
            st.markdown(
                f"""
                <div class="card" style="background: linear-gradient(120deg, #e3f0fc 0%, #f8fafc 100%); border-radius: 16px; padding: 1.2rem; margin-bottom: 1rem; box-shadow: 0 4px 16px rgba(180,180,200,0.10); border: 1px solid #e3e3e3;">
                    <h3 style="color: #234e52; font-size: 1.3rem; margin-bottom: 0.5rem; font-family: 'Inter', 'Segoe UI', sans-serif;">📰 Article Title</h3>
                    <p style="color: #1e293b; font-size: 1.1rem; font-weight: 500; margin-bottom: 0; line-height: 1.4;">{article_data['title']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Authors and Published Date card
        col1, col2 = st.columns(2)
        
        with col1:
            # Authors card
            authors_info = "Not available"
            if "authors" in article_data and article_data["authors"]:
                if isinstance(article_data["authors"], list) and article_data["authors"]:
                    authors_info = ", ".join(article_data["authors"])
                else:
                    authors_info = str(article_data["authors"])
            
            st.markdown(
                f"""
                <div class="card" style="background: linear-gradient(120deg, #fceabb 0%, #f8fafc 100%); border-radius: 16px; padding: 1.2rem; margin-bottom: 1rem; box-shadow: 0 4px 16px rgba(180,180,200,0.10); border: 1px solid #e3e3e3;">
                    <h4 style="color: #234e52; font-size: 1.1rem; margin-bottom: 0.5rem; font-family: 'Inter', 'Segoe UI', sans-serif;">� Authors</h4>
                    <p style="color: #1e293b; font-size: 0.95rem; margin-bottom: 0; line-height: 1.3;">{authors_info}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col2:
            # Published date card
            date_info = "Not available"
            if "publish_date" in article_data and article_data["publish_date"]:
                date_info = str(article_data["publish_date"]).split(' ')[0] if ' ' in str(article_data["publish_date"]) else str(article_data["publish_date"])
            
            st.markdown(
                f"""
                <div class="card" style="background: linear-gradient(120deg, #f8fafc 0%, #e3f0fc 100%); border-radius: 16px; padding: 1.2rem; margin-bottom: 1rem; box-shadow: 0 4px 16px rgba(180,180,200,0.10); border: 1px solid #e3e3e3;">
                    <h4 style="color: #234e52; font-size: 1.1rem; margin-bottom: 0.5rem; font-family: 'Inter', 'Segoe UI', sans-serif;">� Published</h4>
                    <p style="color: #1e293b; font-size: 0.95rem; margin-bottom: 0; line-height: 1.3;">{date_info}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Content preview card
        if "content" in article_data and article_data["content"]:
            content = article_data["content"]
            preview_text = content[:400] + "..." if len(content) > 400 else content
            word_count = len(content.split())
            
            st.markdown(
                f"""
                <div class="card" style="background: linear-gradient(120deg, #e3f0fc 0%, #fceabb 50%, #f8fafc 100%); border-radius: 16px; padding: 1.5rem; margin-bottom: 1rem; box-shadow: 0 4px 16px rgba(180,180,200,0.10); border: 1px solid #e3e3e3;">
                    <h3 style="color: #234e52; font-size: 1.3rem; margin-bottom: 0.8rem; font-family: 'Inter', 'Segoe UI', sans-serif;">📝 Content</h3>
                    <div style="background: rgba(255, 255, 255, 0.7); border-radius: 12px; padding: 1rem; margin-bottom: 1rem; border: 1px solid #e3e3e3;">
                        <p style="color: #1e293b; font-size: 1rem; line-height: 1.6; margin-bottom: 0; text-align: justify;">{preview_text}</p>
                    </div>
                    <div style="display: flex; gap: 1rem; justify-content: center;">
                        <span style="background: linear-gradient(90deg, #234e52 0%, #38b2ac 100%); color: white; padding: 0.4rem 1rem; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">📊 {len(content):,} characters</span>
                        <span style="background: linear-gradient(90deg, #38b2ac 0%, #234e52 100%); color: white; padding: 0.4rem 1rem; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">📖 ~{word_count:,} words</span>
                        <span style="background: linear-gradient(90deg, #234e52 0%, #38b2ac 100%); color: white; padding: 0.4rem 1rem; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">⏱️ ~{max(1, word_count // 200)} min read</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div class="card" style="background: linear-gradient(120deg, #fceabb 0%, #f8fafc 100%); border-radius: 16px; padding: 1.5rem; margin-bottom: 1rem; box-shadow: 0 4px 16px rgba(180,180,200,0.10); border: 1px solid #e3e3e3; text-align: center;">
                    <h3 style="color: #ff6f91; font-size: 1.2rem; margin-bottom: 0.5rem;">⚠️ No Content Available</h3>
                    <p style="color: #1e293b; font-size: 1rem; margin-bottom: 0;">Unable to extract content from this article.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Success message
        st.markdown(
            """
            <div style="text-align: center; margin-top: 1rem;">
                <span style="background: linear-gradient(90deg, #38b2ac 0%, #234e52 100%); color: white; padding: 0.6rem 1.5rem; border-radius: 25px; font-size: 0.95rem; font-weight: 600; box-shadow: 0 2px 8px rgba(180,180,200,0.15);">🎉 Article successfully extracted and ready for analysis!</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    return article_data