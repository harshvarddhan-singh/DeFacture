""" UI Styling Components for DeFacture Application ============================================== This module contains styling constants, CSS templates, and UI helper functions to reduce code duplication and improve maintainability of the main article_input module. """
import streamlit as st

# CSS and Styling Constants
FONT_AWESOME_CSS = """
<!-- Font Awesome Icons -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
"""

MAIN_HEADER_CSS = """
<div style="background: linear-gradient(135deg, #0d7377 0%, #14a085 25%, #2dd4bf 50%, #6ee7b7 75%, #86efac 100%); border-radius: 20px; padding: 2rem; margin-bottom: 2rem; box-shadow: 0 8px 32px rgba(13, 115, 119, 0.4);">
    <h1 style="color: white; text-align: center; font-size: 2.5rem; font-weight: 800; margin-bottom: 1rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.4);">
        <i class="fas fa-search-plus" style="margin-right: 0.5rem; color: #ffd700;"></i> DeFacture: AI-Powered Fact Checker
    </h1>
    <p style="color: #f0fdfa; text-align: center; font-size: 1.2rem; margin: 0; font-weight: 500;">
        Advanced fact-checking with multiple input methods and comprehensive analysis
    </p>
</div>
"""

METHOD_TAB_STYLES = {
    'sample': {
        'icon': '🧪',
        'title': 'Sample Articles',
        'description': 'Try pre-loaded sample articles for testing'
    },
    'url': {
        'icon': '🌐',
        'title': 'URL Input',
        'description': 'Analyze articles from any web URL'
    },
    'search': {
        'icon': '🔍',
        'title': 'Search Articles',
        'description': 'Search for articles using SERP API'
    },
    'dataset': {
        'icon': '📊',
        'title': 'Dataset Upload',
        'description': 'Upload JSON/JSONL datasets for batch processing'
    }
}

import json
import os
from pathlib import Path

# Load sample articles from JSON file
try:
    # Get the path to the JSON file
    sample_articles_path = Path(__file__).parent.parent / "data" / "sample_articles.json"
    
    # Load articles from file
    with open(sample_articles_path, 'r', encoding='utf-8') as file:
        articles_data = json.load(file)
        SAMPLE_ARTICLES = []
        # Process articles and ensure source field is set to "sample"
        for article in articles_data.get("articles", []):
            article["source"] = "sample"
            SAMPLE_ARTICLES.append(article)
