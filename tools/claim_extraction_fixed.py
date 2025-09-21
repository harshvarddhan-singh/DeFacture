"""
Claim extraction tools for DeFacture

This module contains functions for extracting factual claims from article text:
- Sentence tokenization using NLTK
- Candidate claim filtering based on numbers, dates, and named entities
- Confidence scoring for extracted claims

This version has been patched to handle NLTK resource issues.
"""

import re
import logging
from typing import List, Dict
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download required NLTK data if not already present
def _ensure_nltk_data():
    """Ensure NLTK data is available, download if needed"""
    try:
        # Try to import required NLTK functions first
        from nltk.tokenize import sent_tokenize, word_tokenize
        
        # Test if data is available by trying to use it
        sent_tokenize("Test sentence.")
        word_tokenize("Test")
        
        return True
        
    except LookupError:
        # Data not found, try to download
        logger.info("NLTK data not found, attempting download...")
        try:
            import ssl
            # Handle SSL certificate issues
            try:
                _create_unverified_https_context = ssl._create_unverified_context
            except AttributeError:
                pass
            else:
                ssl._create_default_https_context = _create_unverified_https_context
            
            # Download all necessary NLTK data
            nltk.download('punkt', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)  # This is for English
            nltk.download('maxent_ne_chunker', quiet=True)
            nltk.download('words', quiet=True)
            nltk.download('stopwords', quiet=True)
            logger.info("NLTK data downloaded successfully")
            return True
            
        except Exception as e:
            logger.warning(f"Could not download NLTK data: {e}")
            return False
    except Exception as e:
        logger.warning(f"Error checking NLTK data: {e}")
        return False

# Initialize NLTK data availability
NLTK_AVAILABLE = _ensure_nltk_data()

def _contains_numbers_or_dates(sentence: str) -> bool:
    """
    Check if sentence contains numbers, dates, percentages, or measurements
    
    Parameters:
    -----------
    sentence : str
        The sentence to check
        
    Returns:
    --------
    bool
        True if sentence contains numerical or date information
    """
    # Patterns for numbers, dates, percentages, measurements
    patterns = [
        r'\b\d+\.?\d*\b',           # Numbers (integers and decimals)
        r'\b\d+%\b',                # Percentages
        r'\b\d{4}\b',               # Years
        r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',  # Dates (MM/DD/YYYY)
        r'\b\d{1,2}-\d{1,2}-\d{2,4}\b',  # Dates (MM-DD-YYYY)
        r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\b',  # Month names
        r'\b(million|billion|trillion|thousand)\b',  # Large numbers
        r'\b\d+\s*(years?|months?|days?|weeks?|hours?|minutes?)\b',  # Time periods
        r'\b\d+\s*(dollars?|euros?|pounds?|\$|€|£)\b',  # Monetary amounts
        r'\$\d+\.?\d*\b',           # Dollar amounts
        r'\b\d+\s*(km|miles?|meters?|feet|inches?|kg|pounds?|lbs)\b',  # Measurements
    ]
    
    sentence_lower = sentence.lower()
    for pattern in patterns:
        if re.search(pattern, sentence_lower, re.IGNORECASE):
            return True
    
    return False

def _custom_pos_tag(tokens: List[str]) -> List[tuple]:
    """
    Custom POS tagging function that doesn't rely on the problematic tagger
    
    Parameters:
    -----------
    tokens : List[str]
        List of tokens to tag
        
    Returns:
    --------
    List[tuple]
        List of (token, tag) pairs
    """
    result = []
    for token in tokens:
        # Simple heuristic for proper nouns: capitalized words
        if token and len(token) > 0 and token[0].isupper() and token.isalpha():
            result.append((token, 'NNP'))
        else:
            result.append((token, 'NN'))
    return result

