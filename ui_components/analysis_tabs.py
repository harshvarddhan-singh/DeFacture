"""
Analysis tabs component for DeFacture

This module contains the code for the analysis tabs section of the application:
- Summary tab
- Context tab
- Related Articles tab
- Fact Check tab
"""

import streamlit as st

def render_analysis_tabs(article_data=None):
    """
    Renders the analysis tabs section
    
    Parameters:
    -----------
    article_data : dict, optional
        Data for the article being analyzed
    """
    if article_data is None:
        st.info("No article selected. Please select or enter an article to analyze.")
        return

    # Create tabs for different analysis views
    tab_summary, tab_context, tab_related, tab_factcheck = st.tabs([
        "Summary", "Context Analysis", "Related Articles", "Fact Check"
    ])

    # Summary tab
    with tab_summary:
        st.markdown(
            """
            <div class="card" style="background: linear-gradient(120deg, #fceabb 0%, #f8fafc 100%); border-radius: 18px; box-shadow: 0 4px 16px rgba(180,180,255,0.10); padding: 1.5rem; margin-bottom: 1.5rem;">
                <h3 style="color: #6c63ff;">Article Summary</h3>
                <span style="color: #ff6f91;">Summary content will appear here.</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Context Analysis tab
    with tab_context:
        st.markdown(
            """
            <div class="card" style="background: linear-gradient(120deg, #f8fafc 0%, #fceabb 100%); border-radius: 18px; box-shadow: 0 4px 16px rgba(180,180,255,0.10); padding: 1.5rem; margin-bottom: 1.5rem;">
                <h3 style="color: #ff6f91;">Context Analysis</h3>
                <span style="color: #6c63ff;">Context analysis will appear here.</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Related Articles tab
    with tab_related:
        st.markdown(
            """
            <div class="card" style="background: linear-gradient(120deg, #fceabb 0%, #f8fafc 100%); border-radius: 18px; box-shadow: 0 4px 16px rgba(180,180,255,0.10); padding: 1.5rem; margin-bottom: 1.5rem;">
                <h3 style="color: #6c63ff;">Related Articles</h3>
                <span style="color: #ff6f91;">Related articles will appear here.</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Fact Check tab
    with tab_factcheck:
        st.markdown(
            """
            <div class="card" style="background: linear-gradient(120deg, #f8fafc 0%, #fceabb 100%); border-radius: 18px; box-shadow: 0 4px 16px rgba(180,180,255,0.10); padding: 1.5rem; margin-bottom: 1.5rem;">
                <h3 style="color: #ff6f91;">Fact Check</h3>
                <span style="color: #6c63ff;">Fact check results will appear here.</span>
            </div>
            """,
            unsafe_allow_html=True
        )