except Exception as e:
    # Fallback to default sample article if loading fails
    print(f"Failed to load sample articles: {e}")
    SAMPLE_ARTICLES = [
        {
            "title": "Climate Change: Latest Scientific Consensus (Sample)",
            "content": "Recent studies from leading climate research institutions indicate that global temperatures have risen by 1.2°C since pre-industrial times. The Intergovernmental Panel on Climate Change (IPCC) reports unprecedented changes in Earth's climate system. Scientists have observed accelerating ice sheet loss in Greenland and Antarctica, with sea level rise of 3.4mm per year. Ocean acidification has increased by 30% since the Industrial Revolution. Extreme weather events, including hurricanes, droughts, and heatwaves, are becoming more frequent and intense. Carbon dioxide levels have reached 421 parts per million, the highest in over 3 million years. Renewable energy adoption has accelerated, with solar and wind now the cheapest forms of electricity in many regions.",
            "source": "sample",
            "domain": "Sample Climate Research Institute", 
            "author": "Dr. Sarah Johnson, Climate Scientist",
            "published_date": "March 15, 2024",
        # Mock downstream tasks results
        "mock_analysis": {
            "summary": {
                "summary": "This comprehensive climate change report highlights critical environmental indicators showing accelerating global warming. The article presents IPCC findings on temperature increases, ice sheet loss, and rising sea levels, while also noting positive developments in renewable energy adoption.",
                "key_points": [
                    "Global temperatures have increased by 1.2°C since pre-industrial times",
                    "Sea level rise is occurring at 3.4mm per year with accelerating ice sheet loss",
                    "Ocean acidification has increased 30% since Industrial Revolution",
                    "Carbon dioxide levels are at highest point in 3 million years at 421 ppm",
                    "Renewable energy has become cost-competitive with traditional sources"
                ]
            },
            "context": {
                "perspective": "The article presents a scientifically grounded, data-driven perspective on climate change impacts.",
                "bias_indicators": ["Uses peer-reviewed scientific sources", "Presents factual data without political framing", "Includes both challenges and solutions"],
                "historical_context": "This aligns with the IPCC AR6 report series and ongoing international climate negotiations under the Paris Agreement.",
                "missing_context": "Could benefit from discussion of regional variations in climate impacts and socioeconomic implications."
            },
            "related_articles": [
                {
                    "title": "IPCC AR6 Working Group I Report: The Physical Science Basis",
                    "source": "IPCC Publications",
                    "date": "2021-08-09",
                    "url": "https://ipcc.ch/report/ar6/wg1/",
                    "relevance": "High",
                    "perspective": "Supporting"
                },
                {
                    "title": "Global Carbon Budget 2023: Emissions Remain at Record High",
                    "source": "Global Carbon Project",
                    "date": "2023-12-05",
                    "url": "https://globalcarbonproject.org/carbonbudget/",
                    "relevance": "High",
                    "perspective": "Corroborating"
                }
            ],
            "fact_check": {
                "overall_assessment": "Highly Accurate",
                "claims": [
                    {
                        "claim": "Global temperatures have risen by 1.2°C since pre-industrial times",
                        "assessment": "Accurate",
                        "evidence": "Confirmed by NASA GISS, NOAA, and WMO temperature records. Latest data shows 1.15-1.2°C warming."
                    },
                    {
                        "claim": "Sea level rise of 3.4mm per year",
                        "assessment": "Accurate",
                        "evidence": "NOAA satellite altimetry data confirms current rate of 3.4mm/year, with acceleration noted."
                    },
                    {
                        "claim": "Carbon dioxide levels at 421 parts per million",
                        "assessment": "Accurate",
                        "evidence": "Mauna Loa Observatory recorded CO2 levels exceeding 421 ppm in 2023-2024."
                    }
                ]
            }
        }
    },
    {
        "title": "AI Revolution in Healthcare: Transforming Medical Diagnosis (Sample)",
        "content": "Artificial Intelligence is revolutionizing healthcare through advanced diagnostic capabilities. Machine learning algorithms can now detect cancer with 94% accuracy, surpassing human radiologists in some cases. AI-powered drug discovery has reduced development time from 10-15 years to 3-5 years. IBM Watson for Oncology analyzes patient data to recommend personalized treatment plans. Deep learning models process medical images to identify diseases like diabetic retinopathy and pneumonia. Natural Language Processing helps analyze clinical notes and research papers. Robotic surgery systems perform procedures with sub-millimeter precision. AI chatbots provide 24/7 patient support and preliminary health assessments.",
        "source": "sample",
        "domain": "Sample Medical Technology Review",
        "author": "Dr. Michael Chen, Medical AI Researcher",
        "published_date": "February 28, 2024",
        # Mock downstream tasks results
        "mock_analysis": {
            "summary": {
                "summary": "This article explores the transformative impact of AI in healthcare, covering diagnostic improvements, drug discovery acceleration, and various clinical applications. It highlights both current achievements and emerging technologies in medical AI.",
                "key_points": [
                    "AI achieves 94% accuracy in cancer detection, sometimes exceeding human performance",
                    "Drug discovery timeline reduced from 10-15 years to 3-5 years using AI",
                    "Multiple AI applications span imaging, NLP, robotics, and patient support",
                    "Deep learning models successfully identify specific diseases from medical images",
                    "AI systems provide personalized treatment recommendations and 24/7 support"
                ]
            },
            "context": {
                "perspective": "The article presents an optimistic view of AI in healthcare, emphasizing achievements and potential.",
                "bias_indicators": ["Focuses primarily on positive outcomes", "Limited discussion of challenges or limitations", "Industry-focused perspective"],
                "historical_context": "Reflects the rapid advancement of AI in healthcare following deep learning breakthroughs since 2012.",
                "missing_context": "Could include discussion of regulatory challenges, data privacy concerns, and implementation barriers."
            },
            "related_articles": [
                {
                    "title": "FDA Approvals of AI/ML-Based Medical Devices",
                    "source": "FDA Medical Device Database",
                    "date": "2024-01-15",
                    "url": "https://fda.gov/medical-devices/ai-ml",
                    "relevance": "High",
                    "perspective": "Regulatory"
                },
                {
                    "title": "Challenges in Clinical AI Implementation: A Systematic Review",
                    "source": "Nature Medicine",
                    "date": "2024-02-10",
                    "url": "https://nature.com/articles/nm-ai-challenges",
                    "relevance": "Medium",
                    "perspective": "Critical"
                }
            ],
            "fact_check": {
                "overall_assessment": "Mostly Accurate with Some Generalizations",
                "claims": [
                    {
                        "claim": "Machine learning algorithms detect cancer with 94% accuracy",
                        "assessment": "Partially Accurate",
                        "evidence": "Accuracy varies by cancer type and study. Some studies show 94%+ for specific cancers like skin cancer, but general claim needs context."
                    },
                    {
                        "claim": "AI-powered drug discovery reduced development time from 10-15 years to 3-5 years",
                        "assessment": "Optimistic Projection",
                        "evidence": "AI shows promise in drug discovery but 3-5 year timeline is aspirational. Most AI-discovered drugs still in early trials."
                    },
                    {
                        "claim": "IBM Watson for Oncology analyzes patient data for treatment plans",
                        "assessment": "Accurate but Outdated",
                        "evidence": "IBM Watson for Oncology existed but faced criticism and was largely discontinued by major hospitals."
                    }
                ]
            }
        }
    },
    {
        "title": "Quantum Computing Breakthrough: New Milestone Achieved (Sample)",
        "content": "Researchers have achieved quantum supremacy with a 70-qubit quantum processor, solving complex problems impossible for classical computers. Google's quantum computer performed a specific calculation in 200 seconds that would take the world's fastest supercomputer 10,000 years. Quantum computers use quantum bits (qubits) that can exist in multiple states simultaneously through superposition. Quantum entanglement allows instant correlation between particles regardless of distance. Major tech companies including IBM, Microsoft, and Amazon are investing billions in quantum research. Applications include cryptography, drug discovery, financial modeling, and optimization problems. Quantum error correction remains a significant challenge for scaling up quantum systems.",
        "source": "sample",
        "domain": "Sample Quantum Research Lab",
        "author": "Prof. Emily Rodriguez, Quantum Physicist",
        "published_date": "January 10, 2024",
        # Mock downstream tasks results
        "mock_analysis": {
            "summary": {
                "summary": "This article reports on quantum computing advances, highlighting Google's quantum supremacy achievement and explaining fundamental quantum principles. It covers current research investments and both applications and challenges in the field.",
                "key_points": [
                    "Quantum supremacy achieved with 70-qubit processor solving problems impossible for classical computers",
                    "Google's quantum computer completed calculation in 200 seconds vs 10,000 years for supercomputers",
                    "Quantum mechanics principles of superposition and entanglement enable unique computational capabilities",
                    "Major tech companies investing billions in quantum research and development",
                    "Applications span cryptography, drug discovery, and complex optimization problems"
                ]
            },
            "context": {
                "perspective": "The article presents quantum computing achievements with technical optimism while acknowledging scaling challenges.",
                "bias_indicators": ["Emphasizes breakthrough achievements", "Corporate investment focus", "Limited discussion of technical limitations"],
                "historical_context": "Builds on decades of quantum physics research, with practical computing applications emerging since 2019.",
                "missing_context": "Could expand on competing quantum computing approaches and realistic timelines for practical applications."
            },
            "related_articles": [
                {
                    "title": "Google Claims Quantum Supremacy with 54-Qubit Sycamore Processor",
                    "source": "Nature",
                    "date": "2019-10-23",
                    "url": "https://nature.com/articles/s41586-019-1666-5",
                    "relevance": "High",
                    "perspective": "Historical Context"
                },
                {
                    "title": "IBM's Quantum Network Reaches 200+ Members Milestone",
                    "source": "IBM Research Blog",
                    "date": "2024-01-05",
                    "url": "https://research.ibm.com/quantum-network",
                    "relevance": "Medium",
                    "perspective": "Industry"
                }
            ],
            "fact_check": {
                "overall_assessment": "Accurate with Minor Technical Imprecision",
                "claims": [
                    {
                        "claim": "Quantum supremacy achieved with 70-qubit quantum processor",
                        "assessment": "Partially Accurate",
                        "evidence": "Google's 2019 achievement used 53 qubits, not 70. IBM and others have since built larger systems but 'supremacy' claims are debated."
                    },
                    {
                        "claim": "Calculation completed in 200 seconds vs 10,000 years for supercomputers",
                        "assessment": "Accurate for Specific Problem",
                        "evidence": "Google's 2019 Nature paper reports 200 seconds vs 10,000 years, though IBM disputed the classical computation estimate."
                    },
                    {
                        "claim": "Quantum entanglement allows instant correlation regardless of distance",
                        "assessment": "Scientifically Accurate",
                        "evidence": "Quantum entanglement is well-established phenomenon confirmed by numerous experiments, though doesn't enable faster-than-light communication."
                    }
                ]
            }
        }
    }
]

