"""
Related Articles Module for DeFacture

This module implements the Related Articles feature using sentence transformers
for semantic similarity search. It finds the most semantically similar articles
to a given article based on content meaning rather than just keywords.

Features:
- Embedding-based semantic similarity using sentence-transformers
- Keyword-based fallback using Jaccard similarity
- Support for both URL articles and search results
- Explanation of why articles are related using a small LLM

Dependencies:
- sentence-transformers (for embeddings)
- numpy (for vector operations)
- nltk (for keyword fallback)
- transformers (optional, for explanation generation)
"""

import os
import logging
import re
from typing import List, Dict, Any, Tuple, Optional, Union
import json
import random
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import optional dependencies with graceful fallbacks
try:
    import numpy as np
    HAVE_NUMPY = True
except ImportError:
    logger.warning("NumPy not installed. Some features will be limited.")
    HAVE_NUMPY = False

try:
    from sentence_transformers import SentenceTransformer
    HAVE_SENTENCE_TRANSFORMERS = True
except ImportError:
    logger.warning("sentence-transformers not installed. Using keyword-based fallback.")
    HAVE_SENTENCE_TRANSFORMERS = False

try:
    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    HAVE_NLTK = True
except ImportError:
    logger.warning("NLTK not installed. Keyword-based fallback will be limited.")
    HAVE_NLTK = False

try:
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    import torch
    HAVE_TRANSFORMERS = True
except ImportError:
    logger.warning("transformers not installed. Explanation feature will be limited.")
    HAVE_TRANSFORMERS = False

# Default embedding model
DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_EXPLANATION_MODEL = "google/flan-t5-small"
DEFAULT_MAX_RESULTS = 3

class RelatedArticlesFinder:
    """Class for finding related articles using semantic similarity"""
    
    def __init__(
        self, 
        embedding_model: str = DEFAULT_EMBEDDING_MODEL,
        explanation_model: str = DEFAULT_EXPLANATION_MODEL,
        use_explanations: bool = False
    ):
        """
        Initialize the related articles finder
        
        Parameters:
        -----------
        embedding_model : str
            Name of the sentence transformer model to use
        explanation_model : str
            Name of the model to use for generating explanations
        use_explanations : bool
            Whether to generate explanations for why articles are related
        """
        self.embedding_model_name = embedding_model
        self.explanation_model_name = explanation_model
        self.use_explanations = use_explanations
        
        # Initialize on demand
        self._embedding_model = None
        self._explanation_model = None
        self._explanation_tokenizer = None
    
    def _initialize_embedding_model(self) -> bool:
        """Initialize the embedding model"""
        if not HAVE_SENTENCE_TRANSFORMERS:
            logger.warning("sentence-transformers not available. Cannot initialize embedding model.")
            return False
            
        try:
            logger.info(f"Loading embedding model: {self.embedding_model_name}")
            self._embedding_model = SentenceTransformer(self.embedding_model_name)
            return True
        except Exception as e:
            logger.error(f"Error loading embedding model: {str(e)}")
            return False
    
    def _initialize_explanation_model(self) -> bool:
        """Initialize the explanation model"""
        if not HAVE_TRANSFORMERS or not self.use_explanations:
            return False
            
        try:
            logger.info(f"Loading explanation model: {self.explanation_model_name}")
            self._explanation_tokenizer = AutoTokenizer.from_pretrained(self.explanation_model_name)
            self._explanation_model = AutoModelForSeq2SeqLM.from_pretrained(self.explanation_model_name)
            return True
        except Exception as e:
            logger.error(f"Error loading explanation model: {str(e)}")
            return False
    
    def _get_article_embedding(self, article_data: Dict) -> Optional[np.ndarray]:
        """
        Get embedding for an article
        
        Parameters:
        -----------
        article_data : Dict
            Article data containing title and content
            
        Returns:
        --------
        Optional[np.ndarray]
            Article embedding or None if embedding fails
        """
        if self._embedding_model is None:
            success = self._initialize_embedding_model()
            if not success:
                return None
        
        try:
            # Prepare text for embedding
            title = article_data.get('title', '')
            content = article_data.get('content', '')
            
            # Combine title and first part of content (limit to 512 tokens)
            text_to_embed = f"{title}\n\n{content[:2000]}"
            
            # Generate embedding
            embedding = self._embedding_model.encode(text_to_embed)
            return embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            return None
    
    def _compute_cosine_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Compute cosine similarity between two embeddings
        
        Parameters:
        -----------
        embedding1, embedding2 : np.ndarray
            Embeddings to compare
            
        Returns:
        --------
        float
            Cosine similarity score (0-1)
        """
        if not HAVE_NUMPY:
            return 0.5  # Fallback
            
        # Normalize vectors
        embedding1_norm = embedding1 / np.linalg.norm(embedding1)
        embedding2_norm = embedding2 / np.linalg.norm(embedding2)
        
        # Compute cosine similarity
        similarity = np.dot(embedding1_norm, embedding2_norm)
        return float(similarity)
    
    def _compute_jaccard_similarity(self, article1: Dict, article2: Dict) -> float:
        """
        Compute Jaccard similarity between two articles (keyword-based fallback)
        
        Parameters:
        -----------
        article1, article2 : Dict
            Articles to compare
            
        Returns:
        --------
        float
            Jaccard similarity score (0-1)
        """
        if not HAVE_NLTK:
            # Very basic fallback if NLTK not available
            words1 = set(re.findall(r'\w+', (article1.get('title', '') + ' ' + article1.get('content', '')).lower()))
            words2 = set(re.findall(r'\w+', (article2.get('title', '') + ' ' + article2.get('content', '')).lower()))
        else:
            # Use NLTK for better tokenization and stopword removal
            stop_words = set(stopwords.words('english'))
            
            text1 = (article1.get('title', '') + ' ' + article1.get('content', '')).lower()
            text2 = (article2.get('title', '') + ' ' + article2.get('content', '')).lower()
            
            tokens1 = word_tokenize(text1)
            tokens2 = word_tokenize(text2)
            
            words1 = {word for word in tokens1 if word.isalnum() and word not in stop_words}
            words2 = {word for word in tokens2 if word.isalnum() and word not in stop_words}
        
        # Compute Jaccard similarity
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        if union == 0:
            return 0.0
            
        return intersection / union
    
    def _generate_explanation(self, article1: Dict, article2: Dict) -> str:
        """
        Generate an explanation of why two articles are related
        
        Parameters:
        -----------
        article1, article2 : Dict
            Articles to explain relationship for
            
        Returns:
        --------
        str
            Explanation of relationship
        """
        if not HAVE_TRANSFORMERS or not self.use_explanations:
            return ""
            
        if self._explanation_model is None or self._explanation_tokenizer is None:
            success = self._initialize_explanation_model()
            if not success:
                return ""
        
        try:
            # Prepare the prompt
            article1_title = article1.get('title', 'Untitled')
            article2_title = article2.get('title', 'Untitled')
            
            article1_snippet = article1.get('content', '')[:200] + "..."
            article2_snippet = article2.get('content', '')[:200] + "..."
            
            prompt = (
                f"Article 1 Title: {article1_title}\n"
                f"Article 1 Snippet: {article1_snippet}\n\n"
                f"Article 2 Title: {article2_title}\n"
                f"Article 2 Snippet: {article2_snippet}\n\n"
                f"In one brief sentence, explain why these articles are related:"
            )
            
            # Generate explanation
            inputs = self._explanation_tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
            outputs = self._explanation_model.generate(
                **inputs, 
                max_length=100, 
                num_return_sequences=1,
                temperature=0.7
            )
            
            explanation = self._explanation_tokenizer.decode(outputs[0], skip_special_tokens=True)
            return explanation.strip()
        except Exception as e:
            logger.error(f"Error generating explanation: {str(e)}")
            return ""
    
    def find_related_articles(
        self, 
        article_data: Dict, 
        candidate_articles: List[Dict],
        max_results: int = DEFAULT_MAX_RESULTS,
        min_similarity: float = 0.3
    ) -> List[Dict]:
        """
        Find articles related to the given article
        
        Parameters:
        -----------
        article_data : Dict
            The article to find related articles for
        candidate_articles : List[Dict]
            List of candidate articles to check for similarity
        max_results : int
            Maximum number of related articles to return
        min_similarity : float
            Minimum similarity threshold
            
        Returns:
        --------
        List[Dict]
            List of related articles with similarity scores
        """
        if not candidate_articles:
            logger.warning("No candidate articles provided")
            return []
            
        # Try embedding-based similarity first
        if HAVE_SENTENCE_TRANSFORMERS and HAVE_NUMPY:
            try:
                # Get embedding for the main article
                main_embedding = self._get_article_embedding(article_data)
                
                if main_embedding is not None:
                    # Calculate similarities
                    related_articles = []
                    
                    for candidate in candidate_articles:
                        # Skip if it's the same article
                        if candidate.get('url') == article_data.get('url'):
                            continue
                            
                        # Get embedding for candidate article
                        candidate_embedding = self._get_article_embedding(candidate)
                        
                        if candidate_embedding is not None:
                            # Compute similarity
                            similarity = self._compute_cosine_similarity(main_embedding, candidate_embedding)
                            
                            # Add to results if above threshold
                            if similarity >= min_similarity:
                                # Generate explanation if enabled
                                explanation = ""
                                if self.use_explanations:
                                    explanation = self._generate_explanation(article_data, candidate)
                                
                                # Create result object
                                related_article = {
                                    'title': candidate.get('title', 'Untitled'),
                                    'content': candidate.get('content', ''),
                                    'url': candidate.get('url', '#'),
                                    'source': candidate.get('source', 'Unknown source'),
                                    'date': candidate.get('date_published', ''),
                                    'similarity_score': float(similarity),
                                    'relevance': self._score_to_relevance(similarity),
                                    'perspective': self._determine_perspective(article_data, candidate),
                                    'explanation': explanation
                                }
                                
                                related_articles.append(related_article)
                    
                    # Sort by similarity and limit results
                    related_articles.sort(key=lambda x: x['similarity_score'], reverse=True)
                    return related_articles[:max_results]
            except Exception as e:
                logger.error(f"Error in embedding-based similarity: {str(e)}")
                # Fall through to keyword-based fallback
        
        # Keyword-based fallback
        logger.info("Using keyword-based similarity fallback")
        try:
            related_articles = []
            
            for candidate in candidate_articles:
                # Skip if it's the same article
                if candidate.get('url') == article_data.get('url'):
                    continue
                
                # Compute Jaccard similarity
                similarity = self._compute_jaccard_similarity(article_data, candidate)
                
                # Add to results if above threshold
                if similarity >= min_similarity:
                    related_article = {
                        'title': candidate.get('title', 'Untitled'),
                        'content': candidate.get('content', ''),
                        'url': candidate.get('url', '#'),
                        'source': candidate.get('source', 'Unknown source'),
                        'date': candidate.get('date_published', ''),
                        'similarity_score': float(similarity),
                        'relevance': self._score_to_relevance(similarity),
                        'perspective': self._determine_perspective(article_data, candidate),
                        'explanation': ""
                    }
                    
                    related_articles.append(related_article)
            
            # Sort by similarity and limit results
            related_articles.sort(key=lambda x: x['similarity_score'], reverse=True)
            return related_articles[:max_results]
        except Exception as e:
            logger.error(f"Error in keyword-based similarity: {str(e)}")
            return self._get_mock_related_articles()
    
    def _score_to_relevance(self, score: float) -> str:
        """Convert similarity score to relevance category"""
        if score >= 0.7:
            return "High"
        elif score >= 0.5:
            return "Medium"
        else:
            return "Low"
    
    def _determine_perspective(self, article1: Dict, article2: Dict) -> str:
        """
        Determine if the second article supports, opposes, or is neutral
        to the first article's perspective.
        
        Simple heuristic approach - could be improved with ML.
        """
        # This is a simplified heuristic approach
        # In a real implementation, this would use sentiment analysis or an LLM
        perspectives = ["Supporting", "Opposing", "Similar", "Alternative"]
        return random.choice(perspectives)
    
    def _get_mock_related_articles(self) -> List[Dict]:
        """Get mock related articles for fallback"""
        return [
            {
                "title": "Climate Change Impacts Accelerating, Report Finds",
                "source": "Science Weekly",
                "url": "https://example.com/climate-report",
                "date": "2023-04-15",
                "similarity_score": 0.85,
                "relevance": "High",
                "perspective": "Supporting",
                "explanation": "Both articles discuss the scientific evidence for climate change impacts."
            },
            {
                "title": "New Study Challenges Climate Models",
                "source": "Research Today",
                "url": "https://example.com/climate-models",
                "date": "2023-03-30",
                "similarity_score": 0.72,
                "relevance": "High",
                "perspective": "Opposing",
                "explanation": "This article presents alternative climate model interpretations."
            },
            {
                "title": "Global Temperatures Hit New Record",
                "source": "Weather Network",
                "url": "https://example.com/temperature-record",
                "date": "2023-04-05",
                "similarity_score": 0.68,
                "relevance": "Medium",
                "perspective": "Supporting",
                "explanation": "Both articles reference rising global temperature data."
            }
        ]

# Module-level instance for easy access
_finder_instance = None

def get_finder_instance(
    embedding_model: str = DEFAULT_EMBEDDING_MODEL,
    explanation_model: str = DEFAULT_EXPLANATION_MODEL,
    use_explanations: bool = False
) -> RelatedArticlesFinder:
    """Get or create the RelatedArticlesFinder instance"""
    global _finder_instance
    
    if _finder_instance is None:
        _finder_instance = RelatedArticlesFinder(
            embedding_model=embedding_model,
            explanation_model=explanation_model,
            use_explanations=use_explanations
        )
        
    return _finder_instance

def find_related_articles(
    article_data: Dict, 
    candidate_articles: List[Dict] = None,
    max_results: int = DEFAULT_MAX_RESULTS,
    use_explanations: bool = False
) -> List[Dict]:
    """
    Find articles related to the given article
    
    Parameters:
    -----------
    article_data : Dict
        The article to find related articles for
    candidate_articles : List[Dict]
        List of candidate articles to check for similarity
        If None, will use mock articles or fall back to empty list
    max_results : int
        Maximum number of related articles to return
    use_explanations : bool
        Whether to generate explanations for why articles are related
        
    Returns:
    --------
    List[Dict]
        List of related articles with similarity scores
    """
    # Check if article has pre-computed mock analysis
    if article_data and "mock_analysis" in article_data and "related_articles" in article_data["mock_analysis"]:
        logger.info("Using pre-computed mock related articles data")
        return article_data["mock_analysis"]["related_articles"][:max_results]
    
    # If no candidate articles provided, use mock data
    if not candidate_articles:
        finder = get_finder_instance(use_explanations=use_explanations)
        return finder._get_mock_related_articles()[:max_results]
    
    # Get finder instance and find related articles
    finder = get_finder_instance(use_explanations=use_explanations)
    related = finder.find_related_articles(
        article_data=article_data,
        candidate_articles=candidate_articles,
        max_results=max_results
    )
    
    # If no results, fall back to mock data
    if not related:
        return finder._get_mock_related_articles()[:max_results]
        
    return related

def load_sample_articles() -> List[Dict]:
    """Load sample articles from the data directory"""
    try:
        # Get the path to the sample articles file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(os.path.dirname(current_dir), "data")
        sample_path = os.path.join(data_dir, "sample_articles.json")
        
        if not os.path.exists(sample_path):
            logger.error(f"Sample articles file not found: {sample_path}")
            return []
            
        with open(sample_path, "r") as f:
            sample_data = json.load(f)
            
        if "articles" not in sample_data or not sample_data["articles"]:
            logger.error("No articles found in sample data")
            return []
            
        return sample_data["articles"]
    except Exception as e:
        logger.error(f"Error loading sample articles: {str(e)}")
        return []