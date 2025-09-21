"""
Analysis tools for DeFacture

This module contains functions for analyzing articles:
- Summarization (mock and real)
- Context analysis
- Related articles search
- Fact checking
- Future: Claim extraction and agent-based analysis
"""

import os
import logging
from typing import List, Dict, Optional
from dataclasses import dataclass

# Offline extractive summarizer (no internet)
try:
    from sumy.parsers.plaintext import PlaintextParser
    from sumy.nlp.tokenizers import Tokenizer
    from sumy.summarizers.lex_rank import LexRankSummarizer
except Exception:
    LexRankSummarizer = None

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock data for demonstration purposes
def mock_summarization_chain(text: str, article_data: Optional[Dict] = None) -> Dict:
    """
    Mock function for article summarization
    
    Parameters:
    -----------
    text : str
        The article text to summarize
    article_data : dict, optional
        Full article data including potential pre-computed mock analysis
        
    Returns:
    --------
    Dict
        A dictionary containing the summary and key points
    """
    logger.info("Mock summarization called")
    logger.info(f"Article data keys: {article_data.keys() if article_data else 'No article data'}")
    
    # Check if article has pre-computed mock analysis
    if article_data and "mock_analysis" in article_data:
        logger.info("Found mock_analysis in article_data")
        if "summary" in article_data["mock_analysis"]:
            logger.info("Found summary in mock_analysis")
            logger.info(f"Summary: {article_data['mock_analysis']['summary']}")
            return article_data["mock_analysis"]["summary"]
        else:
            logger.info("No summary found in mock_analysis")
    else:
        logger.info("No mock_analysis found in article_data")
    
    # Default mock response
    return {
        "summary": "This is a mock summary of the article. In a real implementation, this would use LangChain to generate a concise summary.",
        "key_points": [
            "First key point from the article",
            "Second key point that highlights important information",
            "Third key point with critical context"
        ]
    }

def mock_context_analysis_chain(text: str, article_data: Optional[Dict] = None) -> Dict:
    """
    Mock function for context analysis
    
    Parameters:
    -----------
    text : str
        The article text to analyze
    article_data : dict, optional
        Full article data including potential pre-computed mock analysis
        
    Returns:
    --------
    Dict
        A dictionary containing the context analysis
    """
    logger.info("Mock context analysis called")
    
    # Check if article has pre-computed mock analysis
    if article_data and "mock_analysis" in article_data and "context" in article_data["mock_analysis"]:
        logger.info("Using pre-computed mock context analysis data")
        return article_data["mock_analysis"]["context"]
    
    # Default mock response
    return {
        "perspective": "The article appears to present a balanced view of the topic.",
        "bias_indicators": ["Minor use of loaded language", "Generally presents multiple perspectives"],
        "historical_context": "This article relates to ongoing discussions about this topic that began in 2023.",
        "missing_context": "The article doesn't mention some relevant background information about regulatory changes."
    }

def mock_related_articles_chain(text: str, article_data: Optional[Dict] = None) -> List[Dict]:
    """
    Mock function for finding related articles
    
    Parameters:
    -----------
    text : str
        The article text to find related articles for
    article_data : dict, optional
        Full article data including potential pre-computed mock analysis
        
    Returns:
    --------
    List[Dict]
        A list of related article information
    """
    logger.info("Mock related articles search called")
    
    # Check if article has pre-computed mock analysis
    if article_data and "mock_analysis" in article_data and "related_articles" in article_data["mock_analysis"]:
        logger.info("Using pre-computed mock related articles data")
        return article_data["mock_analysis"]["related_articles"]
    
    # Default mock response
    return [
        {
            "title": "Related Article 1",
            "source": "News Source A",
            "date": "2025-09-01",
            "url": "https://example.com/related1",
            "relevance": "High",
            "perspective": "Similar"
        },
        {
            "title": "Related Article 2",
            "source": "News Source B",
            "date": "2025-08-28",
            "url": "https://example.com/related2",
            "relevance": "Medium",
            "perspective": "Opposing"
        }
    ]

