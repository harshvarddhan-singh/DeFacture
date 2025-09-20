"""
Analysis tabs component for DeFacture

This module contains the code for the analysis tabs section of the application:
- Summary tab
- Context tab
- Related Articles tab
- Fact Check tab
"""

import streamlit as st
from tools.analysis import (
    mock_summarization_chain,
    real_summarization_chain,
    mock_context_analysis_chain,
    mock_related_articles_chain,
    mock_fact_check_chain,
)

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
        summary_result = None
        
        # Get toggle state from session state (defaults to False if not set)
        use_langchain_toggle = st.session_state.get('use_langchain_toggle', False)

        # Sample articles ALWAYS use mock (keeps demo consistent)
        if article_data.get("source") == "sample":
            summary_result = mock_summarization_chain(article_data.get("content", ""))

        # URL articles: require the toggle ON for real summarizer
        elif article_data.get("source") == "url":
            if not use_langchain_toggle:
                st.info("ℹ️ Turn ON the LangChain toggle in the sidebar to run real AI summarization for URLs. Showing mock demo for now.")
                summary_result = mock_summarization_chain(article_data.get("content", ""))
            else:
                try:
                    with st.spinner("Running real AI summarization (offline LexRank)..."):
                        summary_result = real_summarization_chain(article_data.get("content", ""))
                except Exception as e:
                    st.warning(f"⚠️ Real summarizer failed, falling back to mock. Error: {e}")
                    summary_result = mock_summarization_chain(article_data.get("content", ""))

        # Fallback if source unknown
        else:
            summary_result = mock_summarization_chain(article_data.get("content", ""))

        # Render in beautiful card
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(227,240,252,0.8) 100%); backdrop-filter: blur(20px); border: 1px solid rgba(227,240,252,0.3); border-radius: 20px; box-shadow: 0 8px 32px rgba(180,180,200,0.1); padding: 2rem; margin-bottom: 1.5rem; position: relative; overflow: hidden;">
                <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
                    <div style="background: linear-gradient(135deg, #234e52, #38b2ac); border-radius: 12px; padding: 0.7rem; margin-right: 1rem; box-shadow: 0 4px 15px rgba(35, 78, 82, 0.3);">
                        <div style="width: 24px; height: 24px; color: white; font-size: 16px; display: flex; align-items: center; justify-content: center;">📄</div>
                    </div>
                    <h3 style="color: #234e52; font-size: 1.4rem; font-weight: 700; margin: 0; background: linear-gradient(135deg, #234e52 0%, #38b2ac 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                        Article Summary
                    </h3>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Summary content box - escape HTML content
        import html
        escaped_summary = html.escape(summary_result.get('summary', 'No summary available.'))
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, rgba(255, 255, 255, 0.92) 0%, rgba(227, 240, 252, 0.88) 100%); border-left: 4px solid #38b2ac; border-radius: 0 16px 16px 0; padding: 1.8rem; margin-bottom: 1rem; box-shadow: 0 4px 16px rgba(180,180,200,0.12); border: 1px solid rgba(227,240,252,0.4);">
                <p style="color: #1a202c; font-size: 1.05rem; line-height: 1.7; margin: 0; text-align: justify; font-family: 'Inter', 'Segoe UI', sans-serif; font-weight: 500;">
                    {escaped_summary}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Attribution
        st.markdown(
            """
            <div style="text-align: center; opacity: 0.8; margin-bottom: 2rem;">
                <span style="color: #234e52; font-size: 0.85rem; font-weight: 500; font-family: 'Inter', 'Segoe UI', sans-serif;">
                    ✨ Generated with AI-powered analysis
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Render key points if available
        if summary_result.get("key_points"):
            st.markdown(
                """
                <div style="background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(252,234,187,0.8) 100%); backdrop-filter: blur(20px); border: 1px solid rgba(252,234,187,0.3); border-radius: 20px; box-shadow: 0 8px 32px rgba(180,180,200,0.1); padding: 2rem; margin-bottom: 1.5rem;">
                    <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
                        <div style="background: linear-gradient(135deg, #4169e1, #4682b4); border-radius: 12px; padding: 0.7rem; margin-right: 1rem; box-shadow: 0 4px 15px rgba(65, 105, 225, 0.3);">
                            <div style="width: 24px; height: 24px; color: white; font-size: 16px; display: flex; align-items: center; justify-content: center;">🎯</div>
                        </div>
                        <h3 style="color: #234e52; font-size: 1.4rem; font-weight: 700; margin: 0; background: linear-gradient(135deg, #4169e1 0%, #4682b4 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-family: 'Inter', 'Segoe UI', sans-serif;">
                            Key Takeaways
                        </h3>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Individual key point cards with app's color scheme
            for i, point in enumerate(summary_result["key_points"], 1):
                # Sophisticated color schemes matching the app
                colors = [
                    {"bg": "#234e52", "shadow": "rgba(35, 78, 82, 0.15)", "accent": "#38b2ac"},
                    {"bg": "#4169e1", "shadow": "rgba(65, 105, 225, 0.15)", "accent": "#4682b4"}, 
                    {"bg": "#38b2ac", "shadow": "rgba(56, 178, 172, 0.15)", "accent": "#234e52"},
                    {"bg": "#2563eb", "shadow": "rgba(37, 99, 235, 0.15)", "accent": "#1e293b"},
                    {"bg": "#1e293b", "shadow": "rgba(30, 41, 59, 0.15)", "accent": "#38b2ac"}
                ]
                color_scheme = colors[(i-1) % len(colors)]
                
                # Escape HTML content for key points
                escaped_point = html.escape(point)
                st.markdown(
                    f"""
                    <div style="background: linear-gradient(120deg, rgba(255, 255, 255, 0.92) 0%, rgba(227,240,252,0.88) 100%); backdrop-filter: blur(15px); border: 1px solid rgba(227,240,252,0.5); border-radius: 16px; padding: 1.4rem; margin-bottom: 1rem; box-shadow: 0 6px 20px {color_scheme['shadow']}; position: relative; border-left: 4px solid {color_scheme['bg']};">
                        <div style="position: absolute; top: -8px; left: 15px; background: {color_scheme['bg']}; color: white; border-radius: 50%; width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; font-size: 0.85rem; font-weight: bold; box-shadow: 0 2px 8px {color_scheme['shadow']};">
                            {i}
                        </div>
                        <div style="margin-top: 0.5rem; padding-left: 0.5rem;">
                            <p style="color: #1a202c; font-size: 1rem; line-height: 1.6; margin: 0; text-align: justify; font-family: 'Inter', 'Segoe UI', sans-serif; font-weight: 500;">
                                {escaped_point}
                            </p>
                        </div>
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