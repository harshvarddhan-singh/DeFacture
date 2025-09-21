"""
Local model inference using cached models

This module provides functions to use locally cached models from Hugging Face
without requiring API calls, for faster and more reliable inference.
"""

import logging
import os
from typing import Dict, List, Optional, Union, Tuple

# Conditionally import torch and transformers
try:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    HAVE_TORCH = True
    logger = logging.getLogger(__name__)
    logger.info("PyTorch and Transformers libraries loaded successfully")
except ImportError:
    HAVE_TORCH = False
    logger = logging.getLogger(__name__)
    logger.warning("PyTorch or Transformers not available, local models won't work")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cache for loaded models to avoid reloading
_MODEL_CACHE = {}

def phi2_context_analysis(text: str) -> Dict:
    """
    Analyze article context using locally cached Phi-2 model
    
    Parameters:
    -----------
    text : str
        The article text to analyze
        
    Returns:
    --------
    Dict
        Dictionary with perspective, bias_indicators, historical_context, and missing_context
    """
    if not HAVE_TORCH:
        logger.warning("PyTorch or Transformers not available, using mock data")
        return _get_mock_context_analysis()
    
    try:
        # Truncate text if it's too long
        max_chars = 4000
        truncated_text = text[:max_chars] if len(text) > max_chars else text
        
        # Create a structured prompt
        prompt = f"""Analyze this article and provide:
1. PERSPECTIVE: What is the main perspective or viewpoint of this article?
2. BIAS INDICATORS: List 3 potential indicators of bias in this article, if any.
3. HISTORICAL CONTEXT: What historical context is relevant to understanding this article?
4. MISSING CONTEXT: What important information might be missing from this article?

ARTICLE: {truncated_text}

ANALYSIS:"""

        # Get the model output
        output = phi2_generate(prompt, max_length=800, temperature=0.1)
        logger.info(f"Phi-2 output: {output[:100]}...")
        
        # Parse the structured output
        result = _parse_phi2_output(output)
        return result
        
    except Exception as e:
        logger.error(f"Error using local Phi-2 model: {str(e)}")
        return _get_mock_context_analysis()

def phi2_generate(prompt: str, max_length: int = 1500, temperature: float = 0.7) -> str:
    """
    Generate text using locally cached Phi-2 model
    
    Parameters:
    -----------
    prompt : str
        The prompt to generate from
    max_length : int
        Maximum length of the generated text
    temperature : float
        Temperature for generation (higher = more creative, lower = more deterministic)
        
    Returns:
    --------
    str
        Generated text
    """
    if not HAVE_TORCH:
        logger.warning("PyTorch or Transformers not available")
        return "Local model inference not available. Please install PyTorch and Transformers."
    
    try:
        # Load the model and tokenizer if not already cached
        if "phi-2" not in _MODEL_CACHE:
            logger.info("Loading Phi-2 model from cache...")
            
            # Load in 8-bit if enough GPU memory is available, else CPU
            device = "cuda" if torch.cuda.is_available() and torch.cuda.get_device_properties(0).total_memory > 8e9 else "cpu"
            if device == "cuda":
                model = AutoModelForCausalLM.from_pretrained(
                    "microsoft/phi-2", 
                    torch_dtype=torch.float16, 
                    device_map="auto", 
                    load_in_8bit=True
                )
            else:
                model = AutoModelForCausalLM.from_pretrained(
                    "microsoft/phi-2", 
                    device_map={"": device},
                    torch_dtype=torch.float32 if device == "cpu" else torch.float16
                )
            
            tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2")
            _MODEL_CACHE["phi-2"] = (model, tokenizer)
            logger.info(f"Phi-2 model loaded on {device}")
        else:
            model, tokenizer = _MODEL_CACHE["phi-2"]
        
        # Generate text
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        
        # Get input length to handle properly
        input_length = inputs.input_ids.shape[1]
        
        # If input is longer than max_length, switch to max_new_tokens approach
        if input_length > max_length:
            logger.warning(f"Input length ({input_length}) exceeds max_length ({max_length}). "
                          f"Using max_new_tokens parameter instead of max_length.")
            # Use max_new_tokens approach for better handling of long inputs
            max_new = max(300, max_length - input_length)
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new,  # Generate this many new tokens
                temperature=temperature,
                do_sample=temperature > 0.1,
                pad_token_id=tokenizer.eos_token_id
            )
        else:
            outputs = model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                do_sample=temperature > 0.1,
                pad_token_id=tokenizer.eos_token_id
            )
        
        # Get the generated text
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Remove the prompt from the output
        if generated_text.startswith(prompt):
            generated_text = generated_text[len(prompt):].strip()
        
        return generated_text
        
    except Exception as e:
        logger.error(f"Error generating with Phi-2: {str(e)}")
        return f"Error using local model: {str(e)}"

def _parse_phi2_output(output: str) -> Dict:
    """
    Parse structured output from Phi-2 model
    
    Parameters:
    -----------
    output : str
        The raw output from the model
        
    Returns:
    --------
    Dict
        Parsed structure with perspective, bias_indicators, etc.
    """
    # Create default result
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
    
    lines = output.split('\n')
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

def _get_mock_context_analysis() -> Dict:
    """
    Get mock context analysis when models aren't available
    
    Returns:
    --------
    Dict
        Mock context analysis
    """
    return {
        'perspective': 'The article presents information from multiple perspectives.',
        'bias_indicators': ['Use of emotive language', 'Selection of sources', 'Framing of the issue'],
        'historical_context': 'The article references historical events as context for current situations.',
        'missing_context': 'The article lacks details about alternative viewpoints and important related events.'
    }

def phi2_summarize(text: str) -> str:
    """
    Summarize text using locally cached Phi-2 model
    
    Parameters:
    -----------
    text : str
        The text to summarize
        
    Returns:
    --------
    str
        Generated summary
    """
    if not HAVE_TORCH:
        logger.warning("PyTorch or Transformers not available, can't use local Phi-2")
        return "Local model inference not available. Please install PyTorch and Transformers."
    
    try:
        # Truncate text if it's too long
        max_chars = 4000
        truncated_text = text[:max_chars] if len(text) > max_chars else text
        
        # Create a prompt for summarization
        prompt = f"""Please provide a concise summary of this article:

{truncated_text}

Summary:"""

        # Generate summary
        summary = phi2_generate(prompt, max_length=500, temperature=0.3)
        
        # Clean up the summary
        if summary.startswith("Summary:"):
            summary = summary.replace("Summary:", "", 1).strip()
            
        return summary
        
    except Exception as e:
        logger.error(f"Error summarizing with local Phi-2: {str(e)}")
        return f"Error using local model: {str(e)}"