"""
Keyword Extraction Utility for Related Articles

This module provides functions for extracting keywords from article content,
which can be used for related article searches.
"""

import re
import logging
import string
from typing import List, Dict, Set, Optional
from collections import Counter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import optional dependencies
try:
    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    
    # Download required NLTK data if not already available
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
    
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)
        
    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        nltk.download('wordnet', quiet=True)
        
    # Try to download named entity recognition data
    try:
        nltk.data.find('chunkers/maxent_ne_chunker')
        nltk.data.find('taggers/averaged_perceptron_tagger')
        nltk.data.find('corpora/words')
    except LookupError:
        try:
            nltk.download('maxent_ne_chunker', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
            nltk.download('words', quiet=True)
        except Exception as e:
            logger.warning(f"Error downloading NER data: {str(e)}")
    
    # Fix for averaged_perceptron_tagger_eng error
    try:
        # This is a specific error that occurs in some environments
        nltk.data.find('taggers/averaged_perceptron_tagger_eng')
    except LookupError:
        try:
            # Try to manually download the required resource
            nltk.download('averaged_perceptron_tagger', quiet=True)
        except Exception as e:
            logger.warning(f"Error downloading tagger: {str(e)}")
        
    HAVE_NLTK = True
except ImportError:
    HAVE_NLTK = False
    logger.warning("NLTK not available. Using basic keyword extraction.")
    
# Try to import scikit-learn for TF-IDF
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    HAVE_SKLEARN = True
except ImportError:
    HAVE_SKLEARN = False
    logger.warning("scikit-learn not available. TF-IDF keyword extraction disabled.")

def extract_keywords_tfidf(text: str, max_keywords: int = 10) -> List[str]:
    """
    Extract keywords using TF-IDF if scikit-learn is available.
    
    Parameters:
    -----------
    text : str
        Text to extract keywords from
    max_keywords : int
        Maximum number of keywords to return
        
    Returns:
    --------
    List[str]
        List of keywords
    """
    if not HAVE_SKLEARN:
        logger.warning("scikit-learn not available. Falling back to regular extraction.")
        return extract_keywords_nltk(text, max_keywords) if HAVE_NLTK else extract_keywords_basic(text, max_keywords)
    
    try:
        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer(
            max_features=max_keywords,
            stop_words='english',
            ngram_range=(1, 1)  # Only single words
        )
        
        # Fit and transform the text
        tfidf_matrix = vectorizer.fit_transform([text])
        
        # Get feature names
        feature_names = vectorizer.get_feature_names_out()
        
        # Get TF-IDF scores
        tfidf_scores = tfidf_matrix.toarray()[0]
        
        # Pair words with scores
        word_scores = list(zip(feature_names, tfidf_scores))
        
        # Sort by score
        word_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Get top keywords
        keywords = [word for word, _ in word_scores[:max_keywords]]
        
        return keywords
    except Exception as e:
        logger.warning(f"Error in TF-IDF extraction: {str(e)}. Falling back to regular extraction.")
        return extract_keywords_nltk(text, max_keywords) if HAVE_NLTK else extract_keywords_basic(text, max_keywords)

def extract_named_entities(text: str, max_entities: int = 10) -> List[str]:
    """
    Extract named entities (people, organizations, locations) from text.
    
    Parameters:
    -----------
    text : str
        Text to extract named entities from
    max_entities : int
        Maximum number of entities to return
        
    Returns:
    --------
    List[str]
        List of named entities
    """
    # Skip NER if we've previously had an error
    if getattr(extract_named_entities, '_skip_ner', False):
        return []
        
    if not HAVE_NLTK:
        logger.warning("NLTK not available. Named entity extraction disabled.")
        return []
    
    # Suppress warning output for the specific error we're experiencing
    import logging as python_logging
    nltk_logger = python_logging.getLogger('nltk.tag')
    original_level = nltk_logger.level
    nltk_logger.setLevel(python_logging.ERROR)
    
    try:
        # Tokenize the text
        tokens = word_tokenize(text)
        
        # Try to tag tokens - this may fail with the specific error
        try:
            tagged = nltk.pos_tag(tokens)
        except LookupError:
            # Mark this function to skip in future calls
            extract_named_entities._skip_ner = True
            return []
        
        # Extract named entities
        entities = nltk.chunk.ne_chunk(tagged)
        
        # Extract entity names
        named_entities = []
        
        for chunk in entities:
            if hasattr(chunk, 'label'):
                entity_name = ' '.join(c[0] for c in chunk)
                if entity_name not in named_entities:
                    named_entities.append(entity_name)
        
        return named_entities[:max_entities]
    except Exception as e:
        # Check if it's the specific error we know about
        if "averaged_perceptron_tagger_eng" in str(e):
            # Mark this function to skip in future calls 
            extract_named_entities._skip_ner = True
            return []
        else:
            logger.warning(f"Error in named entity extraction: {str(e)}")
            return []
    finally:
        # Restore original logging level
        nltk_logger.setLevel(original_level)

def extract_keywords(article: Dict, max_keywords: int = 10, method: str = "hybrid") -> List[str]:
    """
    Extract keywords from an article using specified method.
    
    Parameters:
    -----------
    article : Dict
        Dictionary containing article data (title, content)
    max_keywords : int
        Maximum number of keywords to return
    method : str
        Method to use: 'basic', 'nltk', 'tfidf', 'entity', or 'hybrid'
        
    Returns:
    --------
    List[str]
        List of keywords
    """
    # Extract title and content from article
    title = article.get('title', '')
    content = article.get('content', '')
    
    # Combine title and content, giving more weight to title
    text = title + ". " + title + ". " + content
    
    # Extract keywords based on method
    if method == "basic" or not HAVE_NLTK:
        return extract_keywords_basic(text, max_keywords)
    elif method == "nltk":
        return extract_keywords_nltk(text, max_keywords)
    elif method == "tfidf" and HAVE_SKLEARN:
        return extract_keywords_tfidf(text, max_keywords)
    elif method == "entity":
        entities = extract_named_entities(text, max_keywords)
        if not entities:  # Fall back if no entities found
            return extract_keywords_nltk(text, max_keywords)
        return entities
    else:  # hybrid (default) or fallback
        # Hybrid approach combining different methods
        keywords = []
        
        # Get keywords from different methods
        basic_kw = extract_keywords_basic(text, max_keywords // 2)
        
        if HAVE_NLTK:
            nltk_kw = extract_keywords_nltk(text, max_keywords // 2)
            entities = extract_named_entities(text, max_keywords // 3)
        else:
            nltk_kw = []
            entities = []
            
        if HAVE_SKLEARN:
            tfidf_kw = extract_keywords_tfidf(text, max_keywords // 2)
        else:
            tfidf_kw = []
            
        # Combine and deduplicate
        for kw in entities + tfidf_kw + nltk_kw + basic_kw:
            if kw not in keywords:
                keywords.append(kw)
                
        return keywords[:max_keywords]

def extract_keywords_nltk(text: str, max_keywords: int = 10) -> List[str]:
    """
    Extract keywords using NLTK.
    
    Parameters:
    -----------
    text : str
        Text to extract keywords from
    max_keywords : int
        Maximum number of keywords to return
        
    Returns:
    --------
    List[str]
        List of keywords
    """
    # Tokenize
    tokens = word_tokenize(text.lower())
    
    # Get stop words
    stop_words = set(stopwords.words('english'))
    
    # Add punctuation to stop words
    stop_words.update(list(string.punctuation))
    
    # Filter tokens
    filtered_tokens = [token for token in tokens if token not in stop_words 
                      and token.isalpha() 
                      and len(token) > 3]
    
    # Lemmatize tokens
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    
    # Get frequency
    word_freq = Counter(lemmatized_tokens)
    
    # Get top N keywords
    keywords = [word for word, _ in word_freq.most_common(max_keywords)]
    
    return keywords

def extract_keywords_basic(text: str, max_keywords: int = 10) -> List[str]:
    """
    Basic keyword extraction without NLTK.
    
    Parameters:
    -----------
    text : str
        Text to extract keywords from
    max_keywords : int
        Maximum number of keywords to return
        
    Returns:
    --------
    List[str]
        List of keywords
    """
    # Basic stopwords
    basic_stop_words = {
        'a', 'an', 'the', 'and', 'or', 'but', 'if', 'because', 'as', 'what',
        'when', 'where', 'how', 'which', 'who', 'whom', 'this', 'that', 'these',
        'those', 'then', 'just', 'so', 'than', 'such', 'both', 'through', 'about',
        'for', 'is', 'of', 'while', 'during', 'to', 'from', 'in', 'out', 'on', 
        'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there',
        'all', 'any', 'both', 'each', 'few', 'more', 'most', 'some', 'such', 'no',
        'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can',
        'will', 'don', 'should', 'now', 'they', 'them', 'their', 'what', 'which',
        'with', 'into', 'your', 'yours', 'would', 'could', 'should', 'shall'
    }
    
    # Lowercase and remove punctuation
    text = text.lower()
    for p in string.punctuation:
        text = text.replace(p, ' ')
    
    # Split into words
    words = text.split()
    
    # Filter words
    filtered_words = [word for word in words if word not in basic_stop_words 
                     and word.isalpha() 
                     and len(word) > 3]
    
    # Get word frequency
    word_freq = Counter(filtered_words)
    
    # Get top N keywords
    keywords = [word for word, _ in word_freq.most_common(max_keywords)]
    
    return keywords

def generate_search_query(article: Dict, max_query_length: int = 100, max_keywords: int = 10) -> str:
    """
    Generate a search query from an article using a mix of title and keywords.
    
    Parameters:
    -----------
    article : Dict
        Dictionary containing article data
    max_query_length : int
        Maximum length of the generated query string
    max_keywords : int
        Maximum number of keywords to include in query
        
    Returns:
    --------
    str
        Search query
    """
    # Start with the article title if available
    title = article.get("title", "").strip()
    
    # Extract keywords
    keywords = extract_keywords(article, max_keywords)
    
    # Combine title and keywords
    if title:
        # If title is available, use it as the base and add unique keywords
        query_parts = [title]
        
        # Add keywords not in the title
        for keyword in keywords:
            if keyword.lower() not in title.lower() and len(' '.join(query_parts)) < max_query_length:
                query_parts.append(keyword)
    else:
        # If no title, just use keywords
        query_parts = keywords
    
    # Join the parts and trim to max length
    query = ' '.join(query_parts)
    if len(query) > max_query_length:
        query = query[:max_query_length].rsplit(' ', 1)[0]
    
    return query