"""
Hugging Face Inference API Integration for DeFacture

This module provides integration with the Hugging Face Inference API 
for article context analysis without requiring local model downloads.
"""

import os
import json
import requests
import logging
from typing import Dict, Optional, List, Any, Union, Tuple
from functools import lru_cache

# Try to load environment variables from .env
try:
    from dotenv import load_dotenv
    load_dotenv()
    logger = logging.getLogger(__name__)
    logger.info("Loaded .env file successfully")
except ImportError:
    pass
except Exception as e:
    pass

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_api_key() -> str:
    """Get Hugging Face API key from environment or config"""
    # First try HUGGINGFACE_API_KEY (primary)
    api_key = os.environ.get("HUGGINGFACE_API_KEY", "")
    
    # Then try HF_TOKEN (alternative)
    if not api_key:
        api_key = os.environ.get("HF_TOKEN", "")
        
    if not api_key:
        logger.warning("No Hugging Face API key found in environment")
        # Try to get from config if available
        try:
            from config.config import API_KEYS
            api_key = API_KEYS.get("huggingface_api", "")
        except (ImportError, AttributeError):
            pass
    
    return api_key

def get_best_model_for_task(task: str) -> str:
    """
    Get the best model for a specific task
    
    Parameters:
    -----------
    task : str
        The task to perform: "summary", "missing_context", "context_analysis"
        
    Returns:
    --------
    str
        The name of the best model for this task
    """
    # Define task-model mapping - using BART only for summarization
    # and mock data for context analysis since phi-2 isn't available via API
    task_models = {
        "summary": "bart",        # BART works well for summarization
        "missing_context": "mock", # Using mock data for context analysis
        "context_analysis": "mock" # Using mock data for context analysis
    }
    
    # Return the best model or default to BART if task not found
    return task_models.get(task, "bart")