def _contains_named_entities(sentence: str) -> bool:
    """
    Check if sentence contains potential named entities using simple heuristics
    
    Parameters:
    -----------
    sentence : str
        The sentence to check
        
    Returns:
    --------
    bool
        True if sentence contains proper nouns (potential named entities)
    """
    if not NLTK_AVAILABLE:
        # Fallback to simple proper noun detection
        return bool(re.search(r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b', sentence))
    
    try:
        # Tokenize the text
        words = word_tokenize(sentence)
        
        # Use custom POS tagging function
        pos_tags = _custom_pos_tag(words)
        
        # Look for proper nouns (NNP, NNPS) which often indicate named entities
        for word, tag in pos_tags:
            if tag in ['NNP', 'NNPS']:  # Proper noun, singular/plural
                return True
                
        # Also check for common organization/location indicators
        entity_indicators = [
            r'\b(Inc\.|Corp\.|Ltd\.|LLC|Company|University|Hospital|School)\b',
            r'\b(President|CEO|Director|Minister|Senator|Representative)\b',
            r'\b(said|announced|reported|confirmed|stated|declared)\b',  # Attribution verbs
        ]
        
        for pattern in entity_indicators:
            if re.search(pattern, sentence, re.IGNORECASE):
                return True
                
    except Exception as e:
        logger.warning(f"Error in named entity detection: {e}")
        # Fallback to simple proper noun detection
        return bool(re.search(r'\b[A-Z][a-z]+\b', sentence))
    
    return False

def _contains_claim_indicators(sentence: str) -> bool:
    """
    Check if sentence contains phrases often associated with factual claims
    
    Parameters:
    -----------
    sentence : str
        The sentence to check
        
    Returns:
    --------
    bool
        True if sentence contains claim indicators
    """
    indicators = [
        r'\b(study|research|survey|poll|report)\s+(show|found|indicate|suggest|reveal|conclude)',
        r'\b(according\s+to|based\s+on)\b',
        r'\b(evidence|data|statistics|figures|numbers|results)\s+(show|indicate|suggest|reveal)',
        r'\b(scientist|researcher|expert|analyst|official|source)\s+(say|state|claim|report|confirm)',
        r'\b(significant|substantial|considerable|major|important)\s+(increase|decrease|change|impact)',
        r'\b(discover|determine|establish|verify|confirm|prove|demonstrate)\b',
        r'\b(fact|truth|reality|actually|indeed|certainly|definitely)\b'
    ]
    
    sentence_lower = sentence.lower()
    for pattern in indicators:
        if re.search(pattern, sentence_lower, re.IGNORECASE):
            return True
            
    return False

def _calculate_claim_confidence(sentence: str) -> float:
    """
    Calculate a confidence score for a sentence being a factual claim
    
    Parameters:
    -----------
    sentence : str
        The sentence to evaluate
        
    Returns:
    --------
    float
        Confidence score (0-1) with 1 being highest confidence
    """
    score = 0.0
    
    # Check for numbers, dates, etc. (strong indicator)
    if _contains_numbers_or_dates(sentence):
        score += 0.4
        
    # Check for named entities (moderate indicator)
    if _contains_named_entities(sentence):
        score += 0.3
        
    # Check for claim-related phrases (moderate indicator)
    if _contains_claim_indicators(sentence):
        score += 0.3
        
    # Adjust for sentence length (very short or very long sentences less likely to be standalone claims)
    words = len(sentence.split())
    if words < 5:
        score *= 0.5  # Penalize very short sentences
    elif words > 40:
        score *= 0.7  # Penalize very long sentences
    
    # Check for question marks (questions are rarely factual claims)
    if '?' in sentence:
        score *= 0.3  # Significant penalty for questions
        
    # Cap score at 1.0
    return min(score, 1.0)

def extract_claims(article_text: str, min_confidence: float = 0.5) -> List[Dict]:
    """
    Extract potential factual claims from article text
    
    Parameters:
    -----------
    article_text : str
        The article text to analyze
    min_confidence : float
        Minimum confidence threshold for including a claim
        
    Returns:
    --------
    List[Dict]
        List of dictionaries with 'claim' and 'confidence' keys
    """
    if not article_text or len(article_text.strip()) == 0:
        logger.warning("Empty article text provided to extract_claims")
        return []
    
    try:
        # Tokenize article into sentences
        sentences = sent_tokenize(article_text)
        
        # Process each sentence to identify potential claims
        results = []
        for sentence in sentences:
            # Skip very short sentences
            if len(sentence.split()) < 4:
                continue
                
            # Calculate confidence score
            confidence = _calculate_claim_confidence(sentence)
            
            # Add to results if above threshold
            if confidence >= min_confidence:
                results.append({
                    'claim': sentence,
                    'confidence': round(confidence, 2)
                })
        
        # Sort by confidence (descending)
        results.sort(key=lambda x: x['confidence'], reverse=True)
        
        # Limit to top 10 claims if more exist
        if len(results) > 10:
            results = results[:10]
            
        logger.info(f"Extracted {len(results)} potential claims")
        return results
    
    except Exception as e:
        logger.error(f"Error extracting claims: {e}")
        return []

def get_claim_statistics(claims: List[Dict]) -> Dict:
    """
    Generate statistics about extracted claims
    
    Parameters:
    -----------
    claims : List[Dict]
        List of extracted claims
        
    Returns:
    --------
    Dict
        Statistics about the claims
    """
    if not claims:
        return {
            "total_claims": 0,
            "avg_confidence": 0.0,
            "high_confidence_count": 0
        }
    
    confidences = [claim["confidence"] for claim in claims]
    
    return {
        "total_claims": len(claims),
        "avg_confidence": round(sum(confidences) / len(confidences), 2),
        "high_confidence_count": len([c for c in confidences if c >= 0.7])
    }

def get_claim_statistics(claims: List[Dict]) -> Dict:
    """
    Generate statistics about extracted claims
    
    Parameters:
    -----------
    claims : List[Dict]
        List of extracted claims
        
    Returns:
    --------
    Dict
        Statistics about the claims
    """
    if not claims:
        return {
            "total_claims": 0,
            "avg_confidence": 0.0,
            "high_confidence_count": 0
        }
    
    confidences = [claim["confidence"] for claim in claims]
    
    return {
        "total_claims": len(claims),
        "avg_confidence": round(sum(confidences) / len(confidences), 2),
        "high_confidence_count": len([c for c in confidences if c >= 0.7])
    }