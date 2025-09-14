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


        # Icon, heading, subtitle
        st.markdown(
            """
            <div style="text-align: center; margin-bottom: 1.5rem;">
                <img src='https://cdn.pixabay.com/photo/2015/10/31/12/00/financial-equalization-1015309_1280.jpg' width='48' style='border-radius: 12px; box-shadow: 0 2px 8px #e3f0fc; object-fit: cover;' />
                <h2 style='background: linear-gradient(90deg, #4169e1 0%, #4682b4 100%); background-clip: text; -webkit-background-clip: text; color: transparent; font-size: 1.6rem; font-family: Inter, Segoe UI, sans-serif; margin-bottom: 0;'>DeFacture</h2>
                <span style='color: #234e52; font-size: 1rem; font-weight: 500;'>News Analysis Tool</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.divider()


    # Removed custom navigation bar to rely on Streamlit multipage navigation


        # Analysis Settings
        st.subheader("Analysis Settings 🛠️")
        use_langchain = st.toggle("LangChain", value=False)

        st.divider()

        # About section
        st.subheader("About 💡")
        st.markdown(
            """
            <div style='background: linear-gradient(90deg, #e3f0fc 0%, #f8fafc 100%); border-radius: 12px; padding: 0.7rem 1rem; color: #234e52; font-size: 1rem; font-weight: 500; box-shadow: 0 2px 8px rgba(180,180,200,0.07);'>
                DeFacture helps analyze news articles for context and accuracy.<br>
                <span style='font-size: 0.95rem; color: #2563eb;'>Developed by Harshvarddhan Singh</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.caption("v0.1.0 | Prototype")

    return {"use_langchain": use_langchain}