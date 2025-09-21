"""
Navigation Components for DeFacture Application
==============================================

This module contains navigation-related UI components and utilities
to manage workflow navigation between different modes of the application.

Components:
- Workflow breadcrumbs
- Back navigation buttons
- Navigation state management
- Navigation-related UI elements
"""

import streamlit as st
from typing import Dict, Any, Optional, List


def show_workflow_breadcrumbs(current_step: str = "search", article_title: Optional[str] = None) -> None:
    """
    Simple function that does nothing - breadcrumbs removed per user request.
    Only keeping the "Start New Search" button functionality.
    
    Args:
        current_step: Current workflow step (ignored)
        article_title: Title of selected article (ignored)
    """
    # Function exists but does nothing - user wants only the "Start New Search" button
    pass


def show_back_to_search_button(button_key: str = "back_to_search") -> bool:
    """
    Display a prominent 'Start New Search' button that completely resets the application.
    
    Args:
        button_key: Unique key for the button component
        
    Returns:
        bool: True if button was clicked, False otherwise
    """
    
    # Create prominent reset button
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Create the button with clear messaging
        back_clicked = st.button(
            "� Start New Search",
            key=button_key,
            help="Clear all data and return to the beginning",
            use_container_width=True,
            type="secondary"
        )
        
        if back_clicked:
            st.info("🔄 Clearing all data and returning to search...")
    
    # Add custom CSS for the reset button
    st.markdown(
        """
        <style>
        .stButton > button {
            background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.75rem 2rem !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            box-shadow: 0 3px 10px rgba(220, 38, 38, 0.3) !important;
            transition: all 0.3s ease !important;
            margin: 0.5rem 0 !important;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #b91c1c 0%, #7f1d1d 100%) !important;
            box-shadow: 0 5px 15px rgba(220, 38, 38, 0.4) !important;
            transform: translateY(-1px) !important;
        }
        
        .stButton > button:active {
            transform: translateY(0px) !important;
            box-shadow: 0 2px 8px rgba(220, 38, 38, 0.4) !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    return back_clicked


def clear_analysis_mode() -> None:
    """
    Clear analysis mode and return to search interface.
    Completely resets all session state to start fresh.
    """
    
    # Clear ALL session state keys to start completely fresh
    keys_to_clear = [
        'analysis_mode',
        'article_data',
        'temp_article_data',
        'selected_article_url',
        'selected_article_title',
        'analysis_results',
        'current_analysis_step',
        'search_results',
        'last_search_query',
        'selected_search_article',
        'dataset_results',
        'current_workflow_step',
        # Additional keys that might persist
        'use_langchain_toggle',
        'navigation_css_injected',
        'font_awesome_injected',
        'back_button_css_added',
        # Any other potential keys
        'selected_result',
        'analyze_selected'
    ]
    
    # Alternative approach: Clear ALL session state except essential Streamlit keys
    keys_to_keep = [
        'FormSubmitter:article_input-Submit',
        'FormSubmitter:search_form-Search',
        'widget_key',
        'button_key'
    ]
    
    # Get all current session state keys
    all_keys = list(st.session_state.keys())
    
    # Clear everything except essential Streamlit widget keys
    for key in all_keys:
        if not any(keep_key in key for keep_key in keys_to_keep):
            try:
                del st.session_state[key]
            except KeyError:
                pass  # Key already deleted or doesn't exist
    
    # Ensure we're not in analysis mode
    st.session_state.analysis_mode = False
    
    # Reset to search step
    st.session_state.current_workflow_step = 'search'
    
    # Force a complete rerun to refresh the interface
    st.rerun()
    
    # Rerun to refresh the interface
    st.rerun()


def check_returning_from_analysis() -> bool:
    """
    Check if user is returning from analysis mode to search interface.
    
    Returns:
        bool: True if user is returning from analysis, False otherwise
    """
    
    return (hasattr(st.session_state, 'analysis_mode') and 
            not st.session_state.analysis_mode and 
            hasattr(st.session_state, 'article_analysis_data'))


def show_returning_user_message() -> None:
    """
    Show a helpful message for users returning from analysis mode.
    """
    
    if check_returning_from_analysis():
        st.info("🔄 Welcome back! Your previous search results are preserved below. You can select a different article to analyze or perform a new search above.")


def get_navigation_state() -> Dict[str, Any]:
    """
    Get current navigation state information.
    
    Returns:
        dict: Navigation state information
    """
    
    return {
        'is_in_analysis_mode': getattr(st.session_state, 'analysis_mode', False),
        'has_search_results': hasattr(st.session_state, 'search_results') and bool(st.session_state.search_results),
        'has_analysis_data': hasattr(st.session_state, 'article_analysis_data'),
        'is_returning_from_analysis': check_returning_from_analysis(),
        'current_article_title': getattr(st.session_state, 'selected_article_title', None),
        'search_results_count': len(getattr(st.session_state, 'search_results', []))
    }


def show_navigation_help() -> None:
    """
    Display navigation help information for users.
    """
    
    with st.expander("🧭 Navigation Help", expanded=False):
        st.markdown(
            """
            ### How to Navigate DeFacture
            
            **🔍 Search Mode:**
            - Enter your search query to find relevant articles
            - Use the SERP API for comprehensive search results
            - Preview and select articles from the results
            
            **👁️ Preview Mode:**
            - Review article details before analysis
            - Check source credibility and publication date
            - Confirm your selection before proceeding
            
            **🔬 Analysis Mode:**
            - View comprehensive fact-checking results
            - Explore extracted claims and verdicts
            - Use 'Back to Search' to return and analyze other articles
            
            **💡 Tips:**
            - Your search results are preserved when navigating back
            - You can analyze multiple articles from the same search
            - Use workflow breadcrumbs to track your progress
            """
        )


def handle_navigation_action(action: str, **kwargs) -> None:
    """
    Handle different navigation actions.
    
    Args:
        action: Navigation action to perform
        **kwargs: Additional parameters for the action
    """
    
    if action == "back_to_search":
        clear_analysis_mode()
    elif action == "start_analysis":
        st.session_state.analysis_mode = True
        if 'article_url' in kwargs:
            st.session_state.selected_article_url = kwargs['article_url']
        if 'article_title' in kwargs:
            st.session_state.selected_article_title = kwargs['article_title']
        st.rerun()
    elif action == "clear_search":
        search_keys = ['search_results', 'last_search_query', 'selected_search_article']
        for key in search_keys:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
    elif action == "show_help":
        show_navigation_help()


# Utility functions for workflow management
def set_workflow_step(step: str) -> None:
    """Set current workflow step in session state."""
    st.session_state.current_workflow_step = step


def get_workflow_step() -> str:
    """Get current workflow step from session state."""
    return getattr(st.session_state, 'current_workflow_step', 'search')


def is_analysis_mode() -> bool:
    """Check if currently in analysis mode."""
    return getattr(st.session_state, 'analysis_mode', False)


def has_search_results() -> bool:
    """Check if search results are available."""
    return hasattr(st.session_state, 'search_results') and bool(st.session_state.search_results)


# CSS Styles for navigation components
NAVIGATION_CSS = """
<style>
/* Navigation breadcrumbs styling */
.nav-breadcrumb {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.95) 100%);
    border-radius: 12px;
    padding: 1rem;
    margin: 1rem 0;
    border: 1px solid rgba(203, 213, 225, 0.5);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

/* Back button enhanced styling */
.nav-back-button {
    background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1.5rem;
    font-weight: 600;
    font-size: 0.95rem;
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
    transition: all 0.3s ease;
    cursor: pointer;
}

.nav-back-button:hover {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    transform: translateY(-1px);
}

/* Navigation state indicators */
.nav-active-step {
    color: #1e40af;
    background: rgba(59, 130, 246, 0.1);
    font-weight: 700;
}

.nav-completed-step {
    color: #059669;
    background: rgba(16, 185, 129, 0.1);
    font-weight: 600;
}

.nav-pending-step {
    color: #6b7280;
    background: rgba(107, 114, 128, 0.1);
    font-weight: 500;
}
</style>
"""


def inject_navigation_css() -> None:
    """Inject navigation-related CSS styles."""
    if 'navigation_css_injected' not in st.session_state:
        st.markdown(NAVIGATION_CSS, unsafe_allow_html=True)
        st.session_state.navigation_css_injected = True