def inject_font_awesome():
    """Inject Font Awesome CSS if not already done"""
    if 'font_awesome_injected' not in st.session_state:
        st.markdown(FONT_AWESOME_CSS, unsafe_allow_html=True)
        st.session_state.font_awesome_injected = True

def show_main_header():
    """Display the main application header"""
    inject_font_awesome()
    st.markdown(MAIN_HEADER_CSS, unsafe_allow_html=True)

def create_method_tabs():
    """Create and return the method selection tabs"""
    tabs = st.tabs([
        f"{METHOD_TAB_STYLES[method]['icon']} {METHOD_TAB_STYLES[method]['title']}"
        for method in ['sample', 'url', 'search', 'dataset']
    ])
    return tabs

def show_method_description(method: str):
    """Show description for a specific method"""
    if method in METHOD_TAB_STYLES:
        info = METHOD_TAB_STYLES[method]
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); border-radius: 10px; padding: 1rem; margin-bottom: 1.5rem; border-left: 4px solid #667eea;">
                <p style="margin: 0; color: #4a5568; font-weight: 500;">
                    {info['icon']} {info['description']}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

def create_url_input_form():
    """Create URL input form with validation and persistent state"""
    st.markdown("### 🌐 Enter Article URL")
    url_input = st.text_input(
        "Article URL:",
        placeholder="https://example.com/article",
        help="Enter the URL of the article you want to fact-check",
        key="url_input_field"  # Add key to maintain state across reruns
    )

    # Make fetch button more prominent
    st.markdown("**Step 1: Fetch Article Content**")
    fetch_button = st.button(
        "🌐 Fetch from URL",
        type="primary",
        use_container_width=True,
        help="Click to fetch and preview the article content",
        key="fetch_url_button"  # Unique key for URL handler
    )

    return url_input, fetch_button

