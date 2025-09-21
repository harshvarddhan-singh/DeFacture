# Setting Up Hugging Face API for DeFacture

DeFacture uses the Hugging Face Inference API to provide context analysis and summary generation capabilities. This document explains how to set up and configure the API for use with the application.

## Prerequisites

Before setting up the Hugging Face API, ensure you have:

1. A Hugging Face account (free)
2. A Hugging Face API token (sign up at [huggingface.co](https://huggingface.co) and create a token)
3. Python environment with required dependencies (requests, python-dotenv)

## Setup Instructions

### Automatic Setup (Recommended)

The easiest way to configure the Hugging Face API is to use the provided setup script:

```bash
python setup_huggingface_api.py
```

The script will:
1. Check if required dependencies are installed
2. Install any missing dependencies
3. Check if you already have a Hugging Face API key configured
4. Prompt you to enter an API key if one is not found
5. Validate the API key to ensure it works
6. Save the API key to your `.env` file

### Manual Setup

If you prefer to set up the API manually:

1. Create or edit the `.env` file in the root directory of the project
2. Add your Hugging Face API key:
   ```
   HUGGINGFACE_API_KEY=your_api_key_here
   ```
3. Save the file
4. Restart the application if it's already running

## Verifying Setup

To verify that your API key is properly configured:

1. Run the application with `python main.py`
2. Submit an article for analysis
3. Check that the context analysis is performed using the Hugging Face API rather than mock data

## Troubleshooting

If you encounter issues with the Hugging Face API:

- **Invalid API Key**: Make sure your API key is correct and has not expired
- **Rate Limiting**: Free tier accounts have rate limits; if you exceed them, wait a few minutes
- **Network Issues**: Check your internet connection
- **Dependencies**: Ensure all required packages are installed
- **Model Access**: Some models may require additional permissions or pro subscription; we use facebook/bart-large-cnn which is usually accessible with free API tokens
- **Response Format**: Different models return different response formats; our code handles the BART model format specifically

If problems persist, the application will automatically fall back to using mock data for context analysis.

## API Usage and Limitations

The Hugging Face Inference API free tier includes:
- 30,000 requests per month for most models
- Rate limits (typically 9 requests/minute)
- Limited to certain models; we use facebook/bart-large-cnn by default

For more information about Hugging Face API pricing and limitations, visit [huggingface.co/pricing](https://huggingface.co/pricing).