@lru_cache(maxsize=32)
def huggingface_context_analysis(text: str, model: str = "phi-2") -> Dict:
    """
    Analyze article context using Hugging Face models
    
    Parameters:
    -----------
    text : str
        The article text to analyze
    model : str
        The model to use for analysis. Options: "phi-2" (local), "bart" (API), "mock"
        
    Returns:
    --------
    Dict
        Dictionary with perspective, bias_indicators, historical_context, and missing_context
    """
    logger.info(f"Starting context analysis using model: {model}")
    
    # Mock result - we'll use this if requested or if anything fails
    mock_result = {
        'perspective': 'The article presents information from multiple perspectives.',
        'bias_indicators': ['Use of emotive language', 'Selection of sources', 'Framing of the issue'],
        'historical_context': 'The article references historical events as context for current situations.',
        'missing_context': 'The article lacks details about alternative viewpoints and important related events.'
    }
    
    # Return mock data if requested
    if model == "mock":
        logger.info("Using mock context analysis data as requested")
        return mock_result
        
    # Use local phi-2 model if requested
    if model == "phi-2":
        try:
            # Import the local model module
            from tools.local_models import phi2_context_analysis
            logger.info("Using locally cached Phi-2 model for context analysis")
            return phi2_context_analysis(text)
        except ImportError:
            logger.error("Failed to import local_models module, falling back to mock data")
            return mock_result
        except Exception as e:
            logger.error(f"Error using local Phi-2 model: {str(e)}, falling back to mock data")
            return mock_result
    
    # Get API token
    api_token = get_api_key()
    if not api_token:
        logger.warning("Missing Hugging Face API key, falling back to mock data")
        return mock_result
    
    # Truncate text if it's too long (most models have context limits)
    max_chars = 4000 if model == "phi-2" else 2000
    truncated_text = text[:max_chars] if len(text) > max_chars else text
    
    # Define model-specific parameters and URLs
    model_configs = {
        "phi-2": {
            "url": "https://api-inference.huggingface.co/models/microsoft/phi-2",
            "prompt": f"""Analyze this article and provide:
1. PERSPECTIVE: What is the main perspective or viewpoint of this article?
2. BIAS INDICATORS: List 3 potential indicators of bias in this article, if any.
3. HISTORICAL CONTEXT: What historical context is relevant to understanding this article?
4. MISSING CONTEXT: What important information might be missing from this article?

ARTICLE: {truncated_text}

ANALYSIS:""",
            "max_length": 800,
            "temperature": 0.3
        },
        "bart": {
            "url": "https://api-inference.huggingface.co/models/facebook/bart-large-cnn",
            "prompt": f"Analyze this article: {truncated_text}",
            "max_length": 500,
            "temperature": 0.7
        }
    }
    
    # Use the specified model configuration
    if model not in model_configs:
        logger.warning(f"Model {model} not supported, falling back to phi-2")
        model = "phi-2"
        
    config = model_configs[model]
    API_URL = config["url"]
    
    # Set up headers
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    # Request payload
    payload = {
        "inputs": config["prompt"],
        "parameters": {
            "max_length": config["max_length"],
            "temperature": config["temperature"],
            "do_sample": True
        }
    }
    
    try:
        # Make the API request
        logger.info(f"Making request to {API_URL}")
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        # Parse the response
        response_data = response.json()
        logger.info(f"Response received: {response_data[:100]}...")
        
        if isinstance(response_data, list) and len(response_data) > 0:
            # Extract the generated text
            if "summary_text" in response_data[0]:
                generated_text = response_data[0]["summary_text"]
            elif "generated_text" in response_data[0]:
                generated_text = response_data[0]["generated_text"]
            else:
                logger.warning(f"Unexpected response format: {response_data}")
                return mock_result
                
            logger.info(f"Generated text: {generated_text[:100]}...")
            
            # Parse the generated text into our expected format
            try:
                if model == "phi-2":
                    # Parse structured output from Phi-2
                    result = {
                        'perspective': '',
                        'bias_indicators': [],
                        'historical_context': '',
                        'missing_context': ''
                    }
                    
                    # Look for section headers in the text
                    sections = {
                        'perspective': ['perspective:', '1. perspective', 'main perspective'],
                        'bias_indicators': ['bias indicators:', '2. bias', 'potential bias'],
                        'historical_context': ['historical context:', '3. historical', 'relevant context'],
                        'missing_context': ['missing context:', '4. missing', 'important information']
                    }
                    
                    lines = generated_text.split('\n')
                    current_section = None
                    
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                            
                        # Check if this line starts a new section
                        found_section = False
                        for section, markers in sections.items():
                            if any(marker.lower() in line.lower() for marker in markers):
                                current_section = section
                                found_section = True
                                # Remove the header from the content
                                for marker in markers:
                                    if marker.lower() in line.lower():
                                        content = line.lower().replace(marker.lower(), '', 1).strip()
                                        if content:
                                            if section == 'bias_indicators':
                                                if result[section] == []:
                                                    result[section] = [content]
                                                else:
                                                    result[section].append(content)
                                            else:
                                                result[section] = content
                                break
                        
                        # If we're in a section but didn't find a new section header
                        if not found_section and current_section:
                            if current_section == 'bias_indicators':
                                # Check if this is a list item
                                if line.startswith('-') or line.startswith('•') or (len(line) >= 2 and line[0].isdigit() and line[1] in ['.', ')']):
                                    item = line[2:].strip() if line[1] in ['.', ')'] else line[1:].strip()
                                    result['bias_indicators'].append(item)
                                # Otherwise add to the existing list
                                elif result['bias_indicators']:
                                    result['bias_indicators'][-1] += ' ' + line
                            else:
                                if result[current_section]:
                                    result[current_section] += ' ' + line
                                else:
                                    result[current_section] = line
                    
                    # Ensure all sections have content
                    for key in result:
                        if not result[key]:
                            if key == 'bias_indicators':
                                result[key] = ["No clear bias indicators identified"]
                            else:
                                result[key] = f"No {key.replace('_', ' ')} identified"
                                
                    # Ensure bias_indicators is a list
                    if not isinstance(result['bias_indicators'], list):
                        if isinstance(result['bias_indicators'], str):
                            result['bias_indicators'] = [result['bias_indicators']]
                        else:
                            result['bias_indicators'] = ["No clear bias indicators identified"]
                            
                    return result
                    
                else:
                    # For BART or other models, just use a simple approach
                    # Split by newlines and try to guess the sections
                    paragraphs = generated_text.split('\n')
                    if len(paragraphs) == 1:
                        paragraphs = generated_text.split('. ')
                    
                    # Create default result
                    result = {
                        'perspective': paragraphs[0] if len(paragraphs) > 0 else "No perspective identified",
                        'bias_indicators': [paragraphs[1]] if len(paragraphs) > 1 else ["No clear bias indicators identified"],
                        'historical_context': paragraphs[2] if len(paragraphs) > 2 else "No historical context identified",
                        'missing_context': paragraphs[3] if len(paragraphs) > 3 else "No missing context identified"
                    }
                    
                    return result
                    
            except Exception as e:
                logger.error(f"Error parsing model output: {str(e)}")
                return mock_result
        else:
            logger.warning(f"Unexpected response format: {response_data}")
            return mock_result
            
    except Exception as e:
        logger.error(f"Error with Hugging Face API: {str(e)}")
        return mock_result


