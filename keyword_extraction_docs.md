# Enhanced Keyword Extraction and Related Articles

This document explains the enhanced keyword extraction functionality and related article handling in DeFacture.

## Overview

The keyword extraction system has been enhanced to provide better search queries for the SERP API when finding related articles, especially for URL-sourced articles.

## Key Components

### 1. Keyword Extraction (`tools/keyword_extraction.py`)

This module provides several methods to extract relevant keywords from article content:

- **Basic Extraction**: Simple frequency-based extraction with basic stopword removal
- **NLTK-based Extraction**: More sophisticated extraction using NLTK's tokenization, lemmatization, and stopword filtering
- **TF-IDF Extraction**: Uses TF-IDF scoring to identify important terms (when scikit-learn is available)
- **Named Entity Recognition**: Extracts named entities like people, organizations, and locations (with graceful fallback)
- **Hybrid Approach**: Combines multiple methods to get the best keywords

### 2. Search Query Generation

The `generate_search_query()` function creates optimized search queries by:

1. Using the article title if available
2. Adding relevant keywords not already in the title 
3. Limiting query length for optimal search performance
4. Falling back to pure keyword-based queries when no title exists

### 3. URL Article Handling in Analysis Tabs

For URL-sourced articles with no search results in the session state, the system:

1. Extracts keywords from the article content
2. Generates an optimized search query
3. Uses the SERP API to find related articles
4. Stores results in the session state for future use
5. Falls back to sample articles only if no results are found

## Error Handling

- Graceful fallback when NLTK resources are unavailable
- Specific handling for the "averaged_perceptron_tagger_eng" NLTK issue
- Warning suppression for common NLTK errors

## Usage

The keyword extraction system is used automatically when analyzing URL articles without search results. For manual usage:

```python
from tools.keyword_extraction import extract_keywords, generate_search_query

# Extract keywords from an article
article_data = {
    "title": "Climate Change Impact on Global Economy",
    "content": "Long article content here..."
}

# Get keywords
keywords = extract_keywords(article_data, max_keywords=10, method="hybrid")
print(f"Keywords: {keywords}")

# Generate search query
search_query = generate_search_query(article_data, max_query_length=100)
print(f"Search query: {search_query}")
```

## Customization

You can customize keyword extraction by modifying parameters:

- `max_keywords`: Controls how many keywords to extract
- `method`: Choose between "basic", "nltk", "tfidf", "entity", or "hybrid"
- `max_query_length`: Limit the length of generated search queries

## Requirements

- NLTK is required for advanced extraction methods
- scikit-learn is optional for TF-IDF extraction
- Both packages are gracefully handled if not available