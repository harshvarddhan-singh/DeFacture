# DeFacture - News Article Analysis Tool

## Project Overview

DeFacture is a practical tool for analyzing news articles, extracting factual claims, and providing contextual information. Built with Python and Streamlit, it helps users better understand news content through NLP techniques.

## Features

- Article extraction from URLs and sample datasets
- Claim identification from article text
- Factual analysis using local models or Hugging Face API
- Related article discovery through semantic similarity
- Simple and intuitive web interface

## Project Structure

```
DeFacture/
├── assets/              # CSS and static files
├── config/              # Configuration files
├── data/                # Sample data for testing
├── docs/                # Documentation files
├── extras/              # Helper scripts and diagnostics
├── pages/               # Streamlit page components
├── tests/               # Test files
├── tools/               # Core functionality modules
├── ui_components/       # UI components for Streamlit
├── utils/               # Utility functions
├── download_nltk.py     # NLTK resource downloader
├── main.py              # Main application entry point
└── requirements.txt     # Project dependencies
```

## Installation

### Prerequisites
- Python 3.10 or higher
- Virtual environment (recommended)

### Setup
1. Clone the repository:
```bash
git clone https://github.com/harshvarddhan-singh/DeFacture.git
cd DeFacture
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install the dependencies:
```bash
pip install -r requirements.txt
```

4. Download NLTK resources:
```bash
python download_nltk.py
```

## Configuration

Configure the application by modifying `config/config.py`:

- Set up HuggingFace API keys (optional)
- Configure local model paths
- Adjust analysis parameters

## Usage

Run the application:
```bash
streamlit run main.py
```

Access the web interface at http://localhost:8501

### Article Input Options

DeFacture offers multiple ways to input articles:

1. **Sample Articles**: Pre-loaded examples for quick testing
2. **URL Input**: Extract content from web articles
3. **Search**: Find articles by topic (requires API key)
4. **Dataset**: Upload JSON datasets for batch analysis

### Analysis Features

The system processes articles through several components:

1. **Content Extraction**: Pulls article content using newspaper3k with BeautifulSoup fallbacks
2. **Claim Extraction**: Identifies factual statements using NLP techniques
3. **Contextual Analysis**: Provides background and fact-checking when available
4. **Related Content**: Finds semantically similar articles

## Core Components

### Article Fetcher
Located in `tools/fetcher.py`, this module extracts article content from URLs using:
- Primary extraction via newspaper3k library
- Fallback extraction using BeautifulSoup when needed
- Content validation and cleaning

### Claim Extraction
Located in `tools/claim_extraction.py`, this extracts factual claims with:
- Sentence tokenization and filtering
- POS tagging (with NLTK fallback mechanisms)
- Claim confidence scoring

### Local Models
Located in `tools/local_models.py`, this provides inference using:
- Support for Microsoft's Phi-2 (optimized for 1500 token inputs)
- Template-based prompting
- Input/output processing

## Troubleshooting

### NLTK Issues
If you encounter NLTK-related errors:
1. Ensure NLTK resources are properly downloaded
2. Check `utils/nltk_patches.py` for patches
3. Run `extras/setup/fix_nltk_issues.py` to apply fixes

### Model Input Length
The Phi-2 model input length is set to 1500 tokens. If you need to adjust this:
- Modify `tools/local_models.py` and update the `max_length` parameter

## Requirements & Dependencies

### Core Requirements
- Python 3.10+
- 4GB+ RAM (8GB+ recommended for local models)
- Storage: ~2GB for base install, ~5GB with models

### Key Dependencies
- `streamlit`: Web interface
- `newspaper3k`: Article extraction
- `nltk`: Text processing
- `transformers`: Model handling
- `sentence-transformers`: Semantic similarity
- `torch`: Model inference
- Full list in `requirements.txt`

## API Integration

The application can use several APIs for enhanced functionality:

### Hugging Face API (Optional)
For model inference when local models are unavailable:
- Add your API key to `.env` file: `HUGGINGFACE_API_KEY=your_key_here`

### Search API (Optional)
For article discovery:
- SerpAPI or Google Custom Search API
- Configure in `.env` file

## Testing

Run tests with:
```bash
python -m pytest tests/
```

## License

[MIT License](LICENSE)

## Contributors

- Harsh Vardhan Singh
- [Other contributors]