# DeFacture# DeFacture - News Analysis Prototype



## Project OverviewA comprehensive tool for analyzing news articles, extracting factual claims, providing contextual - Optimized prompt templates for token efficiency

DeFacture is a fact-checking application that extracts clai## Article Ingestion & Fetching

### Overview of Article Ingestion Methods

DeFacture offers multiple sophisticated methods for article ingestion to accommodate various user needs:

1. **URL-Based Fetching**: Extract content from live web articles
2. **Sample Article Selection**: Pre-loaded examples for demonstration
3. **Search-Based Discovery**: Find and analyze articles by topic
4. **Dataset Batch Processing**: Analyze multiple articles from JSON datasets

### Technical Implementation

#### Primary Article Fetcher (`tools/fetcher.py`)

The fetcher module implements a robust multi-layered approach to article extraction:

1. **Primary Method: newspaper3k**
   - Uses the `newspaper3k` library to extract content, metadata, and structure
   - Implements comprehensive validation for content quality
   - Handles edge cases like paywalls and dynamic content

   ```python
   def fetch_article_with_newspaper(url: str) -> dict:
       article = Article(url)
       article.download()
       article.parse()
       # Extensive validation and cleaning...
   ```

2. **Fallback Method: BeautifulSoup**
   - Engages when newspaper3k fails to extract meaningful content
   - Uses targeted CSS selectors to identify article content
   - Implements multiple extraction strategies for maximum compatibility

   ```python
   def fetch_article_fallback(url: str) -> dict:
       response = requests.get(url, headers=headers)
       soup = BeautifulSoup(response.content, 'html.parser')
       # Multiple selector strategies...
   ```

3. **Error Handling & Validation**
   - Content length validation (min 50 characters)
   - Detection of navigation/menu content vs. actual article text
   - Identification of common extraction issues (paywalls, JavaScript-rendered content)
   - Detailed error reporting for user feedback

#### Search-Based Article Discovery (`tools/search_api.py`)

The search API module enables discovery of news articles via multiple API backends:

1. **SERP API Integration**
   - Provides news search capability with detailed filtering
   - Handles authentication, rate limiting, and error states gracefully
   - Returns standardized article metadata (title, URL, snippet, source, date)

2. **Google Custom Search API**
   - Alternative search backend for article discovery
   - Configurable via API key and search engine ID
   - Optimized for news content

3. **Mock Search Capability**
   - Graceful fallback when APIs are unavailable
   - Context-aware results based on search query
   - Transparent error reporting to users

#### UI Integration (`ui_components/article_input.py`)

The article input UI provides a seamless user experience across all ingestion methods:

1. **Method Selection Tabs**
   - Sample Articles: Quick access to pre-loaded content
   - URL Input: Direct article fetching from web sources
   - Search: Topic-based article discovery
   - Dataset: Batch processing capabilities

2. **Workflow Management**
   - Clear three-step process: Fetch → Analyze → Start Over
   - Persistent state management via session state
   - Breadcrumb navigation for multi-stage workflows

3. **Error Handling**
   - User-friendly error messages
   - Specific troubleshooting guidance for common issues
   - Graceful fallbacks when primary methods fail

### Sample Article Integration

The system includes pre-loaded sample articles (`data/sample_articles.json`) for:
- Immediate testing without external dependencies
- Consistent benchmarking across features
- Offline operation capability

Each sample article includes:
- Rich metadata (title, source, author, date)
- Full article content
- Pre-generated mock analysis results

### Dataset Batch Processing

For bulk analysis scenarios, DeFacture supports:
- JSON/JSONL dataset uploads
- Sample dataset generation
- Article selection from larger datasets
- Batch analysis capabilities

### Error Handling & Resilience

The article ingestion system implements several resilience strategies:
- Multi-layered fallback mechanisms
- Detailed validation of extracted content
- User-friendly error messages with guidance
- Content quality assessment before analysis

### Performance Considerations

- **Caching**: Fetched articles are cached in session state
- **Validation**: Content is validated for minimum quality requirements
- **Timeout Handling**: Network operations use appropriate timeouts
- **Content Processing**: Large articles are handled with memory-efficient approaches

## � Requirements & Dependencies

### Core Requirements

