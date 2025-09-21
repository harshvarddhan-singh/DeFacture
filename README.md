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
3. **LangChain Analysis** - Choose between:
   - Mock LLM analysis (simulated responses)
   - Real LLM API calls (for custom URLs only, requires API key)
4. **Related Articles** - Find semantically similar content using:
   - Embedding-based semantic similarity (using sentence-transformers)
   - Keyword-based Jaccard similarity (as a fallback)
   - Optional explanations of article relationships

The application automatically chooses the appropriate data source based on user selection.

### LLM API Integration

To enable real LLM API calls for custom URL analysis:

1. Copy `.env.sample` to `.env`
2. Add your OpenAI API key to the `.env` file
3. Set `USE_LANGCHAIN_API = True` in `config.py`

When enabled, the system will:
- Use real LLM API calls for custom URL analysis
- Fall back to mock data for sample articles
- Display errors if API keys are missing or invalid

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
├── .venv/                    # Python virtual environment
├── api.py                   # API integration functions (placeholders)
├── config.py                # Configuration settings
├── data/
│   └── sample_articles.json  # Sample article data
├── main.py                  # Main Streamlit application
├── README.md                # Project documentation
└── requirements.txt         # Dependencies
```

## Future Enhancements

- Real-time web scraping for article content
- Integration with fact-checking APIs
- Machine learning for automated summary generation
- User authentication and saved analysis history
- Export functionality for reports

---

Developed as a prototype for news analysis and fact checking.
