"""
Article fetcher using newspaper3k

This module contains functions for fetching articles from URLs using newspaper3k library.
"""

from newspaper import Article
import streamlit as st

def fetch_article_with_newspaper(url: str) -> dict:
    """
    Fetches article using newspaper3k.
    Returns dict with title, authors, publish_date, and content.
    """
    try:
        article = Article(url)
        article.download()
        article.parse()

        return {
            "source": "url",
            "title": article.title,
            "content": article.text,
            "authors": article.authors,
            "publish_date": article.publish_date
        }
    except Exception as e:
        st.warning(f"⚠️ Could not fetch article: {e}")
        return None