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
    Renders the header section with title, subtitle, logo, and animated stats
    """


    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 1rem;">
            <img src="https://cdn.pixabay.com/photo/2015/10/31/12/00/financial-equalization-1015309_1280.jpg" width="60" style="border-radius: 12px; box-shadow: 0 2px 8px #e3f0fc; object-fit: cover;" />
            <h1 style="background: linear-gradient(90deg, #234e52 0%, #38b2ac 100%); background-clip: text; -webkit-background-clip: text; color: transparent; font-size: 2.8rem; font-family: 'Inter', 'Segoe UI', sans-serif; margin-bottom: 0;">DeFacture: News Analysis & Fact-Checking</h1>
        </div>
        <h3 style="color: #1e293b; font-weight: 500; margin-top: 0.5rem;">Analyze news articles for context, bias, and factual accuracy</h3>
        """,
        unsafe_allow_html=True
    )



    # Animated stats block
    st.markdown(
        """
        <div style="display: flex; gap: 2rem; margin-top: 1.5rem;">
            <div class="card" style="flex: 1; text-align: center;">
                <span style="font-size: 2.2rem; color: #234e52; font-weight: bold; animation: pulse 1.5s infinite;">0</span><br>
                <span style="color: #1e293b; font-size: 1.1rem;">Articles Analyzed</span>
            </div>
            <div class="card" style="flex: 1; text-align: center;">
                <span style="font-size: 2.2rem; color: #1e293b; font-weight: bold; animation: pulse 1.5s infinite;">0</span><br>
                <span style="color: #234e52; font-size: 1.1rem;">Sources Tracked</span>
            </div>
            <div class="card" style="flex: 1; text-align: center;">
                <span style="font-size: 2.2rem; color: #234e52; font-weight: bold; animation: pulse 1.5s infinite;">0</span><br>
                <span style="color: #234e52; font-size: 1.1rem;">Fact Checks</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )