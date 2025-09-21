"""
Article Input Interface - Main Controller
========================================

This is the main interface controller that coordinates between different UI components
to provide a clean and organized article input experience.
"""

import streamlit as st
from tools.fetcher import fetch_article_with_newspaper
from ui_components.navigation import (
    show_workflow_breadcrumbs, 
    show_back_to_search_button, 
    clear_analysis_mode,
    show_returning_user_message,
    inject_navigation_css
)
from ui_components.ui_helpers import (
    show_main_header,
    create_method_tabs,
    show_method_description,
    create_url_input_form,
    create_sample_selector,
    create_dataset_uploader,
    show_article_preview_card,
    show_analysis_start_button,
    SAMPLE_ARTICLES
)
from ui_components.search_components import (
    create_search_interface,
    display_search_results,
    handle_search_process
)
from ui_components.dataset_components import (
    create_sample_dataset,
    handle_dataset_upload,
    process_dataset_batch,
    create_article_selector
)


def show_analysis_header(article_data):
    """
    Show a header with article info and back to search navigation when in analysis mode
    Uses the new navigation module for consistent UI components.
    """
    # Inject navigation CSS styles
    inject_navigation_css()
    
    # Show workflow breadcrumbs
    article_title = article_data.get('title', 'Untitled Article')
    show_workflow_breadcrumbs('analysis', article_title)
    
    # Show back to search button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if show_back_to_search_button("analysis_back_button"):
            clear_analysis_mode()
    
    # Article info card with enhanced styling
    source_emoji = {
        "sample": "🧪",
        "url": "🌐", 
        "search_result": "🔍",
        "uploaded_dataset": "📂"
    }.get(article_data.get("source", ""), "📄")
    
    original_source = article_data.get("original_source", article_data.get("source", "Unknown"))
    
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(16, 185, 129, 0.05) 100%);
                   border-radius: 12px;
                   padding: 1.5rem;
                   margin: 1rem 0 2rem 0;
                   border-left: 4px solid #10b981;
                   box-shadow: 0 4px 12px rgba(16, 185, 129, 0.1);">
            <h4 style="color: #065f46; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem;">
                {source_emoji} Currently Analyzing
            </h4>
            <h3 style="color: #1f2937; font-size: 1.25rem; font-weight: 600; margin-bottom: 0.5rem; line-height: 1.3;">
                {article_title}
            </h3>
            <p style="color: #6b7280; font-size: 0.9rem; margin: 0;">
                <strong>Source:</strong> {original_source} | 
                <strong>Content:</strong> {len(article_data.get('content', '')):,} characters
                {f" | <strong>URL:</strong> {article_data.get('domain', 'N/A')}" if article_data.get('domain') else ""}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


def handle_url_input(url_input):
    """Handle URL input and fetch article content"""
    # Check if URL is blank or empty
    if not url_input or not url_input.strip():
        st.warning("⚠️ Please enter an article URL before clicking Fetch Article")
        return None
    
    # Check if URL format is valid
    if not url_input.startswith(('http://', 'https://')):
        st.error("❌ Please enter a valid URL starting with http:// or https://")
        return None
    
    with st.spinner("🌐 Fetching article content..."):
        try:
            result = fetch_article_with_newspaper(url_input)
            if result and result.get('success', False):
                article_data = {
                    'title': result['title'],
                    'content': result['content'], 
                    'url': url_input,
                    'source': 'url',
                    'domain': result.get('domain', 'Unknown'),
                    'author': result.get('author', 'Unknown Author'),
                    'published_date': result.get('publish_date', 'Unknown Date'),
                    'original_source': result.get('domain', 'URL Source')
                }
                st.success("✅ Article fetched successfully!")
                return article_data
            else:
                error_msg = result.get('error', 'Unknown error') if result else 'Failed to fetch article'
                st.error(f"❌ Failed to fetch article: {error_msg}")
                
                # Show additional help for common issues
                if result and "extraction" in error_msg.lower():
                    st.info("""
                    💡 **Common extraction issues:**
                    - The website might have anti-scraping measures
                    - Content might be loaded dynamically with JavaScript
                    - The article might be behind a paywall
                    - Try a different news article URL
                    """)
                elif result and "short" in error_msg.lower():
                    st.info("""
                    💡 **Content too short:**
                    - The URL might not point to a full article
                    - Try copying the direct article URL from the address bar
                    - Ensure the URL leads to the main article content
                    """)
                
                return None
        except Exception as e:
            st.error(f"❌ Error fetching article: {str(e)}")
            return None


def handle_sample_selection(selected_sample):
    """Handle sample article selection with validation and full details"""
    # Check if no sample is selected
    if selected_sample is None:
        st.warning("⚠️ Please select a sample article from the dropdown before clicking Fetch Sample")
        return None
    
    # Get the selected sample and create full article data
    sample = SAMPLE_ARTICLES[selected_sample]
    
    # Show success message and create article data with full details
    st.success("✅ Sample article fetched successfully!")
    
    article_data = {
        'title': sample.get('title', 'Untitled Sample Article'),
        'content': sample.get('content', 'No content available'),
        'source': 'sample',
        'domain': sample.get('domain', 'Sample Source'),
        'original_source': f"Sample Article #{selected_sample + 1}",
        'published_date': sample.get('published_date', 'Sample Date'),
        'author': sample.get('author', 'Sample Author'),
        'content_preview': sample['content'][:200] + "..." if len(sample['content']) > 200 else sample['content']
    }
    return article_data


def handle_search_workflow():
    """Handle the complete search workflow"""
    search_query, search_button, api_status = create_search_interface()
    
    # Perform search if button clicked
    if search_button:
        # We already have validation in handle_search_process
        search_results = handle_search_process(search_query, api_status)
        if search_results:
            st.session_state.search_results = search_results
            st.session_state.last_search_query = search_query
            # Don't rerun here - let the results show immediately
    
    # Display existing search results
    if hasattr(st.session_state, 'search_results') and st.session_state.search_results:
        selected_result, fetch_selected = display_search_results(st.session_state.search_results)
        
        if fetch_selected and selected_result:
            # Fetch article content from selected search result
            with st.spinner("📰 Fetching article content..."):
                try:
                    # Get the URL from either 'link' or 'url' field
                    article_url = selected_result.get('link', selected_result.get('url', None))
                    
                    if not article_url:
                        st.error("❌ Error: No URL found in search result")
                        return None
                    
                    result = fetch_article_with_newspaper(article_url)
                    if result and result.get('success', False):
                        article_data = {
                            'title': result['title'] or selected_result['title'],
                            'content': result['content'],
                            'url': article_url,
                            'source': 'search_result',
                            'original_source': selected_result['source'],
                            'domain': result.get('domain') or selected_result.get('domain', 'Unknown'),
                            'author': result.get('author', 'Unknown Author'),
                            'published_date': result.get('publish_date', 'Unknown Date')
                        }
                        return article_data
                    else:
                        error_msg = result.get('error', 'Unknown error') if result else 'Failed to fetch article'
                        st.error(f"❌ Failed to fetch article content: {error_msg}")
                except Exception as e:
                    st.error(f"❌ Error fetching article: {str(e)}")
    
    return None


def handle_dataset_workflow():
    """Handle the complete dataset workflow"""
    uploaded_file, process_button, download_sample = create_dataset_uploader()
    
    # Handle sample dataset download
    if download_sample:
        sample_data = create_sample_dataset()
        st.download_button(
            label="📥 Download Sample Dataset",
            data=sample_data,
            file_name="sample_dataset.json",
            mime="application/json"
        )
    
    # Handle dataset processing
    if uploaded_file and process_button:
        articles, filename = handle_dataset_upload(uploaded_file)
        if articles:
            result = process_dataset_batch(articles, filename)
            if result:
                if result['analyze_all']:
                    # Return first article for immediate analysis
                    # In a real implementation, you'd handle batch processing
                    first_article = articles[0]
                    article_data = {
                        'title': first_article.get('title', 'Dataset Article'),
                        'content': first_article.get('content', ''),
                        'source': 'uploaded_dataset',
                        'domain': first_article.get('source', filename),
                        'author': first_article.get('author', 'Dataset Author'),
                        'published_date': first_article.get('date', 'Dataset Date'),
                        'original_source': f"Dataset: {filename}",
                        'batch_mode': True,
                        'total_articles': len(articles)
                    }
                    return article_data
                elif result['select_articles']:
                    selected_articles, fetch_selected = create_article_selector(articles)
                    if fetch_selected and selected_articles:
                        # Return first selected article
                        first_selected = selected_articles[0]
                        article_data = {
                            'title': first_selected.get('title', 'Selected Article'),
                            'content': first_selected.get('content', ''),
                            'source': 'uploaded_dataset',
                            'domain': first_selected.get('source', 'Dataset'),
                            'author': first_selected.get('author', 'Dataset Author'),
                            'published_date': first_selected.get('date', 'Dataset Date'),
                            'original_source': f"Selected from Dataset ({len(selected_articles)} articles)",
                            'selected_count': len(selected_articles)
                        }
                        return article_data
    
    return None


def render_article_input():
    """Main render function - now much cleaner and organized!"""
    
    # Check if we're in analysis mode - must have both article_data AND analysis_mode=True
    if (hasattr(st.session_state, 'article_data') and 
        st.session_state.article_data and 
        hasattr(st.session_state, 'analysis_mode') and
        st.session_state.analysis_mode is True):
        show_analysis_header(st.session_state.article_data)
        return st.session_state.article_data
    
    # Show main header
    show_main_header()
    
    # Create method tabs
    tab_sample, tab_url, tab_search, tab_dataset = create_method_tabs()
    
    # Initialize article_data
    article_data = None
    
    # Handle each tab - avoid st.rerun() to preserve tab state
    with tab_sample:
        show_method_description('sample')
        selected_sample, fetch_sample_button = create_sample_selector()
        
        if fetch_sample_button:
            article_data = handle_sample_selection(selected_sample)
            if article_data:
                st.session_state.temp_article_data = article_data
                # Don't call st.rerun() - let it continue in same execution
    
    with tab_url:
        show_method_description('url')
        url_input, fetch_button = create_url_input_form()
        
        if fetch_button:
            article_data = handle_url_input(url_input)
            if article_data:
                st.session_state.temp_article_data = article_data
                # Don't call st.rerun() - let it continue in same execution
    
    with tab_search:
        show_method_description('search')
        search_article_data = handle_search_workflow()
        if search_article_data:
            article_data = search_article_data
            st.session_state.temp_article_data = article_data
            # Don't call st.rerun() - let it continue in same execution
    
    with tab_dataset:
        show_method_description('dataset')
        dataset_article_data = handle_dataset_workflow()
        if dataset_article_data:
            article_data = dataset_article_data
            st.session_state.temp_article_data = article_data
            # Don't call st.rerun() - let it continue in same execution
    
    # Check for temporarily stored article data
    if hasattr(st.session_state, 'temp_article_data') and st.session_state.temp_article_data:
        article_data = st.session_state.temp_article_data
    
    # Always show the three main action buttons
    st.write("")  # Add some spacing
    st.markdown("---")  # Add separator
    
    # Show the three main action buttons in a clear layout
    st.markdown("### 🎯 Three-Step Process")
    
    # Create three columns for the main action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Step 1: Fetch Article** 📰")
        st.info("💡 Use any tab above to fetch content:\n\n• **Sample**: Select + **Fetch Sample Article**\n• **URL**: Enter URL + **Fetch from URL**\n• **Search**: Search + Select + **Fetch from Search**\n• **Dataset**: Upload + Select + **Fetch from Dataset**")
    
    with col2:
        st.markdown("**Step 2: Start Analysis** 🚀")
        if st.button(
            "🚀 Start Fact Check Analysis",
            type="primary",
            use_container_width=True,
            help="Begin comprehensive fact-checking analysis of the article",
            key="start_analysis_button"  # Add key to avoid button state conflicts
        ):
            # Check if we have article data to analyze
            if not article_data and not (hasattr(st.session_state, 'temp_article_data') and st.session_state.temp_article_data):
                st.error("⚠️ Please fetch an article first before starting fact-check analysis!")
                st.info("💡 Complete Step 1 by fetching article content from any of the tabs above")
            else:
                # Use article data (either current or temporary)
                analysis_article = article_data or st.session_state.temp_article_data
                
                # Store article data and switch to analysis mode
                st.session_state.article_data = analysis_article
                st.session_state.analysis_mode = True
                # Clear temporary data
                if hasattr(st.session_state, 'temp_article_data'):
                    del st.session_state.temp_article_data
                st.rerun()
    
    with col3:
        st.markdown("**Step 3: Start Over** 🔄")
        from ui_components.navigation import clear_analysis_mode
        if st.button(
            "🔄 Start New Search",
            type="secondary",
            use_container_width=True,
            help="Clear all data and start fresh",
            key="start_new_search_button"  # Add key to avoid button state conflicts
        ):
            clear_analysis_mode()
            st.rerun()
    
    # If we have article data, show preview (but analysis button is already shown above)
    if article_data:
        # Show navigation breadcrumbs for article preview stage
        from .navigation import show_workflow_breadcrumbs, show_back_to_search_button
        
        # Inject navigation CSS for styling
        inject_navigation_css()
        
        # Show workflow breadcrumbs (preview stage)
        article_title = article_data.get('title', 'Article Preview')
        show_workflow_breadcrumbs('preview', article_title)
        
        # Show back to search button
        if show_back_to_search_button():
            st.rerun()
        
        st.write("")  # Add some spacing
        
        show_article_preview_card(article_data)
    
    return article_data