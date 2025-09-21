"""
Dataset Processing Components for DeFacture Application
=====================================================

This module handles dataset upload, validation, and processing functionality.
"""

import streamlit as st
import json
from tools.dataset_processor import validate_json_dataset, process_jsonl_dataset, get_dataset_preview


def create_sample_dataset():
    """Create a sample dataset for download"""
    sample_data = [
        {
            "title": "Sample Article 1: Climate Change Research",
            "content": "This is sample content about climate change research findings...",
            "source": "Environmental Journal",
            "date": "2024-01-15"
        },
        {
            "title": "Sample Article 2: AI Technology Advances",
            "content": "This is sample content about recent advances in artificial intelligence...",
            "source": "Tech News",
            "date": "2024-01-20"
        }
    ]
    return json.dumps(sample_data, indent=2)


def validate_dataset_format(uploaded_file):
    """Validate the uploaded dataset format"""
    try:
        file_extension = uploaded_file.name.lower().split('.')[-1]
        
        if file_extension == 'json':
            # Validate JSON format
            content = uploaded_file.read().decode('utf-8')
            uploaded_file.seek(0)  # Reset file pointer
            
            try:
                data = json.loads(content)
                if not isinstance(data, list):
                    st.error("❌ Invalid dataset format: JSON should contain a list of articles")
                    return False
                
                # Check if each item has required fields
                required_fields = ['title', 'content']
                for i, item in enumerate(data[:5]):  # Check first 5 items
                    if not isinstance(item, dict):
                        st.error(f"❌ Invalid dataset format: Item {i+1} should be a dictionary")
                        return False
                    
                    missing_fields = [field for field in required_fields if field not in item]
                    if missing_fields:
                        message = f"Item {i+1} missing fields: {', '.join(missing_fields)}"
                        st.error(f"❌ Invalid dataset format: {message}")
                        return False
                
                st.success("✅ Valid JSON dataset format")
                return True
                
            except json.JSONDecodeError as e:
                st.error(f"❌ Invalid JSON format: {str(e)}")
                return False
                
        elif file_extension == 'jsonl':
            # Validate JSONL format
            content = uploaded_file.read().decode('utf-8')
            uploaded_file.seek(0)  # Reset file pointer
            
            lines = content.strip().split('\n')
            for i, line in enumerate(lines[:5]):  # Check first 5 lines
                try:
                    item = json.loads(line)
                    if not isinstance(item, dict):
                        st.error(f"❌ Invalid JSONL format: Line {i+1} should be a JSON object")
                        return False
                except json.JSONDecodeError as e:
                    st.error(f"❌ Invalid JSON on line {i+1}: {str(e)}")
                    return False
            
            st.success("✅ Valid JSONL dataset format")
            return True
        else:
            st.error("❌ Unsupported file format")
            return False
            
    except Exception as e:
        st.error(f"❌ Error validating dataset: {str(e)}")
        return False


