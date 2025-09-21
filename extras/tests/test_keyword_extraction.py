"""
Test script to verify the keyword extraction functionality
"""

import sys
import json
from pprint import pprint

try:
    from tools.keyword_extraction import (
        extract_keywords, 
        generate_search_query, 
        extract_keywords_basic,
        extract_keywords_nltk,
        extract_keywords_tfidf,
        extract_named_entities
    )
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

def test_keyword_extraction():
    """Test the keyword extraction with a sample article"""
    
    # Sample article
    article = {
        "title": "The Impact of Climate Change on Global Ecosystems",
        "content": """
        Climate change is causing significant shifts in global ecosystems. Rising temperatures, 
        changing precipitation patterns, and extreme weather events are altering habitats worldwide.
        Researchers from Stanford University and the Environmental Protection Agency have documented 
        these changes across forests, oceans, and grasslands. According to Dr. James Thompson, 
        a leading ecologist, "We're seeing migrations of species toward cooler climates at a rate 
        faster than predicted." The melting of polar ice caps is especially concerning for Arctic 
        wildlife such as polar bears and seals. Meanwhile, coral reefs are experiencing unprecedented 
        bleaching events due to ocean acidification. The United Nations Environment Programme has 
        called for immediate action to reduce carbon emissions and implement adaptation strategies.
        """
    }
    
    print("Testing keyword extraction...")
    
    # Test different methods
    methods = ["basic", "nltk", "tfidf", "entity", "hybrid"]
    for method in methods:
        try:
            print(f"\n=== Testing '{method}' method ===")
            keywords = extract_keywords(article, max_keywords=10, method=method)
            print(f"Keywords ({len(keywords)}): {keywords}")
        except Exception as e:
            print(f"Error with method '{method}': {e}")
    
    # Test search query generation
    print("\n=== Testing search query generation ===")
    query = generate_search_query(article, max_query_length=100)
    print(f"Search query: '{query}'")
    
    # Test with article with no title
    no_title_article = {
        "content": article["content"],
        "source": "url"
    }
    
    print("\n=== Testing with no title ===")
    keywords = extract_keywords(no_title_article)
    print(f"Keywords: {keywords}")
    
    query = generate_search_query(no_title_article)
    print(f"Search query: '{query}'")

if __name__ == "__main__":
    test_keyword_extraction()