- **Python**: 3.10 or higher
- **RAM**: 4GB+ (8GB+ recommended for local model inference)
- **GPU**: Optional, for faster local model inference
- **Storage**: ~5GB (including model cache)
- **Operating System**: Windows 10/11, macOS, or Linuxrticles, analyzes them, and provides fact-checking results. The application uses natural language processing techniques to process text data and leverages both local models and HuggingFace API for inference.

## Requirements & Dependenciesormation, and assessing factual accuracy.

## Features

- Claim extraction from articles## Overview

- Semantic analysis of claims

- Fact-checking using local models or HuggingFace APIDeFacture is a sophisticated news analysis prototype built with Streamlit that provides a user-friendly└── requirements.txt         # De| Memory Usage | 2-4 GB | 2-4 GB | 500 MB-1 GB |

- Related articles discovery

- Search functionality## Workflow Examplesdencies

- History tracking```



## Project Structure## System Requirements & Performanceerface for analyzing news articles. The application combines multiple NLP techniques, local and API-based model inference, and structured analysis to help users better understand news content.

```

DeFacture/### Key Features

├── assets/              # CSS and static files

├── config/              # Configuration files- **Article Analysis**: Extract key information from news articles with multiple model options

├── data/                # Sample data for testing- **Claim Extraction**: Identify factual claims for verification using NLP techniques

├── docs/                # Documentation files- **Semantic Similarity**: Discover related articles using embedding-based comparison

├── extras/              # Helper and setup scripts- **Contextual Information**: Generate background information and summaries

│   ├── diagnostics/     # Diagnostic tools- **Fact Checking**: Assess claim accuracy with rule-based heuristics and explanations

│   ├── setup/           # Setup scripts- **Robust Error Handling**: Graceful fallbacks for API failures and resource limitations

│   └── tests/           # Additional test files- **Modular Architecture**: Clean separation of UI, analysis logic, and data processing

├── pages/               # Streamlit page components

├── tests/               # Test files## System Architecture

├── tools/               # Core functionality modules

├── ui_components/       # UI components for StreamlitDeFacture follows a modular architecture with clear separation of concerns:

├── utils/               # Utility functions

├── download_nltk.py     # NLTK resource downloader### Component Structure

├── main.py              # Main application entry point```

└── requirements.txt     # Project dependenciesDeFacture/

```├── UI Components (/ui_components)

│   ├── Reusable UI elements

## Installation│   ├── Navigation system

│   ├── Analysis tabs

### Prerequisites│   └── Input forms

- Python 3.8 or higher├── Analysis Tools (/tools)

- Virtual environment (recommended)│   ├── Hugging Face API integration

│   ├── Local model inference (Phi-2)

### Setup│   ├── Claim extraction

1. Clone the repository:│   ├── Semantic similarity

```bash│   └── Fact checking

git clone https://github.com/yourusername/DeFacture.git├── Data Management

cd DeFacture│   ├── Sample article datasets

```│   ├── URL processing

│   └── Configuration

2. Create and activate a virtual environment (optional but recommended):└── Utilities

```bash    ├── NLTK patches

python -m venv venv    ├── Helper functions

# On Windows    └── Setup scripts

venv\Scripts\activate```

# On macOS/Linux

source venv/bin/activate### Technical Stack

```

- **Frontend**: Streamlit web interface

3. Install the dependencies:- **Backend**: Python-based analysis modules

```bash- **Models**: 

pip install -r requirements.txt  - Local: Microsoft's Phi-2 (optimized for 1500 token inputs)

```  - API: Hugging Face models (BART, FLAN-T5)

- **NLP Libraries**: NLTK (with custom patches), sentence-transformers

4. Download NLTK resources:- **Data Storage**: JSON for sample articles and configurations

```bash

python download_nltk.py## Detailed Features

```

### 1. Article Processing

## Configuration

Configure the application by modifying `config/config.py`:The system can process articles from multiple sources:



- Set up HuggingFace API keys- **Sample Articles Dataset**: Pre-loaded from `data/sample_articles.json` for quick testing

- Configure local model paths- **URL Processing**: Extract article content from user-provided URLs

- Adjust analysis parameters- **Custom Input**: Directly analyze user-provided text



## UsageProcessing pipeline:

Run the application:1. Text extraction and cleaning

```bash2. Metadata extraction (title, date, source)

streamlit run main.py3. Preparation for analysis modules

```

### 2. Context Analysis & Summarization

