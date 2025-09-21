"""
Test Hugging Face API for DeFacture

This script tests the Hugging Face API implementation for context analysis.
It verifies that the API connection is working properly and that the
context analysis function returns expected results.
"""

import os
import sys
import logging
from pathlib import Path

# Add parent directory to path so we can import project modules
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Import project modules
from tools.huggingface_api import huggingface_context_analysis
from tools.analysis import context_analysis_chain
from config.config import API_KEYS

def test_api_key_exists():
    """Test if the Hugging Face API key exists in environment"""
    api_key = API_KEYS.get("huggingface_api", "")
    
    if not api_key:
        logger.error("❌ Hugging Face API key not found")
        logger.info("ℹ️  Run 'python setup_huggingface_api.py' to configure your API key")
        return False
    else:
        logger.info("✅ Hugging Face API key found")
        return True

def test_direct_api_call():
    """Test direct call to the Hugging Face API"""
    test_article = """
    Climate scientists have found that global warming is causing extreme weather events 
    like hurricanes and floods to become more frequent and intense. Studies published in 
    peer-reviewed journals show a clear correlation between rising temperatures and 
    increased storm activity.
    """
    
    logger.info("Testing direct API call to Hugging Face...")
    
    try:
        result = huggingface_context_analysis(text=test_article)
        
        if result and isinstance(result, dict):
            logger.info("✅ Direct API call successful")
            logger.info(f"Response content type: {type(result)}")
            # Log a snippet of the result to avoid exposing full API response
            logger.info(f"Response snippet: {str(result)[:100]}...")
            return True
        else:
            logger.error(f"❌ Direct API call returned unexpected result: {result}")
            return False
    except Exception as e:
        logger.error(f"❌ Direct API call failed: {str(e)}")
        return False

def test_context_analysis_chain():
    """Test the context analysis chain with Hugging Face integration"""
    test_article = """
    A recent study claims that drinking coffee increases lifespan by up to 10 years.
    Researchers conducted a 30-year longitudinal study with over 500,000 participants
    and found that those who drank 3-5 cups of coffee daily lived significantly longer
    than non-coffee drinkers.
    """
    
    logger.info("Testing context analysis chain with Hugging Face integration...")
    
    try:
        result = context_analysis_chain(text=test_article)
        
        if result and isinstance(result, dict):
            logger.info("✅ Context analysis chain successful")
            # Print relevant parts of the analysis
            if "claims" in result:
                logger.info(f"Claims detected: {len(result['claims'])}")
                for i, claim in enumerate(result['claims']):
                    logger.info(f"Claim {i+1}: {claim[:100]}...")
            
            if "context_analysis" in result:
                logger.info(f"Context analysis: {result['context_analysis'][:150]}...")
            
            return True
        else:
            logger.error(f"❌ Context analysis chain returned unexpected result: {result}")
            return False
    except Exception as e:
        logger.error(f"❌ Context analysis chain failed: {str(e)}")
        return False

def run_all_tests():
    """Run all tests and return overall success status"""
    logger.info("🧪 Starting Hugging Face API tests...")
    
    tests = [
        ("API key exists", test_api_key_exists),
        ("Direct API call", test_direct_api_call),
        ("Context analysis chain", test_context_analysis_chain)
    ]
    
    results = []
    
    for name, test_func in tests:
        logger.info(f"\n🔍 Running test: {name}")
        result = test_func()
        results.append(result)
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"Test '{name}': {status}")
    
    # Print summary
    logger.info("\n📋 Test Summary:")
    for i, (name, _) in enumerate(tests):
        status = "✅ PASSED" if results[i] else "❌ FAILED"
        logger.info(f"{status} - {name}")
    
    # Calculate overall result
    passed = sum(results)
    total = len(results)
    success_rate = (passed / total) * 100 if total > 0 else 0
    
    logger.info(f"\n🎯 Overall result: {passed}/{total} tests passed ({success_rate:.1f}%)")
    
    if all(results):
        logger.info("🎉 All tests passed! Hugging Face API integration is working correctly.")
        return True
    else:
        logger.warning("⚠️ Some tests failed. Check the logs for details.")
        return False

if __name__ == "__main__":
    run_all_tests()