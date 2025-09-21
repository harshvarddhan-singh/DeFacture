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
from tools.claim_extraction import extract_claims, get_claim_statistics
from tools.fact_check_agent import fact_check_claims, get_fact_check_statistics

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
    tab_summary, tab_context, tab_related, tab_claims, tab_factcheck_results = st.tabs([
        "Summary", "Context Analysis", "Related Articles", "Extraction", "Fact Check"
    ])

    # Summary tab
    with tab_summary:
        summary_result = None
        
        # Get toggle state from session state (defaults to False if not set)
        use_langchain_toggle = st.session_state.get('use_langchain_toggle', False)

        # Sample articles ALWAYS use mock (keeps demo consistent)
        if article_data.get("source") == "sample":
            summary_result = mock_summarization_chain(article_data.get("content", ""), article_data)

        # URL articles: require the toggle ON for real summarizer
        elif article_data.get("source") == "url":
            if not use_langchain_toggle:
                st.info("ℹ️ Turn ON the LangChain toggle in the sidebar to run real AI summarization for URLs. Showing mock demo for now.")
                summary_result = mock_summarization_chain(article_data.get("content", ""), article_data)
            else:
                try:
                    with st.spinner("Running real AI summarization (offline LexRank)..."):
                        summary_result = real_summarization_chain(article_data.get("content", ""))
                except Exception as e:
                    st.warning(f"⚠️ Real summarizer failed, falling back to mock. Error: {e}")
                    summary_result = mock_summarization_chain(article_data.get("content", ""), article_data)

        # Search results (SERP API): support real AI analysis with toggle
        elif article_data.get("source") == "search_result":
            if not use_langchain_toggle:
                st.info("ℹ️ Turn ON the LangChain toggle in the sidebar to run real AI summarization for SERP articles. Showing mock demo for now.")
                summary_result = mock_summarization_chain(article_data.get("content", ""), article_data)
            else:
                try:
                    with st.spinner("Running real AI summarization on SERP article..."):
                        summary_result = real_summarization_chain(article_data.get("content", ""))
                except Exception as e:
                    st.warning(f"⚠️ Real summarizer failed, falling back to mock. Error: {e}")
                    summary_result = mock_summarization_chain(article_data.get("content", ""), article_data)

        # Fallback if source unknown
        else:
            summary_result = mock_summarization_chain(article_data.get("content", ""), article_data)

        # Render in beautiful card with original gradient styling
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(227,240,252,0.8) 100%); 
                        backdrop-filter: blur(20px); 
                        border: 1px solid rgba(227,240,252,0.3); 
                        border-radius: 20px; 
                        box-shadow: 0 8px 32px rgba(180,180,200,0.1); 
                        padding: 2rem; 
                        margin-bottom: 1.5rem; 
                        position: relative; 
                        overflow: hidden;">
                <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
                    <div style="background: linear-gradient(135deg, #234e52, #38b2ac); 
                                border-radius: 12px; 
                                padding: 0.7rem; 
                                margin-right: 1rem; 
                                box-shadow: 0 4px 15px rgba(35, 78, 82, 0.3);">
                        <div style="width: 24px; height: 24px; color: white; font-size: 16px; display: flex; align-items: center; justify-content: center;">📄</div>
                    </div>
                    <h3 style="color: #234e52; 
                              font-size: 1.4rem; 
                              font-weight: 700; 
                              margin: 0; 
                              background: linear-gradient(135deg, #234e52 0%, #38b2ac 100%); 
                              -webkit-background-clip: text; 
                              -webkit-text-fill-color: transparent;">
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
            <div style="background: linear-gradient(135deg, rgba(255, 255, 255, 0.92) 0%, rgba(227, 240, 252, 0.88) 100%); 
                        border-left: 4px solid #38b2ac; 
                        border-radius: 0 16px 16px 0; 
                        padding: 1.8rem; 
                        margin-bottom: 1rem; 
                        box-shadow: 0 4px 16px rgba(180,180,200,0.12); 
                        border: 1px solid rgba(227,240,252,0.4);">
                <p style="color: #1a202c; 
                         font-size: 1.05rem; 
                         line-height: 1.7; 
                         margin: 0; 
                         text-align: justify; 
                         font-family: 'Inter', 'Segoe UI', sans-serif; 
                         font-weight: 500;">
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
                <div style="background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(252,234,187,0.8) 100%); 
                            backdrop-filter: blur(20px); 
                            border: 1px solid rgba(252,234,187,0.3); 
                            border-radius: 20px; 
                            box-shadow: 0 8px 32px rgba(180,180,200,0.1); 
                            padding: 2rem; 
                            margin-bottom: 1.5rem;">
                    <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
                        <div style="background: linear-gradient(135deg, #4169e1, #4682b4); 
                                    border-radius: 12px; 
                                    padding: 0.7rem; 
                                    margin-right: 1rem; 
                                    box-shadow: 0 4px 15px rgba(65, 105, 225, 0.3);">
                            <div style="width: 24px; height: 24px; color: white; font-size: 16px; display: flex; align-items: center; justify-content: center;">🎯</div>
                        </div>
                        <h3 style="color: #234e52; 
                                  font-size: 1.4rem; 
                                  font-weight: 700; 
                                  margin: 0; 
                                  background: linear-gradient(135deg, #4169e1 0%, #4682b4 100%); 
                                  -webkit-background-clip: text; 
                                  -webkit-text-fill-color: transparent; 
                                  font-family: 'Inter', 'Segoe UI', sans-serif;">
                            Key Takeaways
                        </h3>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Individual key point cards with sophisticated styling
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
                    <div style="background: linear-gradient(120deg, rgba(255, 255, 255, 0.92) 0%, rgba(227,240,252,0.88) 100%); 
                                backdrop-filter: blur(15px); 
                                border: 1px solid rgba(227,240,252,0.5); 
                                border-radius: 16px; 
                                padding: 1.4rem; 
                                margin-bottom: 1rem; 
                                box-shadow: 0 6px 20px {color_scheme['shadow']}; 
                                position: relative; 
                                border-left: 4px solid {color_scheme['bg']};">
                        <div style="position: absolute; 
                                    top: -8px; 
                                    left: 15px; 
                                    background: {color_scheme['bg']}; 
                                    color: white; 
                                    border-radius: 50%; 
                                    width: 28px; 
                                    height: 28px; 
                                    display: flex; 
                                    align-items: center; 
                                    justify-content: center; 
                                    font-size: 0.85rem; 
                                    font-weight: bold; 
                                    box-shadow: 0 2px 8px {color_scheme['shadow']};">
                            {i}
                        </div>
                        <div style="margin-top: 0.5rem; padding-left: 0.5rem;">
                            <p style="color: #1a202c; 
                                     font-size: 1rem; 
                                     line-height: 1.6; 
                                     margin: 0; 
                                     text-align: justify; 
                                     font-family: 'Inter', 'Segoe UI', sans-serif; 
                                     font-weight: 500;">
                                {escaped_point}
                            </p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # Context Analysis tab
    with tab_context:
        context_result = mock_context_analysis_chain(article_data.get("content", ""), article_data)
        
        # Render context analysis in beautiful card
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(252,234,187,0.8) 100%); backdrop-filter: blur(20px); border: 1px solid rgba(252,234,187,0.3); border-radius: 20px; box-shadow: 0 8px 32px rgba(180,180,200,0.1); padding: 2rem; margin-bottom: 1.5rem; position: relative; overflow: hidden;">
                <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
                    <div style="background: linear-gradient(135deg, #234e52, #38b2ac); border-radius: 12px; padding: 0.7rem; margin-right: 1rem; box-shadow: 0 4px 15px rgba(35, 78, 82, 0.3);">
                        <div style="width: 24px; height: 24px; color: white; font-size: 16px; display: flex; align-items: center; justify-content: center;">🔍</div>
                    </div>
                    <h3 style="color: #234e52; font-size: 1.4rem; font-weight: 700; margin: 0; background: linear-gradient(135deg, #234e52 0%, #38b2ac 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                        Context Analysis
                    </h3>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Perspective
        import html
        escaped_perspective = html.escape(context_result.get('perspective', 'No perspective analysis available.'))
        st.markdown(
            f"""
            <div style="background: rgba(255,255,255,0.9); border-radius: 15px; padding: 1.5rem; margin-bottom: 1rem; box-shadow: 0 4px 20px rgba(0,0,0,0.05); border-left: 4px solid #38b2ac;">
                <h4 style="color: #2d3748; margin: 0 0 0.75rem 0; font-size: 1.1rem; font-weight: 600; display: flex; align-items: center;">
                    <span style="margin-right: 0.5rem;">👁️</span> Perspective
                </h4>
                <p style="color: #4a5568; line-height: 1.6; margin: 0; font-size: 0.95rem;">{escaped_perspective}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Bias Indicators
        bias_indicators = context_result.get('bias_indicators', [])
        if bias_indicators:
            st.markdown(
                """
                <h4 style="color: #2d3748; margin: 1.5rem 0 0.75rem 0; font-size: 1.1rem; font-weight: 600; display: flex; align-items: center;">
                    <span style="margin-right: 0.5rem;">⚖️</span> Bias Indicators
                </h4>
                """,
                unsafe_allow_html=True
            )
            for indicator in bias_indicators:
                escaped_indicator = html.escape(indicator)
                st.markdown(
                    f"""
                    <div style="background: rgba(255,255,255,0.9); border-radius: 10px; padding: 1rem; margin-bottom: 0.5rem; box-shadow: 0 2px 10px rgba(0,0,0,0.03); border-left: 3px solid #fbb6ce;">
                        <p style="color: #4a5568; line-height: 1.5; margin: 0; font-size: 0.9rem;">• {escaped_indicator}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
        # Historical Context
        historical_context = context_result.get('historical_context', '')
        if historical_context:
            escaped_historical = html.escape(historical_context)
            st.markdown(
                f"""
                <div style="background: rgba(255,255,255,0.9); border-radius: 15px; padding: 1.5rem; margin: 1.5rem 0 1rem 0; box-shadow: 0 4px 20px rgba(0,0,0,0.05); border-left: 4px solid #9f7aea;">
                    <h4 style="color: #2d3748; margin: 0 0 0.75rem 0; font-size: 1.1rem; font-weight: 600; display: flex; align-items: center;">
                        <span style="margin-right: 0.5rem;">📚</span> Historical Context
                    </h4>
                    <p style="color: #4a5568; line-height: 1.6; margin: 0; font-size: 0.95rem;">{escaped_historical}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Missing Context
        missing_context = context_result.get('missing_context', '')
        if missing_context:
            escaped_missing = html.escape(missing_context)
            st.markdown(
                f"""
                <div style="background: rgba(255,255,255,0.9); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; box-shadow: 0 4px 20px rgba(0,0,0,0.05); border-left: 4px solid #ed8936;">
                    <h4 style="color: #2d3748; margin: 0 0 0.75rem 0; font-size: 1.1rem; font-weight: 600; display: flex; align-items: center;">
                        <span style="margin-right: 0.5rem;">⚠️</span> Missing Context
                    </h4>
                    <p style="color: #4a5568; line-height: 1.6; margin: 0; font-size: 0.95rem;">{escaped_missing}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Related Articles tab
    with tab_related:
        related_articles = mock_related_articles_chain(article_data.get("content", ""), article_data)
        
        # Render related articles in beautiful card
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(252,234,187,0.8) 100%); backdrop-filter: blur(20px); border: 1px solid rgba(252,234,187,0.3); border-radius: 20px; box-shadow: 0 8px 32px rgba(180,180,200,0.1); padding: 2rem; margin-bottom: 1.5rem; position: relative; overflow: hidden;">
                <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
                    <div style="background: linear-gradient(135deg, #234e52, #38b2ac); border-radius: 12px; padding: 0.7rem; margin-right: 1rem; box-shadow: 0 4px 15px rgba(35, 78, 82, 0.3);">
                        <div style="width: 24px; height: 24px; color: white; font-size: 16px; display: flex; align-items: center; justify-content: center;">🔗</div>
                    </div>
                    <h3 style="color: #234e52; font-size: 1.4rem; font-weight: 700; margin: 0; background: linear-gradient(135deg, #234e52 0%, #38b2ac 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                        Related Articles
                    </h3>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        if related_articles:
            for i, article in enumerate(related_articles):
                # Determine relevance color
                relevance = article.get('relevance', 'Medium').lower()
                if relevance == 'high':
                    relevance_color = '#10b981'
                    relevance_bg = 'rgba(16, 185, 129, 0.1)'
                elif relevance == 'medium':
                    relevance_color = '#f59e0b'
                    relevance_bg = 'rgba(245, 158, 11, 0.1)'
                else:
                    relevance_color = '#6b7280'
                    relevance_bg = 'rgba(107, 114, 128, 0.1)'
                
                # Determine perspective color
                perspective = article.get('perspective', 'Similar').lower()
                if perspective == 'supporting':
                    perspective_color = '#10b981'
                    perspective_icon = '✅'
                elif perspective == 'opposing':
                    perspective_color = '#ef4444'
                    perspective_icon = '❌'
                elif perspective == 'critical':
                    perspective_color = '#f59e0b'
                    perspective_icon = '⚠️'
                else:
                    perspective_color = '#6366f1'
                    perspective_icon = '🔄'
                
                import html
                escaped_title = html.escape(article.get('title', 'Untitled'))
                escaped_source = html.escape(article.get('source', 'Unknown Source'))
                escaped_url = html.escape(article.get('url', '#'))
                
                st.markdown(
                    f"""
                    <div style="background: rgba(255,255,255,0.95); border-radius: 15px; padding: 1.5rem; margin-bottom: 1rem; box-shadow: 0 4px 20px rgba(0,0,0,0.06); border: 1px solid rgba(0,0,0,0.05); transition: all 0.2s ease;">
                        <div style="display: flex; justify-content: between; align-items: flex-start; margin-bottom: 1rem;">
                            <h4 style="color: #1a202c; margin: 0; font-size: 1.05rem; font-weight: 600; flex: 1; line-height: 1.4;">
                                <a href="{escaped_url}" target="_blank" style="color: #2563eb; text-decoration: none; transition: color 0.2s ease;">{escaped_title}</a>
                            </h4>
                        </div>
                        
                        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.75rem;">
                            <div style="display: flex; align-items: center; gap: 0.25rem;">
                                <span style="font-size: 0.8rem;">📰</span>
                                <span style="color: #4a5568; font-size: 0.85rem; font-weight: 500;">{escaped_source}</span>
                            </div>
                            
                            <div style="display: flex; align-items: center; gap: 0.25rem;">
                                <span style="font-size: 0.8rem;">📅</span>
                                <span style="color: #6b7280; font-size: 0.8rem;">{article.get('date', 'Unknown Date')}</span>
                            </div>
                        </div>
                        
                        <div style="display: flex; gap: 0.75rem;">
                            <span style="background: {relevance_bg}; color: {relevance_color}; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.75rem; font-weight: 600;">
                                {article.get('relevance', 'Medium')} Relevance
                            </span>
                            
                            <span style="background: rgba({perspective_color[1:]}, 0.1); color: {perspective_color}; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.75rem; font-weight: 600; display: flex; align-items: center; gap: 0.25rem;">
                                {perspective_icon} {article.get('perspective', 'Similar')}
                            </span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                """
                <div style="background: rgba(255,255,255,0.9); border-radius: 15px; padding: 2rem; text-align: center; color: #6b7280;">
                    <p style="margin: 0; font-size: 0.95rem;">No related articles found.</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Extraction tab
    with tab_claims:
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(252,234,187,0.8) 100%); backdrop-filter: blur(20px); border: 1px solid rgba(252,234,187,0.3); border-radius: 20px; box-shadow: 0 8px 32px rgba(180,180,200,0.1); padding: 2rem; margin-bottom: 1.5rem;">
                <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
                    <div style="background: linear-gradient(135deg, #2563eb, #1e293b); border-radius: 12px; padding: 0.7rem; margin-right: 1rem; box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);">
                        <div style="width: 24px; height: 24px; color: white; font-size: 16px; display: flex; align-items: center; justify-content: center;">🔍</div>
                    </div>
                    <h3 style="color: #234e52; font-size: 1.4rem; font-weight: 700; margin: 0; background: linear-gradient(135deg, #2563eb 0%, #1e293b 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-family: 'Inter', 'Segoe UI', sans-serif;">
                        Extraction Agent
                    </h3>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        if article_data and article_data.get("content"):
            try:
                with st.spinner("Extracting factual claims from article..."):
                    claims = extract_claims(article_data["content"])
                    stats = get_claim_statistics(claims)
                    
                    # Store claims in session state for Fact-Check Results tab
                    st.session_state.extracted_claims = claims
                
                if claims:
                    # Display statistics
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(
                            f"""
                            <div style="background: linear-gradient(120deg, #e3f0fc 0%, #f8fafc 100%); border-radius: 12px; padding: 1rem; text-align: center; box-shadow: 0 2px 8px rgba(180,180,200,0.1);">
                                <h4 style="color: #234e52; margin: 0; font-size: 1.5rem;">{stats['total_claims']}</h4>
                                <p style="color: #1e293b; margin: 0; font-size: 0.9rem;">Total Claims</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    
                    with col2:
                        st.markdown(
                            f"""
                            <div style="background: linear-gradient(120deg, #fceabb 0%, #f8fafc 100%); border-radius: 12px; padding: 1rem; text-align: center; box-shadow: 0 2px 8px rgba(180,180,200,0.1);">
                                <h4 style="color: #234e52; margin: 0; font-size: 1.5rem;">{stats['avg_confidence']}</h4>
                                <p style="color: #1e293b; margin: 0; font-size: 0.9rem;">Avg Confidence</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    
                    with col3:
                        st.markdown(
                            f"""
                            <div style="background: linear-gradient(120deg, #f8fafc 0%, #e3f0fc 100%); border-radius: 12px; padding: 1rem; text-align: center; box-shadow: 0 2px 8px rgba(180,180,200,0.1);">
                                <h4 style="color: #234e52; margin: 0; font-size: 1.5rem;">{stats['high_confidence_count']}</h4>
                                <p style="color: #1e293b; margin: 0; font-size: 0.9rem;">High Confidence</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Display individual claims
                    for i, claim_data in enumerate(claims, 1):
                        claim_text = claim_data["claim"]
                        confidence = claim_data["confidence"]
                        
                        # Color scheme based on confidence
                        if confidence >= 0.8:
                            color_scheme = {"bg": "#38b2ac", "shadow": "rgba(56, 178, 172, 0.2)", "confidence_color": "#059669"}
                        elif confidence >= 0.6:
                            color_scheme = {"bg": "#4169e1", "shadow": "rgba(65, 105, 225, 0.2)", "confidence_color": "#2563eb"}
                        else:
                            color_scheme = {"bg": "#f59e0b", "shadow": "rgba(245, 158, 11, 0.2)", "confidence_color": "#d97706"}
                        
                        # Escape HTML content for claims
                        import html
                        escaped_claim = html.escape(claim_text)
                        
                        st.markdown(
                            f"""
                            <div style="background: linear-gradient(120deg, rgba(255, 255, 255, 0.92) 0%, rgba(227,240,252,0.88) 100%); backdrop-filter: blur(15px); border: 1px solid rgba(227,240,252,0.5); border-radius: 16px; padding: 1.4rem; margin-bottom: 1rem; box-shadow: 0 6px 20px {color_scheme['shadow']}; position: relative; border-left: 4px solid {color_scheme['bg']};">
                                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.8rem;">
                                    <div style="background: {color_scheme['bg']}; color: white; border-radius: 20px; padding: 0.3rem 0.8rem; font-size: 0.8rem; font-weight: bold;">
                                        Claim #{i}
                                    </div>
                                    <div style="background: {color_scheme['confidence_color']}; color: white; border-radius: 20px; padding: 0.3rem 0.8rem; font-size: 0.8rem; font-weight: bold;">
                                        {int(confidence * 100)}% confidence
                                    </div>
                                </div>
                                <div style="padding: 0.5rem 0;">
                                    <p style="color: #1a202c; font-size: 1rem; line-height: 1.6; margin: 0; text-align: justify; font-family: 'Inter', 'Segoe UI', sans-serif; font-weight: 500;">
                                        {escaped_claim}
                                    </p>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                
                else:
                    st.markdown(
                        """
                        <div style="background: linear-gradient(120deg, #fceabb 0%, #f8fafc 100%); border-radius: 16px; padding: 2rem; text-align: center; box-shadow: 0 4px 16px rgba(180,180,200,0.10); border: 1px solid #e3e3e3;">
                            <h3 style="color: #f59e0b; font-size: 1.2rem; margin-bottom: 0.5rem;">No Claims Detected</h3>
                            <p style="color: #1e293b; font-size: 1rem; margin-bottom: 0;">This article doesn't contain clearly identifiable factual claims with sufficient confidence.</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                
            except Exception as e:
                st.error(f"Error extracting claims: {str(e)}")
                st.markdown(
                    """
                    <div style="background: linear-gradient(120deg, #fceabb 0%, #f8fafc 100%); border-radius: 16px; padding: 1.5rem; text-align: center; box-shadow: 0 4px 16px rgba(180,180,200,0.10); border: 1px solid #e3e3e3;">
                        <h3 style="color: #ef4444; font-size: 1.2rem; margin-bottom: 0.5rem;">⚠️ Claim Extraction Failed</h3>
                        <p style="color: #1e293b; font-size: 1rem; margin-bottom: 0;">Please try again or select a different article.</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info("💡 Select an article to extract key information and analyze content structure.")

    # Fact-Check Results tab
    with tab_factcheck_results:
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,240,245,0.8) 100%); backdrop-filter: blur(20px); border: 1px solid rgba(255,240,245,0.3); border-radius: 20px; box-shadow: 0 8px 32px rgba(180,180,200,0.1); padding: 2rem; margin-bottom: 1.5rem;">
                <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
                    <div style="background: linear-gradient(135deg, #ef4444, #dc2626); border-radius: 12px; padding: 0.7rem; margin-right: 1rem; box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3);">
                        <div style="width: 24px; height: 24px; color: white; font-size: 16px; display: flex; align-items: center; justify-content: center;">✓</div>
                    </div>
                    <h3 style="color: #234e52; font-size: 1.4rem; font-weight: 700; margin: 0; background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-family: 'Inter', 'Segoe UI', sans-serif;">
                        Fact-Check Results
                    </h3>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # For sample articles, use mock fact check results directly
        if article_data.get("source") == "sample" and article_data.get("mock_analysis", {}).get("fact_check"):
            fact_check_result = article_data["mock_analysis"]["fact_check"]
            
            # Overall Assessment
            overall_assessment = fact_check_result.get('overall_assessment', 'Unknown')
            assessment_color = {
                'Highly Accurate': '#10b981',
                'Mostly Accurate': '#3b82f6', 
                'Partially Accurate': '#f59e0b',
                'Inaccurate': '#ef4444'
            }.get(overall_assessment, '#6b7280')
            
            import html
            escaped_assessment = html.escape(overall_assessment)
            st.markdown(
                f"""
                <div style="background: rgba(255,255,255,0.95); border-radius: 15px; padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 4px 20px rgba(0,0,0,0.06); border: 1px solid rgba(0,0,0,0.05); text-align: center;">
                    <h4 style="color: #1a202c; margin: 0 0 1rem 0; font-size: 1.2rem; font-weight: 600;">Overall Assessment</h4>
                    <div style="display: inline-block; background: {assessment_color}; color: white; padding: 0.75rem 1.5rem; border-radius: 25px; font-size: 1.1rem; font-weight: bold; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                        {escaped_assessment}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Individual Claims
            claims = fact_check_result.get('claims', [])
            if claims:
                st.markdown(
                    """
                    <h4 style="color: #1a202c; margin: 1.5rem 0 1rem 0; font-size: 1.1rem; font-weight: 600;">
                        📋 Individual Claims Analysis
                    </h4>
                    """,
                    unsafe_allow_html=True
                )
                
                for i, claim in enumerate(claims, 1):
                    assessment = claim.get('assessment', 'Unknown')
                    claim_text = claim.get('claim', '')
                    evidence = claim.get('evidence', '')
                    
                    # Color scheme based on assessment
                    color_schemes = {
                        'Accurate': {
                            'bg': '#10b981', 'emoji': '✅', 'shadow': 'rgba(16, 185, 129, 0.2)',
                            'verdict_bg': '#d1fae5', 'verdict_color': '#065f46'
                        },
                        'Partially Accurate': {
                            'bg': '#f59e0b', 'emoji': '⚠️', 'shadow': 'rgba(245, 158, 11, 0.2)',
                            'verdict_bg': '#fef3c7', 'verdict_color': '#92400e'
                        },
                        'False': {
                            'bg': '#ef4444', 'emoji': '❌', 'shadow': 'rgba(239, 68, 68, 0.2)',
                            'verdict_bg': '#fee2e2', 'verdict_color': '#991b1b'
                        }
                    }
                    color_scheme = color_schemes.get(assessment, color_schemes['Partially Accurate'])
                    
                    escaped_claim = html.escape(claim_text)
                    escaped_evidence = html.escape(evidence)
                    
                    st.markdown(
                        f"""
                        <div style="background: linear-gradient(120deg, rgba(255, 255, 255, 0.92) 0%, rgba(255,240,245,0.88) 100%); backdrop-filter: blur(15px); border: 1px solid rgba(255,240,245,0.5); border-radius: 16px; padding: 1.4rem; margin-bottom: 1rem; box-shadow: 0 6px 20px {color_scheme['shadow']}; position: relative; border-left: 4px solid {color_scheme['bg']};">
                            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                                <div style="background: {color_scheme['bg']}; color: white; border-radius: 20px; padding: 0.3rem 0.8rem; font-size: 0.8rem; font-weight: bold;">
                                    Claim #{i}
                                </div>
                                <div style="display: flex; align-items: center; gap: 0.5rem;">
                                    <span style="font-size: 0.9rem;">{color_scheme['emoji']}</span>
                                    <div style="background: {color_scheme['verdict_bg']}; color: {color_scheme['verdict_color']}; border-radius: 20px; padding: 0.3rem 0.8rem; font-size: 0.8rem; font-weight: bold;">
                                        {assessment}
                                    </div>
                                </div>
                            </div>
                            <div style="padding: 0.5rem 0; margin-bottom: 1rem;">
                                <p style="color: #1a202c; font-size: 1rem; line-height: 1.6; margin: 0; text-align: justify; font-family: 'Inter', 'Segoe UI', sans-serif; font-weight: 500;">
                                    {escaped_claim}
                                </p>
                            </div>
                            <div style="background: rgba(255, 255, 255, 0.6); border-radius: 8px; padding: 1rem; border: 1px solid rgba(0, 0, 0, 0.05);">
                                <p style="color: #6b7280; font-size: 0.9rem; line-height: 1.5; margin: 0; font-style: italic; font-family: 'Inter', 'Segoe UI', sans-serif;">
                                    <strong>Evidence:</strong> {escaped_evidence}
                                </p>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
        # For non-sample articles, check if we have extracted claims to fact-check (existing logic)
        elif hasattr(st.session_state, 'extracted_claims') and st.session_state.extracted_claims:
            try:
                with st.spinner("Fact-checking extracted claims..."):
                    fact_checked_claims = fact_check_claims(st.session_state.extracted_claims)
                    fact_check_stats = get_fact_check_statistics(fact_checked_claims)
                
                if fact_checked_claims:
                    # Display fact-check statistics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.markdown(
                            f"""
                            <div style="background: linear-gradient(120deg, #e3f0fc 0%, #f8fafc 100%); border-radius: 12px; padding: 1rem; text-align: center; box-shadow: 0 2px 8px rgba(180,180,200,0.1);">
                                <h4 style="color: #234e52; margin: 0; font-size: 1.3rem;">{fact_check_stats['total_claims']}</h4>
                                <p style="color: #1e293b; margin: 0; font-size: 0.85rem;">Total Checked</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    
                    with col2:
                        st.markdown(
                            f"""
                            <div style="background: linear-gradient(120deg, #dcfce7 0%, #f0fdf4 100%); border-radius: 12px; padding: 1rem; text-align: center; box-shadow: 0 2px 8px rgba(180,180,200,0.1);">
                                <h4 style="color: #059669; margin: 0; font-size: 1.3rem;">{fact_check_stats['accurate_count']}</h4>
                                <p style="color: #065f46; margin: 0; font-size: 0.85rem;">Accurate</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    
                    with col3:
                        st.markdown(
                            f"""
                            <div style="background: linear-gradient(120deg, #fef3c7 0%, #fffbeb 100%); border-radius: 12px; padding: 1rem; text-align: center; box-shadow: 0 2px 8px rgba(180,180,200,0.1);">
                                <h4 style="color: #d97706; margin: 0; font-size: 1.3rem;">{fact_check_stats['partially_accurate_count']}</h4>
                                <p style="color: #92400e; margin: 0; font-size: 0.85rem;">Partially Accurate</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    
                    with col4:
                        st.markdown(
                            f"""
                            <div style="background: linear-gradient(120deg, #fee2e2 0%, #fef2f2 100%); border-radius: 12px; padding: 1rem; text-align: center; box-shadow: 0 2px 8px rgba(180,180,200,0.1);">
                                <h4 style="color: #dc2626; margin: 0; font-size: 1.3rem;">{fact_check_stats['false_count']}</h4>
                                <p style="color: #991b1b; margin: 0; font-size: 0.85rem;">False</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Display individual fact-checked claims
                    for i, claim_data in enumerate(fact_checked_claims, 1):
                        claim_text = claim_data["claim"]
                        verdict = claim_data["verdict"]
                        justification = claim_data["justification"]
                        confidence = claim_data["confidence"]
                        
                        # Color scheme based on verdict
                        if verdict == "Accurate":
                            color_scheme = {
                                "bg": "#059669", 
                                "shadow": "rgba(5, 150, 105, 0.2)", 
                                "verdict_bg": "#dcfce7",
                                "verdict_color": "#059669",
                                "emoji": "🟢"
                            }
                        elif verdict == "Partially Accurate":
                            color_scheme = {
                                "bg": "#d97706", 
                                "shadow": "rgba(217, 119, 6, 0.2)", 
                                "verdict_bg": "#fef3c7",
                                "verdict_color": "#d97706",
                                "emoji": "🟡"
                            }
                        else:  # False
                            color_scheme = {
                                "bg": "#dc2626", 
                                "shadow": "rgba(220, 38, 38, 0.2)", 
                                "verdict_bg": "#fee2e2",
                                "verdict_color": "#dc2626",
                                "emoji": "🔴"
                            }
                        
                        # Escape HTML content for claims and justification
                        import html
                        escaped_claim = html.escape(claim_text)
                        escaped_justification = html.escape(justification)
                        
                        st.markdown(
                            f"""
                            <div style="background: linear-gradient(120deg, rgba(255, 255, 255, 0.92) 0%, rgba(255,240,245,0.88) 100%); backdrop-filter: blur(15px); border: 1px solid rgba(255,240,245,0.5); border-radius: 16px; padding: 1.4rem; margin-bottom: 1rem; box-shadow: 0 6px 20px {color_scheme['shadow']}; position: relative; border-left: 4px solid {color_scheme['bg']};">
                                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                                    <div style="background: {color_scheme['bg']}; color: white; border-radius: 20px; padding: 0.3rem 0.8rem; font-size: 0.8rem; font-weight: bold;">
                                        Claim #{i}
                                    </div>
                                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                                        <span style="font-size: 0.9rem;">{color_scheme['emoji']}</span>
                                        <div style="background: {color_scheme['verdict_bg']}; color: {color_scheme['verdict_color']}; border-radius: 20px; padding: 0.3rem 0.8rem; font-size: 0.8rem; font-weight: bold;">
                                            {verdict}
                                        </div>
                                    </div>
                                </div>
                                <div style="padding: 0.5rem 0; margin-bottom: 1rem;">
                                    <p style="color: #1a202c; font-size: 1rem; line-height: 1.6; margin: 0; text-align: justify; font-family: 'Inter', 'Segoe UI', sans-serif; font-weight: 500;">
                                        {escaped_claim}
                                    </p>
                                </div>
                                <div style="background: rgba(255, 255, 255, 0.6); border-radius: 8px; padding: 1rem; border: 1px solid rgba(0, 0, 0, 0.05);">
                                    <p style="color: #6b7280; font-size: 0.9rem; line-height: 1.5; margin: 0; font-style: italic; font-family: 'Inter', 'Segoe UI', sans-serif;">
                                        <strong>Justification:</strong> {escaped_justification}
                                    </p>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                else:
                    st.markdown(
                        """
                        <div style="background: linear-gradient(120deg, #fceabb 0%, #f8fafc 100%); border-radius: 16px; padding: 2rem; text-align: center; box-shadow: 0 4px 16px rgba(180,180,200,0.10); border: 1px solid #e3e3e3;">
                            <h3 style="color: #f59e0b; font-size: 1.2rem; margin-bottom: 0.5rem;">No Claims to Fact-Check</h3>
                            <p style="color: #1e293b; font-size: 1rem; margin-bottom: 0;">No claims were extracted from this article for fact-checking.</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                
            except Exception as e:
                st.error(f"Error fact-checking claims: {str(e)}")
                st.markdown(
                    """
                    <div style="background: linear-gradient(120deg, #fee2e2 0%, #fef2f2 100%); border-radius: 16px; padding: 1.5rem; text-align: center; box-shadow: 0 4px 16px rgba(180,180,200,0.10); border: 1px solid #e3e3e3;">
                        <h3 style="color: #ef4444; font-size: 1.2rem; margin-bottom: 0.5rem;">⚠️ Fact-Check Failed</h3>
                        <p style="color: #1e293b; font-size: 1rem; margin-bottom: 0;">Please try again or select a different article.</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            # For non-sample articles or when no pre-computed results available, encourage using Extraction tab
            if article_data.get("source") == "sample":
                # This shouldn't happen if sample articles have mock_analysis, but fallback
                st.warning("⚠️ Sample article is missing fact-check analysis data.")
            else:
                st.info("💡 First run the Extraction tab to extract claims, then return here for fact-checking results.")