Access the web interface at http://localhost:8501

Multiple model options with automatic fallbacks:

### Using Local Models

The application supports local model inference. To use a local model:- **Phi-2 Local Inference**: Optimized for up to 1500 tokens with dynamic truncation

1. Download a supported model (e.g., Phi-2)  - Token-efficient prompt templates

2. Configure the model path in `config/config.py`  - Context-preserving truncation strategies

3. Select "Use Local Model" in the settings page  - Memory-optimized inference

  

### Using HuggingFace API- **Hugging Face API Integration**: 

To use HuggingFace API:  - Support for multiple summarization and analysis models

1. Obtain an API key from HuggingFace  - Configurable API settings via `.env` file

2. Add the API key to `config/config.py`  - Rate-limiting handling and error recovery

3. Select "Use HuggingFace API" in the settings page

- **Mock Analysis**: Fallback for when models or APIs are unavailable

## Core Components

### 3. Claim Extraction System

### Claim Extraction

Located in `tools/claim_extraction.py`, this module extracts factual claims from articles using NLP techniques.Advanced NLP pipeline for identifying factual claims:



### Local Models- **Sentence Tokenization**: Break articles into analyzable units

Located in `tools/local_models.py`, this module provides interfaces for local LLM inference.- **POS Tagging**: With custom fallback for NLTK resource errors 

- **Named Entity Recognition**: Identify key subjects in potential claims

### Fact Check Agent- **Claim Scoring**: Heuristic algorithms to identify claim-bearing sentences

Located in `tools/fact_check_agent.py`, this orchestrates the fact-checking workflow.- **Confidence Metrics**: Assessment of extraction confidence



### Analysis### 4. Semantic Similarity & Related Articles

Located in `tools/analysis.py`, this handles semantic analysis of claims and articles.

Sophisticated article comparison techniques:

## Troubleshooting

- **Embedding Generation**: Using sentence-transformers models

### NLTK Issues- **Similarity Calculation**: Cosine similarity on article embeddings

If you encounter NLTK-related errors:- **Keyword Fallback**: Jaccard similarity using extracted keywords when embeddings unavailable

1. Ensure NLTK resources are properly downloaded- **Explanation Generation**: Articulation of why articles are semantically related

2. Check `utils/nltk_patches.py` for patches- **Visualization**: Clear presentation of similarity scores and relationships

3. Run `extras/setup/fix_nltk_issues.py` to apply fixes

### 5. Fact Checking Pipeline

### Model Input Length

The Phi-2 model input length is set to 1500 tokens. If you need to adjust this:Rule-based assessment with structural extensibility:

- Modify `tools/local_models.py` and update the `max_length` parameter

- **Claim Analysis**: Assessment of extracted claims against rules

## Development- **Verdict Assignment**: Accurate, Partially Accurate, or False classifications

- **Justification**: Explanations for each verdict

### Adding New Models- **Source Citation**: References for verification (mock implementation)

To add support for new models:- **Extensibility**: Structure prepared for future API integration

1. Add model configuration to `config/config.py`

2. Implement model interface in `tools/local_models.py`## Technical Challenges & Solutions

3. Update the UI to include the new model option

### NLTK Resource Compatibility

### Testing

Run tests:**Problem**: The system encountered issues with NLTK's POS tagging resource naming (`averaged_perceptron_tagger_eng`), causing failures in claim extraction.

```bash

python -m pytest tests/**Solution**:

```- Implemented a monkey-patched version of NLTK's `pos_tag` function

- Created a simple heuristic-based POS tagger as fallback

## License- Added robust error handling throughout the claim extraction pipeline

[License information]- Developed a utility module (`utils/nltk_patches.py`) to centralize fixes

- Created automatic resource verification and download scripts

## Contributors

[List of contributors]### Phi-2 Model Input Constraints

**Problem**: The default Phi-2 model configuration limited inputs to 800 tokens, insufficient for longer news articles.

**Solution**:
- Increased maximum input length to 1500 tokens in model configuration
- Implemented intelligent truncation that preserves critical context
- Added token counting and input optimization
- Created graceful fallbacks for extremely long inputs
- Optimized prompt templates for token efficiency

## � Requirements & Dependencies

### Core Requirements

