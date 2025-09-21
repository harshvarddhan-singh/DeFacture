"""
SERP API search tools for DeFacture

This module contains functions for searching articles using SERP APIs:
- Search via SerpAPI or Google Search API
- Mock search functionality for demo
- Article URL extraction from search results
"""

import os
import requests
import logging
from typing import List, Dict, Optional
from urllib.parse import urlparse
from config.config import API_KEYS

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_domain_from_url(url: str) -> str:
    """Extract domain name from URL"""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain
    except:
        return ""

def search_articles_serp(query: str, num_results: int = 5) -> List[Dict]:
    """
    Search for articles using SERP API (Google News engine) with detailed error handling
    
    Parameters:
    -----------
    query : str
        The search query
    num_results : int
        Number of results to return (default: 5)
        
    Returns:
    --------
    List[Dict]
        List of search results with title, url, snippet, source, date and error context
    """
    serp_api_key = API_KEYS.get("serp_api", "").strip()
    
    # Check if API key is missing
    if not serp_api_key:
        logger.warning("SERP API key not found in configuration")
        return mock_search_results(query, num_results, 
                                 error="no_api_key",
                                 message="No SERP API key configured. Add your API key to the .env file to use real search results.")
    
    # Basic API key validation
    if len(serp_api_key) < 20:
        logger.warning(f"SERP API key appears invalid (length: {len(serp_api_key)})")
        return mock_search_results(query, num_results, 
                                 error="invalid_api_key",
                                 message="SERP API key appears to be invalid or incomplete. Please check your API key format.")

    try:
        # SerpAPI Google News search with enhanced parameters
        url = "https://serpapi.com/search"
        params = {
            "engine": "google",
            "q": query,
            "api_key": serp_api_key,
            "num": num_results,
            "tbm": "nws",  # News search
            "tbs": "qdr:w",  # Recent articles (past week)
            "hl": "en",  # Language
            "gl": "us",  # Country
            "safe": "active"
        }
        
        logger.info(f"Searching SERP API for: '{query}'")
        response = requests.get(url, params=params, timeout=15)
        
        # Handle different HTTP status codes
        if response.status_code == 401:
            logger.error("SERP API authentication failed - invalid API key")
            return mock_search_results(query, num_results, 
                                     error="auth_failed",
                                     message="SERP API authentication failed. Your API key is invalid or expired.")
        
        if response.status_code == 429:
            logger.error("SERP API rate limit exceeded")
            return mock_search_results(query, num_results, 
                                     error="rate_limit",
                                     message="SERP API rate limit exceeded. Please wait a moment and try again.")
        
        if response.status_code == 400:
            logger.error("SERP API bad request - invalid parameters")
            return mock_search_results(query, num_results, 
                                     error="bad_request",
                                     message="SERP API request failed due to invalid parameters.")
        
        if response.status_code != 200:
            logger.error(f"SERP API request failed with status: {response.status_code}")
            return mock_search_results(query, num_results, 
                                     error="api_error",
                                     message=f"SERP API request failed with status {response.status_code}.")
        
        # Parse JSON response
        try:
            data = response.json()
        except ValueError as e:
            logger.error(f"Failed to parse SERP API response: {e}")
            return mock_search_results(query, num_results, 
                                     error="parse_error",
                                     message="SERP API returned an invalid response format.")
        
        # Check for API errors in response
        if "error" in data:
            error_msg = data["error"]
            logger.error(f"SERP API returned error: {error_msg}")
            return mock_search_results(query, num_results, 
                                     error="api_response_error",
                                     message=f"SERP API error: {error_msg}")
        
        results = []
        news_results = data.get("news_results", [])
        
        if not news_results:
            logger.warning("SERP API returned no news results")
            return mock_search_results(query, num_results, 
                                     error="no_results",
                                     message="SERP API found no news results for your search query. Try different keywords.")
        
        for item in news_results[:num_results]:
            try:
                # Extract enhanced metadata
                result = {
                    "title": item.get("title", "").strip(),
                    "url": item.get("link", ""),
                    "snippet": item.get("snippet", "").strip(),
                    "source": item.get("source", "").strip(),
                    "date": item.get("date", ""),
                    "position": item.get("position", 0),
                    "thumbnail": item.get("thumbnail", ""),
                    # Additional metadata
                    "domain": extract_domain_from_url(item.get("link", "")),
                    "api_source": "serp_api",
                    "error_type": None,
                    "error_message": None
                }
                
                # Clean up the result
                if not result["snippet"] and "snippet" in item:
                    result["snippet"] = item.get("snippet", "")[:200] + "..."
                    
                results.append(result)
                
            except Exception as e:
                logger.warning(f"Error processing SERP result: {e}")
                continue
        
        if not results:
            logger.warning("No valid results after processing SERP API response")
            return mock_search_results(query, num_results, 
                                     error="processing_failed",
                                     message="SERP API results could not be processed properly.")
        
        logger.info(f"SERP API returned {len(results)} news articles")
        return results
        
    except requests.exceptions.Timeout:
        logger.error("SERP API request timed out")
        return mock_search_results(query, num_results, 
                                 error="timeout",
                                 message="SERP API request timed out. Please check your internet connection and try again.")
    except requests.exceptions.ConnectionError:
        logger.error("Failed to connect to SERP API")
        return mock_search_results(query, num_results, 
                                 error="connection_error",
                                 message="Cannot connect to SERP API. Please check your internet connection.")
    except requests.exceptions.RequestException as e:
        logger.error(f"SERP API request failed: {e}")
        return mock_search_results(query, num_results, 
                                 error="request_failed",
                                 message=f"SERP API request failed: {str(e)}")
    except Exception as e:
        logger.error(f"SERP API search failed unexpectedly: {e}")
        return mock_search_results(query, num_results, 
                                 error="unexpected_error",
                                 message=f"An unexpected error occurred: {str(e)}")