def show_dataset_preview(articles):
    """Show preview of dataset articles"""
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.05) 0%, rgba(16, 185, 129, 0.02) 100%);
                   border-radius: 10px;
                   padding: 1.5rem;
                   margin: 1.5rem 0;
                   border: 1px solid rgba(16, 185, 129, 0.1);
                   box-shadow: 0 2px 8px rgba(16, 185, 129, 0.08);">
            <h3 style="color: #065f46; font-size: 1.3rem; font-weight: 700; margin-bottom: 1rem;">
                📂 Dataset Preview - {len(articles)} Articles
            </h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Show first few articles
    for i, article in enumerate(articles[:3]):
        title = article.get('title', f'Article {i+1}')
        content_preview = article.get('content', '')[:100]
        
        st.markdown(
            f"""
            <div style="background: white; padding: 1rem; margin: 0.5rem 0; border-radius: 8px; border-left: 3px solid #10b981;">
                <h4 style="margin: 0 0 0.5rem 0; color: #1f2937;">{title}</h4>
                <p style="margin: 0; color: #6b7280; font-size: 0.9rem;">{content_preview}{'...' if len(article.get('content', '')) > 100 else ''}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    if len(articles) > 3:
        st.markdown(
            f"""
            <div style="text-align: center; color: #6b7280; font-style: italic; margin: 1rem 0;">
                ... and {len(articles) - 3} more articles
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown("</div>", unsafe_allow_html=True)


def process_dataset_batch(articles: list, filename: str):
    """Process dataset for batch analysis"""
    if not articles:
        st.error("❌ No articles to process")
        return None
    
    try:
        with st.spinner(f"📊 Processing {len(articles)} articles..."):
            # Here you would typically process each article
            # For now, we'll just prepare the data structure
            processed_data = {
                'source': 'uploaded_dataset',
                'filename': filename,
                'article_count': len(articles),
                'articles': articles,
                'batch_mode': True
            }
            
            st.success(f"✅ Successfully processed {len(articles)} articles")
            
            # Show processing options
            st.markdown("### 🎯 Processing Options")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Fetch All Articles**")
                analyze_all = st.button(
                    "📂 Fetch All Articles",
                    type="primary",
                    use_container_width=True,
                    help="Fetch all articles for fact-checking"
                )
            with col2:
                st.markdown("**Select Specific Articles**") 
                select_articles = st.button(
                    "📝 Select Specific Articles",
                    use_container_width=True,
                    help="Choose which articles to fetch"
                )
            
            return {
                'analyze_all': analyze_all,
                'select_articles': select_articles,
                'processed_data': processed_data
            }
            
    except Exception as e:
        st.error(f"❌ Error processing dataset: {str(e)}")
        return None


def create_article_selector(articles: list):
    """Create interface to select specific articles from dataset"""
    st.markdown("### 📝 Select Articles to Analyze")
    
    selected_articles = []
    
    for i, article in enumerate(articles):
        title = article.get('title', f'Article {i+1}')
        content_preview = article.get('content', '')[:150]
        
        if st.checkbox(
            f"**{title}**\n{content_preview}{'...' if len(article.get('content', '')) > 150 else ''}",
            key=f"article_select_{i}"
        ):
            selected_articles.append(article)
    
    if selected_articles:
        st.success(f"✅ Selected {len(selected_articles)} articles")
        
        # Add prominent fetch button with unique name
        st.markdown("**Step 1: Fetch Dataset Articles**")
        fetch_button = st.button(
            f"📂 Fetch from Dataset ({len(selected_articles)})",
            type="primary",
            use_container_width=True,
            help="Click to fetch the selected articles for analysis",
            key="fetch_dataset_button"  # Unique key for dataset handler
        )
        
        return selected_articles, fetch_button
    
    return [], False


def handle_dataset_upload(uploaded_file):
    """Handle the uploaded dataset file"""
    try:
        if not validate_dataset_format(uploaded_file):
            return None, None
            
        file_extension = uploaded_file.name.lower().split('.')[-1]
        
        if file_extension == 'json':
            content = uploaded_file.read().decode('utf-8')
            articles = json.loads(content)
        elif file_extension == 'jsonl':
            content = uploaded_file.read().decode('utf-8')
            lines = content.strip().split('\n')
            articles = [json.loads(line) for line in lines if line.strip()]
        else:
            st.error("❌ Unsupported file format")
            return None, None
        
        show_dataset_preview(articles)
        return articles, uploaded_file.name
        
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        return None, None


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
        
        # Show file info
        file_size = len(uploaded_file.read())
        uploaded_file.seek(0)  # Reset file pointer
        st.info(f"📋 File size: {file_size:,} bytes")
        
        col1, col2 = st.columns(2)
        with col1:
            process_button = st.button(
                "🔄 Process Dataset",
                type="primary",
                use_container_width=True
            )
        with col2:
            download_sample = st.button(
                "📥 Download Sample Format",
                use_container_width=True
            )
    else:
        process_button = False
        download_sample = st.button(
            "📥 Download Sample Format",
            use_container_width=True
        )
    
    return uploaded_file, process_button, download_sample


def show_batch_processing_status(current: int, total: int, article_title: str):
    """Show progress of batch processing"""
    progress = current / total if total > 0 else 0
    
    st.progress(progress)
    st.markdown(
        f"""
        <div style="text-align: center; margin: 1rem 0;">
            <h4 style="color: #1f2937; margin: 0.5rem 0;">Processing Article {current} of {total}</h4>
            <p style="color: #6b7280; margin: 0; font-size: 0.9rem;">{article_title}</p>
        </div>
        """,
        unsafe_allow_html=True
    )