def generate_context_summary(article_text: str, summary_type: str = "summary", model: str = "bart") -> Tuple[str, bool]:
    """
    Generate a summary or missing context analysis for an article using Hugging Face's Inference API
    
    Parameters:
    -----------
    article_text : str
        The article text to summarize or analyze
    summary_type : str
        Type of summary to generate: "summary" or "missing_context"
    model : str
        Model to use: "bart" (default), "phi-2", or "flan-t5"
        
    Returns:
    --------
    Tuple[str, bool]
        A tuple containing (generated_text, success_flag)
        If successful, returns (generated_text, True)
        If failed, returns (error_message, False)
    """
    logger.info(f"Generating {summary_type} using Hugging Face API with {model} model")
    
    # Get API key from our standard function that checks all sources
    api_token = get_api_key()
    if not api_token:
        error_msg = "No Hugging Face API token found. Please set HUGGINGFACE_API_KEY in your .env file."
        logger.warning(error_msg)
        return error_msg, False
    
    # Model configurations
    model_configs = {
        "bart": {
            "url": "https://api-inference.huggingface.co/models/facebook/bart-large-cnn",
            "max_chars": 1500,
            "max_output": 500,
            "temperature": 0.7
        },
        "phi-2": {
            "url": "https://api-inference.huggingface.co/models/microsoft/phi-2",
            "max_chars": 4000,
            "max_output": 800,
            "temperature": 0.3
        },
        "flan-t5": {
            "url": "https://api-inference.huggingface.co/models/google/flan-t5-large",
            "max_chars": 2000,
            "max_output": 500,
            "temperature": 0.4
        }
    }
    
    # Check if model is supported
    if model not in model_configs:
        logger.warning(f"Model {model} not supported, falling back to bart")
        model = "bart"
        
    config = model_configs[model]
    
    # Truncate text based on model's context limit
    max_chars = config["max_chars"]
    truncated_text = article_text[:max_chars] if len(article_text) > max_chars else article_text
    
    # Create prompts based on model and summary type
    if model == "phi-2":
        if summary_type == "summary":
            prompt = f"""Please provide a concise summary of this article:

{truncated_text}

Summary:"""
        elif summary_type == "missing_context":
            prompt = f"""Read this article and identify what important context or information might be missing:

{truncated_text}

Missing context:"""
        else:
            prompt = f"""Please analyze this article objectively:

{truncated_text}

Analysis:"""
    else:
        # Simpler prompts for BART and T5 models
        if summary_type == "summary":
            prompt = f"Summarize: {truncated_text}"
        elif summary_type == "missing_context":
            prompt = f"What important information is missing from this text: {truncated_text}"
        else:
            prompt = f"Analyze: {truncated_text}"
    
    # API endpoint from the selected model
    API_URL = config["url"]
    
    # Set up headers
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    # Request payload with model-specific parameters
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": config["max_output"],
            "temperature": config["temperature"],
            "do_sample": True
        }
    }
    
    try:
        # Make the API request
        logger.info(f"Making {summary_type} request to {API_URL}")
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        # Log response details for debugging
        logger.info(f"Response status code: {response.status_code}")
        
        # Parse the response
        response_data = response.json()
        logger.info(f"Response data preview: {str(response_data)[:200]}...")
        
        # Extract the generated text based on response format
        raw_text = ""
        if isinstance(response_data, list) and len(response_data) > 0:
            if "summary_text" in response_data[0]:
                raw_text = response_data[0]["summary_text"]
                logger.info(f"Found summary_text: {raw_text[:100]}...")
            elif "generated_text" in response_data[0]:
                raw_text = response_data[0]["generated_text"]
                logger.info(f"Found generated_text: {raw_text[:100]}...")
            else:
                logger.error(f"No summary_text or generated_text in response")
                return f"Error: Unexpected response format", False
        elif isinstance(response_data, dict) and "generated_text" in response_data:
            # Some models return a dict with generated_text directly
            raw_text = response_data["generated_text"]
            logger.info(f"Found generated_text in dict: {raw_text[:100]}...")
        else:
            logger.error(f"Unexpected API response format")
            return f"Error: Unexpected response format from API", False
                
        # Clean up the generated text based on model
        if model == "phi-2":
            # For Phi-2, remove any prompt echoing and filter out prompts/instructions
            # Remove the prompt if it was echoed in the response
            if summary_type == "summary" and "Summary:" in raw_text:
                raw_text = raw_text.split("Summary:", 1)[1].strip()
            elif summary_type == "missing_context" and "Missing context:" in raw_text:
                raw_text = raw_text.split("Missing context:", 1)[1].strip()
            elif "Analysis:" in raw_text:
                raw_text = raw_text.split("Analysis:", 1)[1].strip()
        
        # Common post-processing for all models
        # Remove patterns like "Here's a summary of the article:" or "This article is about..."
        starter_phrases = [
            "here's a summary", 
            "this article is about",
            "in this article",
            "the article discusses",
            "this text discusses",
        ]
        
        for phrase in starter_phrases:
            if raw_text.lower().startswith(phrase):
                raw_text = raw_text[raw_text.find(" ", len(phrase)):].strip()
        
        # Split by sentences for web artifact filtering
        sentences = raw_text.split('.')
        cleaned_sentences = []
        
        # Filter out sentences that contain web artifacts
        web_artifacts = [
            'click here', 'visit the', 'follow us', 'sign up', 'read more',
            'comments', 'share your', 'subscribe', 'full article', 'read the',
            'mail online', 'www.', 'http', '.com', '.org', '.gov',
            'back to', 'return to', 'home page', 'summarize', 'tell us',
            'in the comments below', 'what do you think', 'let us know',
            'tell me what', 'leave a comment', 'write in the', 'find more',
            'learn about', 'check out', 'visit our', 'for more information'
        ]
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            # Check if this sentence contains web artifacts
            if any(artifact.lower() in sentence.lower() for artifact in web_artifacts):
                continue
                
            # Check if it's a question (for "missing context" sometimes the model asks questions)
            if summary_type == "missing_context" and sentence.endswith('?'):
                continue
                
            cleaned_sentences.append(sentence)
        
        # Reconstruct cleaned text
        if cleaned_sentences:
            generated_text = '. '.join(cleaned_sentences)
            # Add final period if missing
            if not generated_text.endswith('.'):
                generated_text += '.'
            return generated_text, True
        else:
            # If we filtered out everything, return the original but warn
            logger.warning("All sentences were filtered out, returning raw text")
            return raw_text, True
            
    except requests.exceptions.RequestException as e:
        error_msg = f"API request failed: {str(e)}"
        logger.error(error_msg)
        return f"Error: {error_msg}", False
    except Exception as e:
        error_msg = f"Error generating {summary_type}: {str(e)}"
        logger.error(error_msg)
        return f"Error: {error_msg}", False