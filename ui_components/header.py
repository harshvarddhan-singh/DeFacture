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
    
    # Add CSS for metric cards hover effects
    st.markdown(
        """
        <style>
        .metric-card {
            transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        }
        .metric-card:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

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



    # Enhanced metrics block with prominent labels
    st.markdown(
        """
        <div style="display: flex; gap: 0.75rem; margin-top: 0.5rem; margin-bottom: 0.5rem;">
            <div class="metric-card" style="flex: 1; text-align: center; background: linear-gradient(120deg, #e3f0fc 0%, #f8fafc 100%); border-radius: 8px; padding: 0.75rem; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06); border: 1px solid rgba(227,240,252,0.4); min-height: 80px; display: flex; flex-direction: column; justify-content: center; cursor: pointer;">
                <span style="font-size: 1.25rem; color: #234e52; font-weight: 700; line-height: 1; margin-bottom: 0.25rem;">0</span>
                <span style="color: #1e293b; font-size: 1rem; font-weight: 600; margin-top: 0.1rem;"><strong>Articles Analyzed</strong></span>
            </div>
            <div class="metric-card" style="flex: 1; text-align: center; background: linear-gradient(120deg, #e3f0fc 0%, #f8fafc 100%); border-radius: 8px; padding: 0.75rem; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06); border: 1px solid rgba(227,240,252,0.4); min-height: 80px; display: flex; flex-direction: column; justify-content: center; cursor: pointer;">
                <span style="font-size: 1.25rem; color: #1e293b; font-weight: 700; line-height: 1; margin-bottom: 0.25rem;">0</span>
                <span style="color: #234e52; font-size: 1rem; font-weight: 600; margin-top: 0.1rem;"><strong>Sources Tracked</strong></span>
            </div>
            <div class="metric-card" style="flex: 1; text-align: center; background: linear-gradient(120deg, #e3f0fc 0%, #f8fafc 100%); border-radius: 8px; padding: 0.75rem; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06); border: 1px solid rgba(227,240,252,0.4); min-height: 80px; display: flex; flex-direction: column; justify-content: center; cursor: pointer;">
                <span style="font-size: 1.25rem; color: #234e52; font-weight: 700; line-height: 1; margin-bottom: 0.25rem;">0</span>
                <span style="color: #234e52; font-size: 1rem; font-weight: 600; margin-top: 0.1rem;"><strong>Fact Checks</strong></span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )