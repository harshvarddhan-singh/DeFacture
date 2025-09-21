# Hugging Face API Context Analysis

This document describes the implementation of Hugging Face API-based context analysis and summary generation in DeFacture.

## Overview

The context analysis feature uses the Hugging Face Inference API to provide detailed analysis of article context without requiring local model downloads. This analysis includes:

1. **Perspective**: The general point of view taken by the article
2. **Bias Indicators**: Phrases or patterns that suggest bias
3. **Historical Context**: Background information that places the article in context
4. **Missing Context**: What might be missing or presented without nuance

Additionally, the application now uses the BART model (facebook/bart-large-cnn) to generate:

1. **Article Summaries**: Concise summaries of article content
2. **Missing Context Analysis**: Identification of information that might be missing from articles

## Requirements

The implementation requires:
- `requests`: For making API calls to Hugging Face
- `json`: For parsing API responses
- `python-dotenv`: For loading environment variables (recommended)
- `logging`: For error logging and troubleshooting
- `re`: For extracting JSON from model responses when needed

All these dependencies except for `re` and `logging` (which are part of the Python standard library) are listed in the `requirements.txt` file.

## Setup

To use the Hugging Face API-based context analysis and summary generation:

1. Sign up for a Hugging Face account at [huggingface.co](https://huggingface.co/join)

2. Create an API token:
   - Go to your [Hugging Face profile settings](https://huggingface.co/settings/tokens)
   - Click "New token"
   - Give it a name (e.g., "DeFacture")
   - Select "Read" access
   - Click "Generate token"

3. Set up your API token using one of these methods:
   - **Recommended**: Run the setup script: `python setup_huggingface_api.py`
   - **Manual**: Create a `.env` file in the project root (or edit existing)
     - Add: `HUGGINGFACE_API_KEY=your_token_here`
     - Alternatively, you can use `HF_TOKEN=your_token_here` (the code checks both)

4. Ensure `USE_LANGCHAIN_API = True` in `config.py` (this is the default)

5. When analyzing an article, the system will automatically use the Hugging Face API for:
   - Context analysis
   - Article summarization
   - Missing context identification

## Implementation Details

### Context Analysis
- Uses the Flan-T5-Base model for generating structured context analysis
- Implements caching via `@lru_cache` to avoid repeated analysis of the same article
- Provides graceful fallback to mock data if the API fails
- Preserves the same output structure as the mock version so UI remains unchanged

### Summary Generation
- Uses the facebook/bart-large-cnn model, which is specifically fine-tuned for summarization tasks
- Returns both the generated text and a success flag to handle errors gracefully
- Can generate both general summaries and missing context analyses using the same model
- Maximum character limit on input text to avoid token limits (1500 chars by default)
- Handles different API response formats for compatibility

## Customization

You can modify the models used in both main functions:

### Context Analysis Model

For context analysis, edit the `API_URL` variable in the `huggingface_context_analysis` function in `tools/huggingface_api.py`. The function currently uses:

```python
# Current context analysis model
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"

# Alternative models you could use
# API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
# API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf"
# API_URL = "https://api-inference.huggingface.co/models/microsoft/phi-2"
```

### Summary Generation Model

For summaries and missing context analysis, edit the `API_URL` variable in the `generate_context_summary` function. The function currently uses:

```python
# Current summary generation model (recommended)
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
```

Note that the BART model is specifically designed for summarization tasks, which makes it well-suited for generating concise article summaries.

## Testing

Run the test scripts to verify the implementation:

```bash
# Test the context analysis functionality
python tests/test_huggingface_api.py

# Test the BART model specifically for summarization
python tests/test_bart_model.py
```

The test_bart_model.py script specifically tests the facebook/bart-large-cnn model that's used for generating summaries and context analyses.

## Troubleshooting

If you encounter issues:

1. **API Key Issues**: Check that your Hugging Face API token is correctly set in the `.env` file or environment variables.

2. **Rate Limits**: Free Hugging Face API usage has rate limits. If you're seeing errors, you may need to wait or upgrade to a paid plan.

3. **Response Format**: If the model returns unexpected formats, the system will automatically fall back to the mock implementation.

4. **Network Issues**: Check your internet connection if API requests are failing.

5. **Model Availability**: Sometimes specific models may be temporarily unavailable on Hugging Face. Try a different model if this happens.