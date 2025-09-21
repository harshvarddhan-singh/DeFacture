"""
Test Related Articles Feature

This script tests the new related articles functionality with both embedding-based
and keyword-based similarity approaches.
"""

import os
import sys
import json
import logging
from pathlib import Path

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_sample_articles():
    """Load sample articles for testing"""
    sample_path = os.path.join(parent_dir, "data", "sample_articles.json")
    
    if not os.path.exists(sample_path):
        logger.error(f"Sample articles file not found: {sample_path}")
        return []
        
    try:
        with open(sample_path, "r") as f:
            data = json.load(f)
            
        if "articles" not in data:
            logger.error("No articles found in sample data")
            return []
            
        return data["articles"]
    except Exception as e:
        logger.error(f"Error loading sample articles: {str(e)}")
        return []

def test_embedding_similarity():
    """Test embedding-based similarity"""
    try:
        from tools.related_articles import find_related_articles
        
        # Load sample articles
        articles = load_sample_articles()
        
        if not articles:
            logger.error("No sample articles available")
            return
            
        # Use the first article as the test article
        test_article = articles[0]
        logger.info(f"Finding articles related to: {test_article.get('title', 'Unknown title')}")
        
        # Find related articles using embedding-based similarity
        related = find_related_articles(
            article_data=test_article,
            candidate_articles=articles,
            max_results=3,
            use_explanations=True
        )
        
        # Print results
        logger.info(f"Found {len(related)} related articles:")
        for i, article in enumerate(related):
            logger.info(f"{i+1}. {article.get('title', 'Untitled')}")
            logger.info(f"   Source: {article.get('source', 'Unknown')}")
            logger.info(f"   Similarity: {article.get('similarity_score', 0):.2f}")
            logger.info(f"   Relevance: {article.get('relevance', 'Unknown')}")
            logger.info(f"   Perspective: {article.get('perspective', 'Unknown')}")
            
            if article.get('explanation'):
                logger.info(f"   Explanation: {article.get('explanation')}")
                
            logger.info("---")
            
        return related
    except ImportError as e:
        logger.error(f"Error importing modules: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Error testing embedding similarity: {str(e)}")
        import traceback
        traceback.print_exc()
        return []

def test_keyword_similarity():
    """Test keyword-based similarity fallback"""
    try:
        # Temporarily rename/move sentence_transformers to force fallback
        import sys
        sentence_transformers_modules = {}
        
        for module_name in list(sys.modules.keys()):
            if 'sentence_transformers' in module_name:
                sentence_transformers_modules[module_name] = sys.modules[module_name]
                del sys.modules[module_name]
        
        # Reload related_articles module to trigger fallback
        if 'tools.related_articles' in sys.modules:
            del sys.modules['tools.related_articles']
            
        # Import with fallback
        from tools.related_articles import find_related_articles
        
        # Load sample articles
        articles = load_sample_articles()
        
        if not articles:
            logger.error("No sample articles available")
            return
            
        # Use the first article as the test article
        test_article = articles[0]
        logger.info(f"Finding articles related to: {test_article.get('title', 'Unknown title')} (keyword fallback)")
        
        # Find related articles using keyword-based similarity
        related = find_related_articles(
            article_data=test_article,
            candidate_articles=articles,
            max_results=3,
            use_explanations=False
        )
        
        # Print results
        logger.info(f"Found {len(related)} related articles (keyword fallback):")
        for i, article in enumerate(related):
            logger.info(f"{i+1}. {article.get('title', 'Untitled')}")
            logger.info(f"   Source: {article.get('source', 'Unknown')}")
            logger.info(f"   Similarity: {article.get('similarity_score', 0):.2f}")
            logger.info(f"   Relevance: {article.get('relevance', 'Unknown')}")
            logger.info(f"   Perspective: {article.get('perspective', 'Unknown')}")
            logger.info("---")
        
        # Restore sentence_transformers modules
        for name, module in sentence_transformers_modules.items():
            sys.modules[name] = module
            
        return related
    except Exception as e:
        logger.error(f"Error testing keyword similarity: {str(e)}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == "__main__":
    logger.info("Testing Related Articles Feature")
    
    # Test embedding-based similarity
    logger.info("=== Testing Embedding-Based Similarity ===")
    embedding_results = test_embedding_similarity()
    
    # Test keyword-based similarity
    logger.info("\n=== Testing Keyword-Based Similarity (Fallback) ===")
    keyword_results = test_keyword_similarity()
    
    # Compare results
    logger.info("\n=== Results Comparison ===")
    
    if embedding_results and keyword_results:
        # Get titles for comparison
        embedding_titles = [a.get('title') for a in embedding_results]
        keyword_titles = [a.get('title') for a in keyword_results]
        
        # Find common titles
        common_titles = set(embedding_titles).intersection(set(keyword_titles))
        
        logger.info(f"Common articles between methods: {len(common_titles)}")
        for title in common_titles:
            logger.info(f"  - {title}")
            
        # Calculate Jaccard similarity between result sets
        jaccard = len(common_titles) / len(set(embedding_titles).union(set(keyword_titles)))
        logger.info(f"Result set similarity (Jaccard): {jaccard:.2f}")
        
    logger.info("\nTest completed.")