- **Python**: 3.10 or higher
- **RAM**: 4GB+ (8GB+ recommended for local model inference)
- **GPU**: Optional, for faster local model inference
- **Storage**: ~5GB (including model cache)
- **Operating System**: Windows 10/11, macOS, or Linux

### Python Package Dependencies

#### Essential Libraries
- `streamlit>=1.31.0`: Web application framework
- `nltk==3.9.1`: Natural Language Toolkit for text processing
- `newspaper3k==0.2.8`: Article extraction and parsing
- `requests>=2.32.0`: HTTP requests for API calls
- `python-dotenv>=1.0.0`: Environment variable management
- `beautifulsoup4>=4.12.0`: HTML parsing

#### Model & AI Dependencies
- `transformers>=4.34.0`: Hugging Face transformer models
- `torch>=2.1.0`: PyTorch for model inference
- `sentence-transformers>=2.3.1`: For semantic embeddings
- `sumy==0.11.0`: Text summarization

#### API Integration
- `serpapi-python>=0.1.3`: Search API integration
- `google-api-python-client>=2.115.0`: Google Custom Search API

#### UI Enhancements
- `plotly>=5.18.0`: Interactive visualizations
- `streamlit-extras>=0.3.0`: Additional Streamlit components
- `streamlit-aggrid>=0.3.4`: Interactive tables

#### Development Tools
- `pytest>=7.4.0`: Testing
- `black>=23.7.0`: Code formatting
- `flake8>=6.1.0`: Linting

### Full requirements are available in `requirements.txt`.

## API Keys & External Services

The application can integrate with several external APIs for enhanced functionality:

### 1. Hugging Face API

Required for using remote model inference when local models are not available.