def mock_fact_check_chain(text: str, article_data: Optional[Dict] = None) -> Dict:
    """
    Mock function for fact checking
    
    Parameters:
    -----------
    text : str
        The article text to fact check
    article_data : dict, optional
        Full article data including potential pre-computed mock analysis
        
    Returns:
    --------
    Dict
        A dictionary containing the fact check results
    """
    logger.info("Mock fact checking called")
    
    # Check if article has pre-computed mock analysis
    if article_data and "mock_analysis" in article_data and "fact_check" in article_data["mock_analysis"]:
        logger.info("Using pre-computed mock fact check data")
        return article_data["mock_analysis"]["fact_check"]
    
    # Default mock response
    return {
        "overall_assessment": "Mostly Accurate",
        "claims": [
            {
                "claim": "First claim extracted from article",
                "assessment": "Accurate",
                "evidence": "Supporting information for this assessment"
            },
            {
                "claim": "Second claim extracted from article",
                "assessment": "Partially Accurate",
                "evidence": "This claim contains some inaccuracies regarding dates and figures"
            }
        ]
    }

def _extractive_summary(text: str, sentences: int = 3) -> str:
    """
    Offline extractive summary using LexRank (sumy).
    No internet, fast, deterministic. Returns up to `sentences` sentences.
    """
    if not text or not text.strip():
        return ""
    if LexRankSummarizer is None:
        return ""

    # Clean the text
    text = text.strip()
    if len(text) < 50:  # Too short to summarize
        return text
        
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    
    # Get document sentences count
    doc_sentences = len(list(parser.document.sentences))
    
    # If document has fewer sentences than requested, return all
    if doc_sentences <= sentences:
        return text
        
    summary_sents = summarizer(parser.document, sentences)
    return " ".join(str(s) for s in summary_sents)

def _extract_key_points(text: str, num_points: int = 4) -> List[str]:
    """
    Extract key points from text using sentence ranking
    """
    if not text or not text.strip():
        return []
    if LexRankSummarizer is None:
        return []
        
    # Clean the text
    text = text.strip()
    if len(text) < 100:
        return [text]
        
    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LexRankSummarizer()
        
        # Get more sentences for key points than summary
        sentences_for_points = min(num_points + 2, len(list(parser.document.sentences)))
        summary_sents = summarizer(parser.document, sentences_for_points)
        
        # Convert to key points format
        key_points = []
        for sent in summary_sents:
            sent_str = str(sent).strip()
            if sent_str and len(sent_str) > 20:  # Filter very short sentences
                # Make it more like a key point
                if not sent_str.endswith('.'):
                    sent_str += '.'
                key_points.append(sent_str)
                if len(key_points) >= num_points:
                    break
                    
        return key_points
    except Exception:
        # Fallback: split into sentences and take first few
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        return sentences[:num_points]

def real_summarization_chain(text: str) -> Dict:
    """
    Real summarization (offline extractive via LexRank).
    Later, swap this body to call a Transformers / LangChain LLM.
    """
    # Cap very long inputs (basic guard)
    cleaned = text.strip()
    if len(cleaned) > 15000:
        cleaned = cleaned[:15000]
    
    if len(cleaned) < 100:
        return {
            "summary": "Article too short to summarize effectively.",
            "key_points": [cleaned] if cleaned else []
        }

    summary = _extractive_summary(cleaned, sentences=3)
    key_points = _extract_key_points(cleaned, num_points=4)
    
    if not summary:
        # If sumy missing or failed, fall back to mock-style message
        return {
            "summary": "Summary unavailable: Summarizer could not process this text.",
            "key_points": [
                "Unable to extract key points from this article",
                "Please try with a different article",
                "Check if the article content is properly formatted",
            ]
        }

    # Ensure we have a proper summary (not just the original text)
    if len(summary) > len(cleaned) * 0.8:  # Summary is too similar to original
        # Try with fewer sentences
        summary = _extractive_summary(cleaned, sentences=2)
        if len(summary) > len(cleaned) * 0.7:  # Still too long
            # Create a simple summary by taking first few sentences
            sentences = [s.strip() + '.' for s in cleaned.split('.') if s.strip()]
            summary = ' '.join(sentences[:2])

    return {
        "summary": summary,
        "key_points": key_points if key_points else ["No key points could be extracted from this article."]
    }

def summarize_article(text: str) -> Dict:
    """
    Wrapper function for article summarization that can switch between mock and real implementation
    
    Parameters:
    -----------
    text : str
        The article text to summarize
        
    Returns:
    --------
    Dict
        A dictionary containing the summary and key points
    """
    # In a real implementation, this would check a config setting to decide whether
    # to use the mock or real implementation
    return mock_summarization_chain(text)