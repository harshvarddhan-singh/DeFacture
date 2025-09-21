"""
Test Hugging Face API Integration for DeFacture

This script tests that the Hugging Face API is correctly calling the model
using the provided access token. Initially we tried using flan-t5-base,
but found that the facebook/bart-large-cnn model works more reliably with
the current API token.
"""

import os
import requests
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def test_huggingface_api_call():
    """Test direct call to Hugging Face API with bart-large-cnn model"""
    
    # Load environment variables
    load_dotenv()
    
    # Get API token - first try HF_TOKEN, then fall back to HUGGINGFACE_API_KEY
    api_token = os.environ.get("HF_TOKEN", "")
    if not api_token:
        api_token = os.environ.get("HUGGINGFACE_API_KEY", "")
        if not api_token:
            logger.error("No Hugging Face API token found in environment variables")
            return False
    
    # Print token details (first 5 chars only for security)
    token_preview = api_token[:5] + "..." if api_token else "None"
    logger.info(f"Using API token starting with: {token_preview}")
    
    # First verify token is valid by checking model list
    VALIDATE_URL = "https://huggingface.co/api/whoami"
    
    logger.info("Checking Hugging Face API token validity...")
    validate_headers = {
        "Authorization": f"Bearer {api_token}"
    }
    
    try:
        validate_response = requests.get(VALIDATE_URL, headers=validate_headers)
        logger.info(f"Validation response status: {validate_response.status_code}")
        if validate_response.status_code == 200:
            logger.info(f"Token validated: {validate_response.text[:100]}...")
        else:
            logger.warning(f"Token validation response: {validate_response.text[:100]}...")
    except Exception as e:
        logger.error(f"Error validating token: {str(e)}")
    
    # API endpoint for BART-CNN model (confirmed to work with token)
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    
    # Test text
    test_text = "Summarize the following: Climate change is causing global temperatures to rise, leading to melting ice caps and rising sea levels."
    
    # Request payload
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": test_text,
        "parameters": {
            "max_length": 100,
            "temperature": 0.7,
            "do_sample": True
        }
    }
    
    try:
        # Make the API request
        logger.info("Making request to Hugging Face API bart-large-cnn model")
        response = requests.post(API_URL, headers=headers, json=payload)
        
        # Log full response for debugging
        logger.info(f"Response status code: {response.status_code}")
        logger.info(f"Response headers: {response.headers}")
        
        # Check if request was successful
        if response.status_code == 200:
            response_data = response.json()
            logger.info("API request successful!")
            logger.info(f"Response type: {type(response_data)}")
            logger.info(f"Response content: {response_data}")
            
            # Check if response format matches what we expect for flan-t5-base
            # Handle different possible response formats:
            # 1. List of dicts with generated_text (like GPT-2)
            # 2. List of strings (like some T5 models)
            # 3. List of dicts with summary_text (like BART)
            if isinstance(response_data, list) and len(response_data) > 0:
                if isinstance(response_data[0], dict):
                    # Try both generated_text and summary_text keys
                    generated_text = response_data[0].get("generated_text", response_data[0].get("summary_text", ""))
                    logger.info(f"Generated text: {generated_text}")
                elif isinstance(response_data[0], str):
                    # Handle direct string output
                    generated_text = response_data[0]
                    logger.info(f"Generated text: {generated_text}")
                else:
                    logger.warning(f"Unexpected response item type: {type(response_data[0])}")
                    generated_text = str(response_data[0])
                
                if generated_text:
                    logger.info("✅ Test PASSED: Successfully generated text from bart-large-cnn model")
                    return True
                else:
                    logger.error("Generated text is empty")
                    return False
            else:
                logger.error(f"Unexpected response format: {response_data}")
                return False
        else:
            logger.error(f"API request failed with status code: {response.status_code}")
            logger.error(f"Response content: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error making API request: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("Starting Hugging Face API flan-t5-base model test")
    success = test_huggingface_api_call()
    
    if success:
        logger.info("✅ Test PASSED: Successfully called bart-large-cnn model using Hugging Face API")
    else:
        logger.error("❌ Test FAILED: Could not call bart-large-cnn model using Hugging Face API")