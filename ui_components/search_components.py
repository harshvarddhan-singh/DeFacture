"""
Search UI Components for DeFacture Application
============================================

This module contains search-related UI components and functionality
to handle SERP API search, results display, and article selection.
"""

import streamlit as st
from tools.search_api import search_articles_serp, check_serp_api_status, validate_search_query
from ui_components.navigation import show_returning_user_message


def create_search_interface():
    """Create the search interface with API status and input form"""
    st.markdown("### 🔍 Search Articles with SERP API")
    
    # Check SERP API status
    raw_api_status = check_serp_api_status()
    
    # Determine status and show appropriate message
    if raw_api_status.get('serp_api', False):
        st.success("✅ SERP API Ready - API key configured")
        status = 'configured'
    elif raw_api_status.get('mock_available', False):
        st.warning("⚠️ SERP API not configured - using mock data for testing")
        status = 'warning'
    else:
        st.error("❌ No search functionality available")
        status = 'error'
    
    # Create a simplified status dict for compatibility
    api_status = {'status': status}
    
    # Search input form
    search_query = st.text_input(
        "Enter your search query:",
        placeholder="e.g., climate change latest research",
        help="Enter keywords to search for relevant articles"
    )
    
    col1, col2 = st.columns([3, 1])
    with col2:
        search_button = st.button(
            "Search Articles",
            type="primary",
            use_container_width=True,
            disabled=not validate_search_query(search_query),
            key="search_articles_button"  # Add key to avoid button state conflicts
        )
    
    return search_query, search_button, api_status

def display_search_results(search_results: list):
    """Display search results with selection interface"""
    if not search_results:
        st.error("❌ No articles found for your search query")
        return None, None
    
    # Show returning user message if applicable
    show_returning_user_message()
    
    # Enhanced results display
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.05) 0%, rgba(16, 185, 129, 0.02) 100%);
                   border-radius: 10px;
                   padding: 1.5rem;
                   margin: 1.5rem 0;
                   border: 1px solid rgba(16, 185, 129, 0.1);
                   box-shadow: 0 2px 8px rgba(16, 185, 129, 0.08);">
            <h3 style="color: #065f46; font-size: 1.3rem; font-weight: 700; margin-bottom: 1rem;">
                🔍 Search Results - Select an Article
            </h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Create article options for radio button
    article_options = []
    for i, result in enumerate(search_results):
        title_preview = result['title'][:60] + "..." if len(result['title']) > 60 else result['title']
        article_options.append(f"{i+1}. {title_preview} - {result['source']}")
    
    # Radio button selection
    selected_article_idx = st.radio(
        "Choose an article to analyze:",
        range(len(article_options)),
        format_func=lambda x: article_options[x],
        key="selected_search_article"
    )
    
    if selected_article_idx is not None:
        selected_result = search_results[selected_article_idx]
        show_article_preview(selected_result)
        
        # Add prominent fetch button
        st.markdown("**Step 1: Fetch Article Content**")
        fetch_button = st.button(
            "🔍 Fetch from Search",
            type="primary",
            use_container_width=True,
            help="Click to fetch the selected article content",
            key="fetch_search_button"  # Unique key for search handler
        )
        
        return selected_result, fetch_button
    
    return None, None

def show_article_preview(article_result: dict):
    """Show preview of selected search result"""
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(16, 185, 129, 0.05) 100%);
                   border-radius: 12px;
                   padding: 1.5rem;
                   margin: 1rem 0;
                   border-left: 4px solid #10b981;
                   box-shadow: 0 4px 12px rgba(16, 185, 129, 0.1);">
            <h4 style="color: #065f46; font-size: 1.2rem; font-weight: 700; margin-bottom: 0.75rem;">
                📰 {article_result['title']}
            </h4>
            <div style="margin-bottom: 0.5rem;">
                <span style="background: #10b981; color: white; padding: 0.2rem 0.6rem; border-radius: 15px; font-size: 0.85rem; font-weight: 600; margin-right: 0.5rem;">
                    📡 {article_result['source']}
                </span>
                {f'<span style="background: #6b7280; color: white; padding: 0.2rem 0.6rem; border-radius: 15px; font-size: 0.85rem; font-weight: 600; margin-right: 0.5rem;">📅 {article_result["date"]}</span>' if article_result.get('date') else ''}
                <span style="background: #3b82f6; color: white; padding: 0.2rem 0.6rem; border-radius: 15px; font-size: 0.85rem; font-weight: 600;">
                    🌐 {article_result.get('domain', 'N/A')}
                </span>
            </div>
            <p style="color: #374151; font-size: 1rem; line-height: 1.6; margin: 0.75rem 0;">
                <strong>Summary:</strong> {article_result['snippet']}
            </p>
            <div style="margin-top: 1rem; padding-top: 0.75rem; border-top: 1px solid rgba(16, 185, 129, 0.2);">
                <a href="{article_result['link']}" target="_blank" style="color: #10b981; text-decoration: none; font-weight: 600;">
                    🔗 View Original Article
                </a>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def handle_search_process(search_query: str, api_status: dict):
    """Handle the search process and return results"""
    if api_status['status'] != 'configured':
        # Show mock results with warning
        st.warning("🔧 Using mock search results due to API configuration issue")
        mock_results = [
            {
                'title': f'Mock Result: {search_query.title()}',
                'snippet': f'This is a mock search result for "{search_query}". Configure your SERP API key for real results.',
                'link': 'https://example.com/mock-article',
                'source': 'Mock Source',
                'date': '2024-01-15',
                'domain': 'example.com'
            }
        ]
        return mock_results
    else:
        # Perform actual search
        with st.spinner("🔍 Searching for articles..."):
            try:
                results = search_articles_serp(search_query)
                if results.get('status') == 'success':
                    search_results = results.get('articles', [])
                    st.success(f"✅ Found {len(search_results)} articles")
                    return search_results
                else:
                    st.error(f"❌ Search failed: {results.get('message', 'Unknown error')}")
                    return []
            except Exception as e:
                st.error(f"❌ Search error: {str(e)}")
                return []

def create_new_search_button():
    """Create a button to start a new search"""
    if st.button("🔄 New Search", use_container_width=False):
        # Clear search-related session state
        search_keys = ['search_results', 'last_search_query', 'selected_search_article']
        for key in search_keys:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()