def search_articles_google(query: str, num_results: int = 5) -> List[Dict]:
    """
    Search for articles using Google Custom Search API
    
    Parameters:
    -----------
    query : str
        The search query
    num_results : int
        Number of results to return (default: 5)
        
    Returns:
    --------
    List[Dict]
        List of search results with title, url, snippet
    """
    api_key = API_KEYS.get("google_search_api", "")
    engine_id = API_KEYS.get("google_search_engine_id", "")
    
    if not api_key or not engine_id:
        logger.warning("Google Search API credentials not found, using mock results")
        return mock_search_results(query, num_results, 
                                 error="no_api_key",
                                 message="Google Search API credentials not configured")
    
    try:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": api_key,
            "cx": engine_id,
            "q": f"{query} news",
            "num": min(num_results, 10),  # Google API max is 10
            "searchType": "image",
            "fileType": "html"
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        results = []
        items = data.get("items", [])
        
        for item in items[:num_results]:
            results.append({
                "title": item.get("title", ""),
                "url": item.get("link", ""),
                "snippet": item.get("snippet", ""),
                "source": item.get("displayLink", ""),
                "date": ""
            })
        
        logger.info(f"Found {len(results)} search results")
        return results
        
    except Exception as e:
        logger.error(f"Google Search API failed: {e}")
        return mock_search_results(query, num_results, 
                                 error="api_error",
                                 message=f"Google Search API failed: {str(e)}")

def mock_search_results(query: str, num_results: int = 5, error: str = None, message: str = None) -> List[Dict]:
    """
    Generate mock search results for demo purposes
    
    Parameters:
    -----------
    query : str
        The search query (used for context)
    num_results : int
        Number of results to generate
    error : str
        Error type that triggered fallback to mock results
    message : str
        Detailed error message for user display
        
    Returns:
    --------
    List[Dict]
        Mock search results with error context
    """
    if error:
        logger.info(f"Generating mock results due to {error}: {message}")
    
    mock_results = [
        {
            "title": f"Breaking: {query.title()} - Latest Updates and Analysis",
            "url": "https://example.com/breaking-news-1",
            "snippet": f"Latest developments in {query} with comprehensive analysis and expert opinions from leading experts...",
            "source": "Reuters",
            "date": "2025-09-20",
            "domain": "reuters.com",
            "api_source": "mock_fallback",
            "position": 1,
            "error_type": error,
            "error_message": message
        },
        {
            "title": f"In-depth Report: Understanding the Impact of {query.title()}",
            "url": "https://example.com/in-depth-report-2", 
            "snippet": f"A detailed examination of how {query} affects various sectors and communities across different regions...",
            "source": "BBC News",
            "date": "2025-09-19",
            "domain": "bbc.com",
            "api_source": "mock_fallback",
            "position": 2,
            "error_type": error,
            "error_message": message
        },
        {
            "title": f"Expert Analysis: {query.title()} and Its Global Implications",
            "url": "https://example.com/expert-analysis-3",
            "snippet": f"Leading experts weigh in on the significance of {query} and future projections for global impact...",
            "source": "CNN",
            "date": "2025-09-18",
            "domain": "cnn.com",
            "api_source": "mock_fallback",
            "position": 3,
            "error_type": error,
            "error_message": message
        },
        {
            "title": f"Market Response: How {query.title()} Affects the Economy",
            "url": "https://example.com/market-response-4",
            "snippet": f"Financial markets react to {query} with varied responses across different sectors and regions...",
            "source": "Associated Press",
            "date": "2025-09-17",
            "domain": "apnews.com",
            "api_source": "mock_fallback",
            "position": 4,
            "error_type": error,
            "error_message": message
        },
        {
            "title": f"Public Opinion: Community Reactions to {query.title()}",
            "url": "https://example.com/public-opinion-5",
            "snippet": f"Survey results show diverse public opinions on {query} across different demographics and regions...",
            "source": "Washington Post",
            "date": "2025-09-16",
            "domain": "washingtonpost.com",
            "api_source": "mock_fallback",
            "position": 5,
            "error_type": error,
            "error_message": message
        }
    ]
    
    return mock_results[:num_results]

def validate_search_query(query: str) -> bool:
    """
    Validate search query
    
    Parameters:
    -----------
    query : str
        The search query to validate
        
    Returns:
    --------
    bool
        True if query is valid, False otherwise
    """
    if not query or not query.strip():
        return False
    
    if len(query.strip()) < 3:
        return False
    
    return True

def check_serp_api_status() -> Dict[str, bool]:
    """
    Check the status of available SERP APIs
    
    Returns:
    --------
    Dict[str, bool]
        Status of each API (True if available, False if not)
    """
    return {
        "serp_api": bool(API_KEYS.get("serp_api", "")),
        "google_search": bool(API_KEYS.get("google_search_api", "") and API_KEYS.get("google_search_engine_id", "")),
        "mock_available": True
    }