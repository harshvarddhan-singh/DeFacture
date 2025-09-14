"""
History page for DeFacture

This page displays the history of previously analyzed articles.
"""

import streamlit as st
from datetime import datetime, timedelta

def main():
    st.title("Analysis History")
    st.markdown("View and revisit previously analyzed articles")
    
    # Placeholder for history data
    # This would be loaded from a database or file in a real application
    history_data = [
        {
            "title": "Example Article 1",
            "source": "News Source A",
            "date_analyzed": datetime.now() - timedelta(days=2),
            "summary": "This is a summary of the article...",
        },
        {
            "title": "Example Article 2",
            "source": "News Source B",
            "date_analyzed": datetime.now() - timedelta(days=5),
            "summary": "This is a summary of another article...",
        }
    ]
    
    # Display history entries
    for i, entry in enumerate(history_data):
        with st.expander(f"{entry['title']} - {entry['source']}"):
            st.write(f"**Analyzed on:** {entry['date_analyzed'].strftime('%Y-%m-%d %H:%M')}")
            st.write(f"**Summary:** {entry['summary']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.button("View Full Analysis", key=f"view_{i}")
            with col2:
                st.button("Delete from History", key=f"delete_{i}")
            
    # Placeholder for empty state
    if not history_data:
        st.info("No analysis history found. Start by analyzing an article on the home page.")

# Run the app
if __name__ == "__main__":
    main()