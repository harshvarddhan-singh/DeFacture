# DeFacture - News Analysis Prototype

A streamlined tool for analyzing news articles and checking factual accuracy.

## Overview

DeFacture is a prototype application built with Streamlit that provides a user-friendly interface for analyzing news articles. The prototype allows users to:

- Select from sample news articles or enter custom URLs
- View article summaries with key points
- See contextual background information
- Discover semantically related articles with similarity scores
- Review fact-checking results

## Data Sources and Analysis Modes

The application intelligently handles both sample data and external APIs:

1. **Sample Articles** - Pre-loaded articles from `data/sample_articles.json` for quick demos
2. **API Integration** - When entering a custom URL, the system attempts to fetch and analyze the content
3. **Context Analysis** - Choose between multiple models:
   - **Phi-2 (Local)** - Uses locally cached Phi-2 model for fast, high-quality analysis
   - **Phi-2 (API)** - Uses Hugging Face API with Phi-2 model
   - **BART (API)** - Uses Hugging Face API with BART model
   - **Mock Data** - Simulated responses for testing
4. **Related Articles** - Find semantically similar content using:
   - Embedding-based semantic similarity (using sentence-transformers)
   - Keyword-based Jaccard similarity (as a fallback)
   - Optional explanations of article relationships

The application automatically chooses the appropriate data source based on user selection.

### Hugging Face API Integration

DeFacture uses the Hugging Face Inference API for context analysis:

1. Set up the API key:
   ```bash
   python setup_huggingface_api.py
   ```
   This will guide you through obtaining and configuring your API key.

2. Ensure `USE_LANGCHAIN_API = True` in `config.py` (default setting)

When enabled, the system will:
- Use Hugging Face API for context analysis of articles
- Fall back to mock data if API is unavailable or rate-limited
- Display informative errors if API keys are missing or invalid

For detailed information, see the [Hugging Face API setup documentation](docs/huggingface_api_setup.md).

### Related Articles Feature

The related articles feature uses semantic embeddings to find similar articles:

1. **Setup the environment**:
   ```bash
   python setup_related_articles.py --all
   ```

2. **Features**:
   - Semantic similarity using sentence transformers
   - Automatically compares with other articles in the dataset
   - Displays similarity scores and article perspectives
   - Optional explanations of why articles are related

3. **Configuration options** in the UI:
   - Choose similarity method (semantic or keyword)
   - Set maximum number of results
   - Toggle explanation feature on/off

## Setup Instructions

### Prerequisites

- Python 3.10+
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/s93hsing/defacture.git
cd defacture
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS/Linux
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
streamlit run main.py
```

## Usage Guide

### Selecting an Article

- Choose from the dropdown menu of sample articles
- Or select "Enter custom URL..." to input your own URL

### Analysis Features

The application provides analysis through several tabs:

1. **📝 Summary** - View the article summary and key points
2. **🔍 Context** - See contextual background information about the topic
3. **🔗 Related** - Discover related articles on the same subject
4. **⚠️ Fact Check** - Review fact-checking results for the article

### Sample Data

This prototype includes sample data in `data/sample_articles.json`. In a production environment, this would be replaced with real-time analysis and API calls.

## Project Structure

```
defacture/
├── assets/                  # CSS and static assets
├── config/                  # Configuration settings
├── data/                    # Data storage
│   └── sample_articles.json # Sample article data
├── docs/                    # Documentation
├── extras/                  # Non-essential utilities and scripts
│   ├── diagnostics/         # Diagnostic scripts
│   ├── setup/               # Setup scripts
│   └── tests/               # Informal test scripts
├── pages/                   # Streamlit pages
├── tests/                   # Formal test modules
├── tools/                   # Core functionality
│   ├── analysis.py          # Analysis tools and integrations
│   ├── huggingface_api.py   # Hugging Face API integration
│   ├── local_models.py      # Local model inference
│   ├── keyword_extraction.py # Keyword extraction
│   └── ...                  # Other tools
├── ui_components/           # UI components
├── utils/                   # Utility functions
├── main.py                  # Main Streamlit application
├── README.md                # Project documentation
└── requirements.txt         # Dependencies
```

## Local Model Inference

The application can use locally cached models for faster and more efficient analysis without requiring API calls. 

### Checking Local Model Availability

Run the following script to check if your system is properly configured for local model inference:

```bash
python extras/diagnostics/check_local_models.py
```

This will verify:
1. PyTorch installation
2. Transformers library installation
3. Whether the Phi-2 model is available in your local cache

### Model Options

- **Phi-2 (Local)**: Uses Microsoft's Phi-2 model directly from your local cache for best performance
- **Phi-2 (API)**: Uses Hugging Face API to access the Phi-2 model remotely
- **BART (API)**: Uses Hugging Face API to access the BART model remotely
- **Mock Data**: Returns simulated responses for testing purposes

### Benefits of Local Models

- **Speed**: Faster analysis without network latency
- **Cost**: No API usage fees or quotas
- **Offline Use**: Works without internet access once models are cached
- **Privacy**: All processing happens locally

## Future Enhancements

- Real-time web scraping for article content
- Integration with fact-checking APIs
- Additional local models for different analysis tasks
- User authentication and saved analysis history
- Export functionality for reports

---

Developed as a prototype for news analysis and fact checking.
