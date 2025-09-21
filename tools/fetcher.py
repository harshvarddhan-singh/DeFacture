"""
Article fetcher using newspaper3k

This module contains functions for fetching articles from URLs using newspaper3k library.
"""

from newspaper import Article
import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

def fetch_article_with_newspaper(url: str) -> dict:
    """
    Fetches article using newspaper3k.
    Returns dict with success flag, title, authors, publish_date, and content.
    """
    try:
        article = Article(url)
        article.download()
        article.parse()
        
        # Extract domain from URL
        from urllib.parse import urlparse
        domain = urlparse(url).netloc

        # Clean and validate content
        content = article.text.strip() if article.text else ""
        
        # Basic content validation - check if we got meaningful content
        if len(content) < 50:
            # Try fallback method
            fallback_result = fetch_article_fallback(url)
            if fallback_result["success"]:
                return fallback_result
            
            return {
                "success": False,
                "error": f"Article content too short ({len(content)} characters). This might be due to paywall or extraction issues.",
                "title": article.title,
                "content": content,
                "authors": article.authors,
                "publish_date": article.publish_date,
                "domain": domain
            }
        
        # Check for common extraction issues (navigation menus, etc.)
        problematic_phrases = [
            "see all topics follow",
            "subscribe now",
            "menu items",
            "navigation",
            "social media",
            "follow us"
        ]
        
        content_lower = content.lower()
        if any(phrase in content_lower for phrase in problematic_phrases) and len(content) < 200:
            # Try fallback method
            fallback_result = fetch_article_fallback(url)
            if fallback_result["success"]:
                return fallback_result
            
            return {
                "success": False,
                "error": "Extracted content appears to contain navigation elements rather than article text. The website might use dynamic loading or have anti-scraping measures.",
                "title": article.title,
                "content": content,
                "authors": article.authors,
                "publish_date": article.publish_date,
                "domain": domain
            }

        return {
            "success": True,
            "source": "url",
            "title": article.title,
            "content": content,
            "authors": article.authors,
            "publish_date": article.publish_date,
            "domain": domain
        }
    except Exception as e:
        # Try fallback method
        fallback_result = fetch_article_fallback(url)
        if fallback_result["success"]:
            return fallback_result
            
        return {
            "success": False,
            "error": str(e),
            "title": None,
            "content": None,
            "authors": [],
            "publish_date": None,
            "domain": None
        }

def fetch_article_fallback(url: str) -> dict:
    """
    Fallback method using requests and BeautifulSoup for basic content extraction
    """
    try:
        # Extract domain from URL
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try to extract title
        title = None
        title_selectors = ['h1', 'title', '.article-title', '.post-title', '.entry-title']
        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                title = title_elem.get_text().strip()
                break
        
        # Try to extract article content
        content = ""
        content_selectors = [
            '.article-content', '.post-content', '.entry-content', 
            '.article-body', '.story-body', '.content', 
            'article', '.main-content', '.post-body'
        ]
        
        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                # Remove script and style elements
                for script in content_elem(["script", "style"]):
                    script.extract()
                content = content_elem.get_text()
                break
        
        # If no content found with selectors, try paragraphs
        if not content:
            paragraphs = soup.find_all('p')
            if len(paragraphs) > 3:  # Likely an article if has multiple paragraphs
                content = '\n'.join([p.get_text().strip() for p in paragraphs[:10]])  # First 10 paragraphs
        
        # Clean content
        content = re.sub(r'\s+', ' ', content).strip()
        
        if len(content) > 100:  # Good enough content
            return {
                "success": True,
                "source": "url",
                "title": title or "Article from " + domain,
                "content": content,
                "authors": [],
                "publish_date": None,
                "domain": domain
            }
        else:
            return {
                "success": False,
                "error": "Fallback extraction also failed to get meaningful content",
                "title": title,
                "content": content,
                "authors": [],
                "publish_date": None,
                "domain": domain
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Fallback extraction failed: {str(e)}",
            "title": None,
            "content": None,
            "authors": [],
            "publish_date": None,
            "domain": None
        }

def fetch_article_with_newspaper(url: str) -> dict:
    """
    Fetches article using newspaper3k.
    Returns dict with success flag, title, authors, publish_date, and content.
    """
    try:
        article = Article(url)
        article.download()
        article.parse()
        
        # Extract domain from URL
        from urllib.parse import urlparse
        domain = urlparse(url).netloc

        # Clean and validate content
        content = article.text.strip() if article.text else ""
        
        # Basic content validation - check if we got meaningful content
        if len(content) < 50:
            return {
                "success": False,
                "error": f"Article content too short ({len(content)} characters). This might be due to paywall or extraction issues.",
                "title": article.title,
                "content": content,
                "authors": article.authors,
                "publish_date": article.publish_date,
                "domain": domain
            }
        
        # Check for common extraction issues (navigation menus, etc.)
        problematic_phrases = [
            "see all topics follow",
            "subscribe now",
            "menu items",
            "navigation",
            "social media",
            "follow us"
        ]
        
        content_lower = content.lower()
        if any(phrase in content_lower for phrase in problematic_phrases) and len(content) < 200:
            return {
                "success": False,
                "error": "Extracted content appears to contain navigation elements rather than article text. The website might use dynamic loading or have anti-scraping measures.",
                "title": article.title,
                "content": content,
                "authors": article.authors,
                "publish_date": article.publish_date,
                "domain": domain
            }

        return {
            "success": True,
            "source": "url",
            "title": article.title,
            "content": content,
            "authors": article.authors,
            "publish_date": article.publish_date,
            "domain": domain
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "title": None,
            "content": None,
            "authors": [],
            "publish_date": None,
            "domain": None
        }