def create_sample_selector():
    """Create sample article selector with dropdown and fetch button"""
    st.markdown("### 🧪 Choose a Sample Article")

    # Create dropdown options
    dropdown_options = ["Select a sample article..."]
    for i, sample in enumerate(SAMPLE_ARTICLES):
        title_preview = sample['title'][:50] + "..." if len(sample['title']) > 50 else sample['title']
        dropdown_options.append(f"{i+1}. {title_preview}")

    selected_index = st.selectbox(
        "Select a sample article:",
        range(len(dropdown_options)),
        format_func=lambda x: dropdown_options[x],
        key="sample_article_dropdown"
    )

    # Make fetch button more prominent
    st.markdown("**Step 1: Fetch Sample Article**")
    fetch_sample_button = st.button(
        "📄 Fetch Sample Article",
        type="primary",
        use_container_width=True,
        help="Click to fetch sample article details",
        key="fetch_sample_button"  # Unique key for sample handler
    )

    # Return the actual sample index (subtract 1 because first option is placeholder)
    if selected_index > 0:
        actual_sample_index = selected_index - 1
        return actual_sample_index, fetch_sample_button
    else:
        return None, fetch_sample_button

def create_dataset_uploader():
    """Create dataset upload interface"""
    st.markdown("### 📊 Upload Dataset")
    st.markdown("Upload a JSON or JSONL file containing articles to analyze in batch.")

    uploaded_file = st.file_uploader(
        "Choose a dataset file",
        type=['json', 'jsonl'],
        help="Upload JSON/JSONL files with article data"
    )

    if uploaded_file:
        st.success(f"📁 File uploaded: {uploaded_file.name}")
        col1, col2 = st.columns([3, 1])
        with col2:
            process_button = st.button(
                "Process Dataset",
                type="primary",
                use_container_width=True
            )
    else:
        process_button = False

    # Download sample dataset link
    st.markdown("---")
    st.markdown("**📥 Download Sample Dataset:**")
    col1, col2 = st.columns([3, 1])
    with col2:
        download_sample = st.button(
            "Download Sample",
            use_container_width=True
        )

    return uploaded_file, process_button, download_sample

