"""
Claim extraction tools for DeFacture

This module contains functions for extracting factual claims from article text:
- Sentence tokenization using NLTK
- Candidate claim filtering based on numbers, dates, and named entities
- Confidence scoring for extracted claims
"""

import re
import logging
from typing import List, Dict
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download required NLTK data if not already present
def _ensure_nltk_data():
    """Ensure NLTK data is available, download if needed"""
    try:
        # Try to import required NLTK functions first
        from nltk.tokenize import sent_tokenize, word_tokenize
        from nltk.tag import pos_tag
        
        # Test if data is available by trying to use it
        sent_tokenize("Test sentence.")
        pos_tag(word_tokenize("Test"))
        
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

def _contains_named_entities(sentence: str) -> bool:
    """
    Check if sentence contains potential named entities using POS tagging
    
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
        # Import NLTK functions (only after ensuring availability)
        from nltk.tokenize import word_tokenize
        from nltk.tag import pos_tag
        
        # Tokenize and get POS tags
        words = word_tokenize(sentence)
        pos_tags = pos_tag(words)
        
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

def _calculate_claim_confidence(sentence: str) -> float:
    """
    Calculate confidence score for a potential claim based on various factors
    
    Parameters:
    -----------
    sentence : str
        The sentence to score
        
    Returns:
    --------
    float
        Confidence score between 0.0 and 1.0
    """
    confidence = 0.5  # Base confidence
    
    # Increase confidence for factual indicators
    factual_indicators = [
        r'\b(research|study|survey|data|statistics|analysis|report)\b',
        r'\b(according to|based on|found that|shows that|indicates)\b',
        r'\b(percent|percentage|rate|average|total|amount)\b',
        r'\b(increased|decreased|grew|fell|rose|dropped)\b',
        r'\b(million|billion|trillion|thousand)\b',
        r'\b\d+\.?\d*\s*(percent|%)\b',
    ]
    
    sentence_lower = sentence.lower()
    for pattern in factual_indicators:
        if re.search(pattern, sentence_lower):
            confidence += 0.1
            
    # Increase confidence for specific numbers and dates
    if _contains_numbers_or_dates(sentence):
        confidence += 0.2
        
    # Increase confidence for named entities
    if _contains_named_entities(sentence):
        confidence += 0.15
        
    # Decrease confidence for opinion indicators
    opinion_indicators = [
        r'\b(believe|think|feel|opinion|might|could|should|would)\b',
        r'\b(probably|possibly|likely|maybe|perhaps)\b',
        r'\b(I think|in my opinion|personally)\b',
    ]
    
    for pattern in opinion_indicators:
        if re.search(pattern, sentence_lower):
            confidence -= 0.2
            
    # Ensure confidence is within bounds
    confidence = max(0.1, min(1.0, confidence))
    
    return round(confidence, 2)

def extract_claims(text: str) -> List[Dict]:
    """
    Extract potential factual claims from article text
    
    Parameters:
    -----------
    text : str
        The article text to extract claims from
        
    Returns:
    --------
    List[Dict]
        List of dictionaries containing claim text and confidence scores
        Format: [{"claim": str, "confidence": float}, ...]
    """
    if not text or not text.strip():
        return []
        
    logger.info("Starting claim extraction")
    
    # Check if NLTK is available
    if not NLTK_AVAILABLE:
        logger.warning("NLTK not available, using fallback extraction")
        return _fallback_extract_claims(text)
    
    try:
        # Import NLTK functions (only after ensuring availability)
        from nltk.tokenize import sent_tokenize
        
        # Tokenize text into sentences
        sentences = sent_tokenize(text)
        logger.info(f"Found {len(sentences)} sentences")
        
        claims = []
        
        for sentence in sentences:
            # Skip very short sentences
            if len(sentence.split()) < 5:
                continue
                
            # Skip sentences that are questions or commands
            if sentence.strip().endswith('?') or sentence.strip().startswith(('How', 'What', 'When', 'Where', 'Why', 'Who')):
                continue
                
            # Check if sentence contains potential claim indicators
            is_candidate = False
            
            # Check for numbers, dates, or measurements
            if _contains_numbers_or_dates(sentence):
                is_candidate = True
                
            # Check for named entities
            elif _contains_named_entities(sentence):
                is_candidate = True
                
            # Check for factual statements with attribution
            factual_patterns = [
                r'\b(research|study|survey|report|analysis)\b.*\b(found|shows|indicates|reveals)\b',
                r'\b(according to|based on|data shows|statistics show)\b',
                r'\b(announced|confirmed|reported|stated|declared)\b',
            ]
            
            sentence_lower = sentence.lower()
            for pattern in factual_patterns:
                if re.search(pattern, sentence_lower):
                    is_candidate = True
                    break
            
            if is_candidate:
                confidence = _calculate_claim_confidence(sentence)
                
                # Only include claims with reasonable confidence
                if confidence >= 0.4:
                    claims.append({
                        "claim": sentence.strip(),
                        "confidence": confidence
                    })
        
        # Sort by confidence (highest first)
        claims.sort(key=lambda x: x["confidence"], reverse=True)
        
        # Limit to top 10 claims to avoid overwhelming the UI
        claims = claims[:10]
        
        logger.info(f"Extracted {len(claims)} potential claims")
        return claims
        
    except Exception as e:
        logger.error(f"Error in claim extraction: {e}")
        return _fallback_extract_claims(text)

def _fallback_extract_claims(text: str) -> List[Dict]:
    """
    Fallback claim extraction when NLTK is not available
    Uses simple sentence splitting and basic pattern matching
    """
    logger.info("Using fallback claim extraction")
    
    try:
        # Simple sentence splitting (fallback)
        sentences = []
        for delimiter in ['. ', '! ', '? ', '.\n', '!\n', '?\n']:
            if delimiter in text:
                text = text.replace(delimiter, delimiter + '|SPLIT|')
        
        raw_sentences = text.split('|SPLIT|')
        sentences = [s.strip() for s in raw_sentences if s.strip() and len(s.split()) >= 5]
        
        claims = []
        
        for sentence in sentences[:50]:  # Limit processing
            # Check for basic claim indicators
            if (_contains_numbers_or_dates(sentence) or 
                any(word in sentence.lower() for word in ['study', 'research', 'data', 'according', 'reported'])):
                
                confidence = _calculate_claim_confidence(sentence)
                
                if confidence >= 0.4:
                    claims.append({
                        "claim": sentence.strip(),
                        "confidence": confidence
                    })
        
        # Sort and limit
        claims.sort(key=lambda x: x["confidence"], reverse=True)
        return claims[:10]
        
    except Exception as e:
        logger.error(f"Error in fallback claim extraction: {e}")
        return [{
            "claim": "Claim extraction temporarily unavailable. Please try refreshing the page.",
            "confidence": 0.1
        }]

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