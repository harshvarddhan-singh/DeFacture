"""
Header component for DeFacture

This module contains the code for the header section of the application:
- Title
- Subtitle
- Stats block
"""

import streamlit as st

def render_header():
    """
    Renders the header section with title, subtitle and stats
    """
    st.title("DeFacture: News Analysis & Fact-Checking")
    st.markdown("### Analyze news articles for context, bias, and factual accuracy")
    
    # Optional: Add stats in a metrics section
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Articles Analyzed", value="0")
    with col2:
        st.metric(label="Sources Tracked", value="0")
    with col3:
        st.metric(label="Fact Checks", value="0")