- **Setup**:
  1. Create a [Hugging Face account](https://huggingface.co/join)
  2. Generate an API key at https://huggingface.co/settings/tokens
  3. Add to `.env` file: `HUGGINGFACE_API_KEY=your_key_here`

- **Models Used**:
  - `facebook/bart-large-cnn`: For article summarization
  - `microsoft/phi-2`: For context analysis (local inference preferred)

### 2. SerpAPI (Optional)

For enhanced article search capabilities:

- **Setup**:
  1. Create an account at [SerpAPI](https://serpapi.com/)
  2. Obtain API key from dashboard
  3. Add to `.env` file: `SERP_API_KEY=your_key_here`

### 3. Google Custom Search API (Optional)

For article discovery and verification:

- **Setup**:
  1. Create a [Google Cloud project](https://console.cloud.google.com/)
  2. Enable Custom Search API
  3. Create API credentials
  4. Add to `.env`: 
     ```
     GOOGLE_SEARCH_API_KEY=your_key_here
     GOOGLE_SEARCH_ENGINE_ID=your_engine_id_here
     ```

### Environment Variables

Create a `.env` file in the project root with the following variables:

```
# API Keys
HUGGINGFACE_API_KEY=your_huggingface_key
SERP_API_KEY=your_serpapi_key
GOOGLE_SEARCH_API_KEY=your_google_key
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id

# Configuration
USE_LANGCHAIN_API=True
```

## Getting Started

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/harshvarddhan-singh/DeFacture.git
cd DeFacture
```

2. **Set up a virtual environment**:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Download required NLTK resources**:
```bash
python download_nltk.py
```

5. **Configure API keys** (create `.env` file as described above)

### Running the Application

Start the Streamlit server:
```bash
streamlit run main.py
```

The application will be available at `http://localhost:8501` in your web browser.

## Usage Guide

### Main Interface

1. **Article Selection**:
   - Choose from sample articles in the dropdown
   - Enter a custom URL
   - Input text directly

2. **Analysis Tabs**:
   - **Summary**: Key points and overview
   - **Context**: Background information and contextual analysis
   - **Related Articles**: Semantically similar content
   - **Fact Check**: Claim extraction and verification results

3. **Settings**:
   - Toggle between analysis models
   - Configure similarity thresholds
   - Set API preferences

### Model Selection

Use the sidebar to select your preferred analysis model:

1. **Phi-2 (Local)**: Best performance when available locally
2. **API Models**: Multiple options through Hugging Face
3. **Mock Analysis**: For testing or when other options unavailable

### Advanced Features

- **Customization**: Configure model parameters in `config/config.py`
- **Debug Mode**: Enable detailed logging with `?debug=true` URL parameter
- **Performance Metrics**: View processing times in expanded UI sections

## Testing

The project includes multiple test suites:

1. **Basic Functionality Tests**:
```bash
python -m pytest extras/tests/test_basic.py
```

2. **API Integration Tests**:
```bash
python -m pytest tests/test_huggingface_api.py
```

3. **Model Performance Tests**:
```bash
python -m pytest extras/tests/test_local_models.py
```

4. **UI Flow Tests**:
```bash
python -m pytest tests/test_navigation_flow.py
```

## Project Structure

```
DeFacture/
├── assets/                  # CSS and static assets
├── config/                  # Configuration settings
│   └── config.py            # Main configuration parameters
├── data/                    # Data storage
│   └── sample_articles.json # Sample article data
├── docs/                    # Documentation
│   ├── huggingface_api_setup.md   # API setup guide
│   ├── keyword_extraction_docs.md # Keyword extraction docs
│   └── local_model_integration.md # Local model guide
├── extras/                  # Non-essential utilities and scripts
│   ├── diagnostics/         # Diagnostic scripts
│   ├── setup/               # Setup scripts
│   └── tests/               # Informal test scripts
├── pages/                   # Streamlit pages
│   ├── history.py           # History page
│   └── settings.py          # Settings page
├── tests/                   # Formal test modules
├── tools/                   # Core functionality
│   ├── analysis.py          # Analysis tools and integrations
│   ├── claim_extraction.py  # Claim extraction module
│   ├── fact_check_agent.py  # Fact checking logic
│   ├── fetcher.py           # Article fetching utilities
│   ├── huggingface_api.py   # Hugging Face API integration
│   ├── keyword_extraction.py # Keyword extraction
│   ├── local_models.py      # Local model inference
│   ├── related_articles.py  # Article similarity features
│   └── search_api.py        # Search integration
├── ui_components/           # UI components
│   ├── analysis_tabs.py     # Analysis tab components
│   ├── article_input.py     # Article input forms
│   ├── header.py            # Header components
│   ├── navigation.py        # Navigation system
│   ├── sidebar.py           # Sidebar components
│   └── ui_helpers.py        # UI utility functions
├── utils/                   # Utility functions
│   ├── helper.py            # General helper functions
│   └── nltk_patches.py      # NLTK compatibility patches
├── download_nltk.py         # NLTK resource downloader
├── main.py                  # Main Streamlit application
├── defacture_paper.tex      # Academic paper about the project
├── README.md                # Project documentation
└── requirements.txt         # Dependencies
```

## �️ System Requirements & Performance

### Minimum System Requirements
- **CPU**: Dual-core 2GHz+
- **RAM**: 4GB
- **Storage**: 2GB free space
- **Network**: Broadband internet connection (for API usage)
- **GPU**: Not required
- **Operating System**: Windows 10, macOS Catalina, Ubuntu 20.04 or newer

### Recommended System Requirements
- **CPU**: Quad-core 3GHz+
- **RAM**: 8GB+
- **Storage**: 10GB+ free space (for model caching)
- **GPU**: Any CUDA-compatible GPU with 4GB+ VRAM (for local model inference)
- **Network**: High-speed broadband connection
- **Operating System**: Windows 11, macOS Ventura, Ubuntu 22.04 or newer

### Performance Characteristics

| Feature | CPU Only | With GPU | API-Only Mode |
|---------|----------|----------|---------------|
| Startup Time | 15-30 sec | 10-20 sec | 5-10 sec |
| Article Processing | 1-3 sec | 1-2 sec | 1-2 sec |
| Summary Generation | 20-40 sec | 5-15 sec | 3-10 sec |
| Claim Extraction | 5-10 sec | 3-5 sec | 5-10 sec |
| Fact Checking | 15-30 sec | 5-15 sec | 3-10 sec |
| Memory Usage | 2-4 GB | 2-4 GB | 500 MB-1 GB |

## �🔄 Workflow Examples

### 1. Analyzing a News Article

1. Select an article from the dropdown or enter a URL
2. The system automatically:
   - Extracts article content and metadata
   - Generates a summary using the selected model
   - Provides contextual analysis
   - Identifies related articles
   - Extracts and verifies factual claims

### 2. Comparing Multiple Perspectives

1. Analyze an initial article
2. Click on related articles to analyze them
3. Compare summaries and fact-checking results side by side
4. Identify differences in reporting and perspective

### 3. Offline Analysis Workflow

1. Configure local Phi-2 model
2. Use sample articles or previously cached content
3. Perform full analysis without internet connectivity
4. Export or save results for later reference

## API & Integration Details

### Hugging Face API Integration

The Hugging Face API integration enables access to powerful NLP models without requiring local resources:

#### Models Used
- **Summarization**: `facebook/bart-large-cnn`
  - Parameters: `max_length=150, min_length=50, do_sample=False`
  - Cost: Free tier allows ~30K tokens/month
  
- **Context Analysis**: `google/flan-t5-base`
  - Parameters: `max_length=200, temperature=0.3`
  - Cost: Free tier allows ~30K tokens/month

- **Backup Options**: `t5-small`, `distilbart-cnn-6-6`
  - Used if primary models are unavailable

#### Rate Limiting & Fallbacks
- Free tier: 30K tokens/month (~100-200 articles)
- Rate limiting: Max 5 requests per minute
- When limits reached: Falls back to local models or mock data
- Error handling: Graceful degradation with user notifications

#### Security & Privacy
- API keys stored in `.env` file (not in repository)
- Minimal article data sent to API (only what's needed for processing)
- No PII or user data transmitted

### SerpAPI Integration

Used for discovering related news articles and search results:

- **Endpoint**: `https://serpapi.com/search`
- **Query Types**: News search, related articles
- **Rate Limits**: Depends on plan (free tier: 100 searches/month)
- **Results Processing**: Top 10 results parsed and analyzed

### Google Custom Search API

Alternative search integration for article discovery:

- **Endpoint**: `https://www.googleapis.com/customsearch/v1`
- **Configuration**: Custom Search Engine ID required
- **Rate Limits**: Free tier: 100 queries/day
- **Usage**: Targeted fact verification searches

## Troubleshooting

### Common Issues

1. **NLTK Resource Errors**:
   - Run `python download_nltk.py` to ensure all resources are available
   - Check `utils/nltk_patches.py` for custom patches
   - Specific error `averaged_perceptron_tagger_eng`: Fixed with our patch

2. **Model Loading Failures**:
   - Verify PyTorch installation with `python extras/diagnostics/check_local_models.py`
   - Ensure sufficient RAM/VRAM for model loading
   - Try reducing model precision with `--half-precision` flag

3. **API Connection Issues**:
   - Verify API key in `.env` file
   - Check network connectivity
   - Review rate limiting restrictions
   - Use `extras/diagnostics/check_api_key.py` to test API credentials

4. **Performance Considerations**:
   - For slower systems, prefer API models over local inference
   - Reduce article length for faster processing
   - Use mock analysis for UI testing
   - Consider enabling caching with `--enable-cache` option

### Diagnostic Tools

The `extras/diagnostics/` directory contains several helpful scripts:

- `check_api_key.py`: Verify Hugging Face API key functionality
- `check_env.py`: Check environment configuration
- `check_local_models.py`: Test local model availability
- `diagnose_phi2_model.py`: Diagnose Phi-2 model issues

## Future Roadmap

### Planned Enhancements

1. **Analysis Capabilities**:
   - Integration with real fact-checking APIs
   - Sentiment analysis module
   - Bias detection system
   - Source credibility assessment

2. **Technical Improvements**:
   - Multi-article comparative analysis
   - Advanced claim matching across sources
   - More efficient embedding generation
   - Additional local model options

3. **User Experience**:
   - User accounts and saved analyses
   - Customizable analysis parameters
   - Export functionality for reports
   - Visual representations of article relationships

4. **Infrastructure**:
   - Containerized deployment
   - API endpoints for headless operation
   - Improved caching mechanisms
   - Parallel processing for batch analysis

## Academic Paper

For a comprehensive academic discussion of this project, see the included LaTeX paper:
`defacture_paper.tex`

The paper covers:
- Technical implementation details
- Methodological approach
- Challenges and solutions
- Future research directions

## License

[MIT License](LICENSE)

## Acknowledgements

- Microsoft Research for the Phi-2 model
- Hugging Face for model hosting and APIs
- Streamlit team for the web application framework
- NLTK project for natural language processing tools
- Sentence-transformers library for embedding capabilities

---

**DeFacture** - Empowering critical news consumption through technology