def styled_notification(content: str, emoji: str = "", title: str = "Article Ready for Analysis!"):
    """Create a reusable styled notification with frosted glass effect"""
    return f"""
    <div style="
        background: rgba(255, 255, 255, 0.7);
        padding: 1rem 1.5rem;
        border-radius: 1rem;
        border: 1px solid #d0d0d0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        backdrop-filter: blur(6px);
        margin-bottom: 1rem;
    ">
        <span style="font-size: 1.1rem; font-weight: bold;">{emoji} {title}</span><br>
        <span style="font-size: 0.95rem;">{content}</span>
    </div>
    """

def show_article_preview_card(article_data: dict):
    """Show a detailed preview card for article data with content preview and metadata"""
    source_emoji = {
        "sample": "🧪",
        "url": "🌐",
        "search_result": "🔍",
        "uploaded_dataset": "📂"
    }.get(article_data.get("source", ""), "📄")

    # Get article content and create preview
    content = article_data.get('content', '')

    # Content quality validation
    content_issues = []
    if len(content) < 100:
        content_issues.append("⚠️ Content appears very short")
    
    content_lower = content.lower()
    nav_indicators = ["see all topics follow", "subscribe now", "menu items", "follow us on", "social media"]
    if any(indicator in content_lower for indicator in nav_indicators):
        content_issues.append("⚠️ Content may contain navigation elements")
    
    if content_issues:
        content_preview = f"[Content Quality Issues: {'; '.join(content_issues)}]\n\n{content[:200]}..." if content else "No content available"
    else:
        content_preview = content[:300] + "..." if len(content) > 300 else content
        
    title = article_data.get('title', 'Untitled Article')
    domain = article_data.get('domain', 'Unknown Source')
    author = article_data.get('author', 'Unknown Author')
    published_date = article_data.get('published_date', 'Unknown Date')
    
    char_count = len(content)
    word_count = len(content.split()) if content else 0
    source_display = article_data.get('original_source', domain)

    # CARD 1: Article content with success notification and preview - Using hybrid approach with HTML and Streamlit components
    # Start with the container and notification
    st.markdown(
        f"""
        <div style="background: rgba(255, 255, 255, 0.7);
                    border-radius: 1rem 1rem 0 0;
                    padding: 1.5rem 1.5rem 0 1.5rem;
                    margin: 2rem 0 0 0; 
                    border: 1px solid #d0d0d0;
                    border-bottom: none;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                    backdrop-filter: blur(6px);">
            <div style="background: rgba(255, 255, 255, 0.5);
                        padding: 1rem 1.5rem;
                        border-radius: 0.75rem;
                        margin-bottom: 1.2rem;">
                <span style="font-size: 1.1rem; font-weight: bold;">{source_emoji} Article Ready for Analysis!</span><br>
                <span style="font-size: 0.95rem;">✅ Successfully fetched from <b>{source_display}</b></span>
            </div>
            <h2 style="text-align:center; margin-bottom:1.2rem; color:#333;">{title}</h2>
            <h3 style="margin-top:0; margin-bottom:1rem;">📄 Article Preview</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Use Streamlit components within the same visual card (continue the styling)
    with st.container():
        st.markdown(
            """
            <div style="background: rgba(255, 255, 255, 0.7);
                        border-radius: 0;
                        padding: 0 1.5rem;
                        margin: 0; 
                        border-left: 1px solid #d0d0d0;
                        border-right: 1px solid #d0d0d0;">
            """, 
            unsafe_allow_html=True
        )
        
        if content_issues:
            st.markdown(
                f"""
                <div style="background: rgba(255, 255, 255, 0.7);
                            padding: 1rem 1.5rem;
                            border-radius: 1rem;
                            border: 1px solid #d0d0d0;
                            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                            backdrop-filter: blur(6px);
                            margin-bottom: 1rem;">
                    <span style="font-size: 1.1rem; font-weight: bold;">⚠️ Content Quality Issues</span><br>
                    <span style="font-size: 0.95rem;">{'; '.join(content_issues)}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with st.expander("View Content Preview", expanded=True):
            st.markdown(f"{content_preview}")
        
        st.markdown(
            """
            <div style="background: rgba(255, 255, 255, 0.7);
                        border-radius: 0 0 1rem 1rem;
                        padding: 0.75rem 1.5rem 1.5rem 1.5rem;
                        margin: 0 0 1.5rem 0; 
                        border: 1px solid #d0d0d0;
                        border-top: none;">
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    # CARD 2: Metadata card with all details - Using Streamlit components for proper rendering
    # Start with the card header
    st.markdown(
        """
        <div style="background: rgba(255, 255, 255, 0.7);
                    border-radius: 1rem 1rem 0 0;
                    padding: 1.5rem 1.5rem 0.5rem 1.5rem;
                    margin: 1.5rem 0 0 0; 
                    border: 1px solid #d0d0d0;
                    border-bottom: none;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                    backdrop-filter: blur(6px);">
            <h3 style="margin-top:0; margin-bottom:1rem;">📊 Article Metadata</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Use a container for the metadata content with continued styling
    with st.container():
        st.markdown(
            """
            <div style="background: rgba(255, 255, 255, 0.7);
                        padding: 0 1.5rem;
                        margin: 0;
                        border-left: 1px solid #d0d0d0;
                        border-right: 1px solid #d0d0d0;
                        backdrop-filter: blur(6px);">
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Character and Word count
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(
                f"""
                <div style="background:rgba(255,255,255,0.5); 
                            padding:1rem; border-radius:10px; 
                            text-align:center; margin-bottom: 1rem;">
                    <div style="color:#555; font-size:0.9rem;">🔢 Characters</div>
                    <div style="font-size:1.5rem; font-weight:bold;">{char_count:,}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                f"""
                <div style="background:rgba(255,255,255,0.5); 
                            padding:1rem; border-radius:10px; 
                            text-align:center; margin-bottom: 1rem;">
                    <div style="color:#555; font-size:0.9rem;">🔤 Words</div>
                    <div style="font-size:1.5rem; font-weight:bold;">{word_count:,}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Author and Published date
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"👤 **Author:** {author}")
        with col2:
            st.markdown(f"📅 **Published:** {published_date}")
        
        # Publisher and Source Type
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"🏢 **Publisher:** {domain}")
        with col2:
            st.markdown(f"📊 **Source Type:** {article_data.get('source', 'Unknown').replace('_', ' ').title()}")
        
        # URL if available
        if article_data.get('url'):
            st.markdown(f"🔗 **URL:** {article_data.get('url')[:80]}...")
        
        # Close the card with a bottom border
        st.markdown(
            """
            <div style="background: rgba(255, 255, 255, 0.7);
                        border-radius: 0 0 1rem 1rem;
                        padding: 0.5rem 1.5rem 1.5rem 1.5rem;
                        margin: 0 0 1.5rem 0; 
                        border: 1px solid #d0d0d0;
                        border-top: none;
                        backdrop-filter: blur(6px);">
            </div>
            """, 
            unsafe_allow_html=True
        )

def show_analysis_start_button():
    """Show the analysis start button"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        return st.button(
            "🚀 Start Fact-Check Analysis",
            type="primary",
            use_container_width=True,
            help="Begin comprehensive fact-checking analysis of the article"
        )