"""
JSON dataset processing tools for DeFacture

This module contains functions for handling uploaded JSON datasets:
- Validate JSON structure
- Extract articles from different JSON formats
- Process batch datasets
"""

import json
import logging
from typing import List, Dict, Optional, Union
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_json_dataset(file_content: str) -> Dict[str, Union[bool, str, List]]:
    """
    Validate uploaded JSON dataset structure
    
    Parameters:
    -----------
    file_content : str
        Raw content of the uploaded JSON file
        
    Returns:
    --------
    Dict
        Validation result with status, message, and parsed articles
    """
    try:
        # Try to parse JSON
        data = json.loads(file_content)
        
        # Check if it's a list or dict
        if isinstance(data, list):
            articles = data
        elif isinstance(data, dict):
            # Check for common structures
            if "articles" in data:
                articles = data["articles"]
            elif "data" in data:
                articles = data["data"]
            elif "items" in data:
                articles = data["items"]
            else:
                # Assume the dict itself is an article
                articles = [data]
        else:
            return {
                "valid": False,
                "message": "JSON must contain an object or array",
                "articles": []
            }
        
        # Validate articles structure
        valid_articles = []
        for i, article in enumerate(articles):
            if not isinstance(article, dict):
                continue
                
            # Check for required fields (title and content)
            title = article.get("title", "") or article.get("headline", "") or article.get("name", "")
            content = (article.get("content", "") or 
                      article.get("text", "") or 
                      article.get("body", "") or 
                      article.get("description", "") or
                      article.get("summary", ""))
            
            if not title and not content:
                continue
                
            # Create standardized article structure
            standardized_article = {
                "title": title or f"Article {i+1}",
                "content": content or "No content available",
                "url": article.get("url", "") or article.get("link", ""),
                "source": article.get("source", "") or article.get("site", "") or "Uploaded Dataset",
                "date": article.get("date", "") or article.get("published", "") or article.get("timestamp", ""),
                "authors": article.get("authors", []) or article.get("author", []),
                "dataset_index": i
            }
            
            valid_articles.append(standardized_article)
        
        if not valid_articles:
            return {
                "valid": False,
                "message": "No valid articles found. Articles must have 'title' and 'content' (or similar fields)",
                "articles": []
            }
        
        return {
            "valid": True,
            "message": f"Successfully processed {len(valid_articles)} articles",
            "articles": valid_articles
        }
        
    except json.JSONDecodeError as e:
        return {
            "valid": False,
            "message": f"Invalid JSON format: {str(e)}",
            "articles": []
        }
    except Exception as e:
        return {
            "valid": False,
            "message": f"Error processing dataset: {str(e)}",
            "articles": []
        }

def process_jsonl_dataset(file_content: str) -> Dict[str, Union[bool, str, List]]:
    """
    Process JSONL (JSON Lines) dataset
    
    Parameters:
    -----------
    file_content : str
        Raw content of the uploaded JSONL file
        
    Returns:
    --------
    Dict
        Processing result with status, message, and parsed articles
    """
    try:
        lines = file_content.strip().split('\n')
        valid_articles = []
        
        for i, line in enumerate(lines):
            if not line.strip():
                continue
                
            try:
                article = json.loads(line)
                
                # Check for required fields
                title = article.get("title", "") or article.get("headline", "") or article.get("name", "")
                content = (article.get("content", "") or 
                          article.get("text", "") or 
                          article.get("body", "") or 
                          article.get("description", ""))
                
                if not title and not content:
                    continue
                
                standardized_article = {
                    "title": title or f"Article {i+1}",
                    "content": content or "No content available",
                    "url": article.get("url", "") or article.get("link", ""),
                    "source": article.get("source", "") or article.get("site", "") or "Uploaded Dataset",
                    "date": article.get("date", "") or article.get("published", ""),
                    "authors": article.get("authors", []) or article.get("author", []),
                    "dataset_index": i
                }
                
                valid_articles.append(standardized_article)
                
            except json.JSONDecodeError:
                logger.warning(f"Skipping invalid JSON on line {i+1}")
                continue
        
        if not valid_articles:
            return {
                "valid": False,
                "message": "No valid articles found in JSONL file",
                "articles": []
            }
        
        return {
            "valid": True,
            "message": f"Successfully processed {len(valid_articles)} articles from JSONL",
            "articles": valid_articles
        }
        
    except Exception as e:
        return {
            "valid": False,
            "message": f"Error processing JSONL dataset: {str(e)}",
            "articles": []
        }

def get_dataset_preview(articles: List[Dict], max_preview: int = 3) -> List[Dict]:
    """
    Generate preview of dataset articles
    
    Parameters:
    -----------
    articles : List[Dict]
        List of processed articles
    max_preview : int
        Maximum number of articles to preview
        
    Returns:
    --------
    List[Dict]
        Preview articles with truncated content
    """
    preview_articles = []
    
    for article in articles[:max_preview]:
        preview = {
            "title": article["title"],
            "content_preview": article["content"][:200] + "..." if len(article["content"]) > 200 else article["content"],
            "source": article["source"],
            "date": article["date"],
            "word_count": len(article["content"].split()) if article["content"] else 0,
            "dataset_index": article["dataset_index"]
        }
        preview_articles.append(preview)
    
    return preview_articles

def create_sample_dataset() -> str:
    """
    Create a sample JSON dataset for demonstration
    
    Returns:
    --------
    str
        Sample JSON dataset as string
    """
    sample_dataset = {
        "articles": [
            {
                "title": "Sample Tech Innovation Article",
                "content": "This is a sample article about technological innovation and its impact on society. The article discusses various aspects of how technology is reshaping our daily lives and business operations.",
                "url": "https://example.com/tech-innovation",
                "source": "Tech Weekly",
                "date": "2025-09-20",
                "authors": ["Dr. Jane Smith", "Prof. John Doe"]
            },
            {
                "title": "Environmental Policy Update",
                "content": "Recent developments in environmental policy have significant implications for businesses and consumers alike. This article explores the new regulations and their expected impact.",
                "url": "https://example.com/env-policy",
                "source": "Environmental Times",
                "date": "2025-09-19",
                "authors": ["Maria Garcia"]
            }
        ]
    }
    
    return json.dumps(sample_dataset, indent=2)