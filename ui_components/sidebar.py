"""
Sidebar component for DeFacture

This module contains the code for the sidebar:
- Agent toggles
- Search functionality
- Information and links
"""

import streamlit as st

def render_sidebar():
    """
    Renders the sidebar with navigation and controls
    """
    with st.sidebar:
        st.title("DeFacture")
        st.markdown("### News Analysis Tool")
        
        st.divider()
        
        # Agent toggles
        st.subheader("Analysis Settings")
        use_langchain = st.toggle("Use LangChain API", value=False)
        
        st.divider()
        
        # Navigation
        st.subheader("Navigation")
        st.page_link("main.py", label="Home", icon="🏠")
        st.page_link("pages/history.py", label="History", icon="📚")
        st.page_link("pages/settings.py", label="Settings", icon="⚙️")
        
        st.divider()
        
        # About section
        st.subheader("About")
        st.markdown("DeFacture helps analyze news articles for context and accuracy.")
        
        # Version info
        st.caption("v0.1.0 | Prototype")
        
    return {"use_langchain": use_langchain}