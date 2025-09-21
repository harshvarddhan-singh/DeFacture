"""
Test Summary Generation via Hugging Face API

This script tests the summary generation functionality of the Hugging Face API
integration in DeFacture.
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Add parent directory to path so we can import from tools
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.huggingface_api import generate_context_summary

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def test_summary_generation():
    """Test summary generation with a sample article text"""
    
    # Load environment variables
    load_dotenv()
    
    # Sample article text about climate change
    article_text = """
    Climate change is a pressing global issue that requires immediate action from governments, businesses, and individuals.
    The scientific consensus is clear that human activities are contributing to rising global temperatures. 
    According to the Intergovernmental Panel on Climate Change (IPCC), global temperatures have already risen 
    by about 1°C above pre-industrial levels and are continuing to increase. This warming is primarily driven 
    by greenhouse gas emissions from burning fossil fuels, deforestation, and industrial processes.
    
    The consequences of climate change are far-reaching and include more frequent extreme weather events, 
    rising sea levels, biodiversity loss, and threats to food and water security. These impacts 
    disproportionately affect vulnerable communities and developing countries that have contributed least to the problem.
    
    To address climate change effectively, we need a combination of mitigation strategies to reduce emissions 
    and adaptation measures to build resilience to unavoidable impacts. This includes transitioning to renewable energy, 
    improving energy efficiency, protecting and restoring natural carbon sinks like forests, and implementing 
    climate-smart agricultural practices.
    """
    
    # Test summary generation
    logger.info("Testing summary generation...")
    summary_text, success = generate_context_summary(article_text, "summary")
    
    logger.info(f"Success: {success}")
    if success:
        if summary_text:
            logger.info(f"Generated summary: {summary_text}")
        else:
            logger.warning("Summary was returned as empty but marked as successful!")
    else:
        logger.error(f"Failed to generate summary: {summary_text}")
    
    # Try again with a simpler text
    logger.info("\nTrying with a simpler text...")
    simple_text = "Climate change is causing global temperatures to rise, leading to melting ice caps and rising sea levels."
    summary_text, success = generate_context_summary(simple_text, "summary")
    
    logger.info(f"Success: {success}")
    if success:
        if summary_text:
            logger.info(f"Generated summary: {summary_text}")
        else:
            logger.warning("Summary was returned as empty but marked as successful!")
    else:
        logger.error(f"Failed to generate summary: {summary_text}")
    
    # Test missing context analysis
    logger.info("\nTesting missing context analysis...")
    missing_context, success = generate_context_summary(article_text, "missing_context")
    
    logger.info(f"Success: {success}")
    if success:
        if missing_context:
            logger.info(f"Missing context analysis: {missing_context}")
        else:
            logger.warning("Missing context was returned as empty but marked as successful!")
    else:
        logger.error(f"Failed to generate missing context analysis: {missing_context}")
    
if __name__ == "__main__":
    test_summary_generation()