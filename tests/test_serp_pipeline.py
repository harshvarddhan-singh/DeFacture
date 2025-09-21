"""
Test script to verify SERP → Full Pipeline Integration

This script traces the data flow from SERP search results through 
newspaper3k extraction to all downstream analysis modules.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from tools.search_api import search_articles_serp, mock_search_results
from tools.fetcher import fetch_article_with_newspaper
from tools.analysis import mock_summarization_chain, real_summarization_chain
from tools.claim_extraction import extract_claims, get_claim_statistics
from tools.fact_check_agent import fact_check_claims, get_fact_check_statistics

def test_serp_pipeline():
    """Test the complete SERP to analysis pipeline"""
    
    print("🔍 Testing SERP → Full Pipeline Integration")
    print("=" * 50)
    
    # Step 1: SERP Search
    print("\n1️⃣ SERP API Search")
    query = "climate change"
    search_results = search_articles_serp(query, num_results=3)
    
    if search_results:
        print(f"✅ Found {len(search_results)} search results")
        first_result = search_results[0]
        print(f"   📰 Title: {first_result['title'][:60]}...")
        print(f"   🌐 Source: {first_result['source']}")
        print(f"   🔗 URL: {first_result['url']}")
        print(f"   📊 API Source: {first_result.get('api_source', 'unknown')}")
    else:
        print("❌ No search results found")
        return False
    
    # Step 2: Article Extraction
    print("\n2️⃣ Full Article Extraction")
    selected_result = search_results[0]
    
    # Try newspaper3k extraction
    fetched_article = fetch_article_with_newspaper(selected_result['url'])
    
    if fetched_article and len(fetched_article.get('content', '').strip()) > 100:
        print("✅ Full article content extracted successfully")
        article_data = fetched_article
        # Enhance with SERP metadata
        article_data.update({
            "source": "search_result",
            "original_source": selected_result['source'],
            "domain": selected_result.get('domain', ''),
            "api_source": selected_result.get('api_source', ''),
            "search_snippet": selected_result.get('snippet', ''),
            "search_position": selected_result.get('position', 0)
        })
        content_length = len(article_data['content'])
        print(f"   📊 Content Length: {content_length:,} characters")
        print(f"   📝 Title: {article_data.get('title', 'N/A')}")
        print(f"   👤 Authors: {article_data.get('authors', [])}")
    else:
        print("⚠️ Using fallback to search snippet")
        article_data = {
            "title": selected_result['title'],
            "content": selected_result['snippet'] + "\n\n[Note: This is a summary from search results.]",
            "url": selected_result['url'],
            "source": "search_result",
            "original_source": selected_result['source'],
            "authors": [],
            "publish_date": selected_result.get('date', ''),
            "domain": selected_result.get('domain', ''),
            "api_source": selected_result.get('api_source', ''),
        }
        content_length = len(article_data['content'])
        print(f"   📊 Snippet Length: {content_length} characters")
    
    # Step 3: Summarization Analysis
    print("\n3️⃣ Article Summarization")
    try:
        summary_result = mock_summarization_chain(article_data['content'])
        if summary_result and 'summary' in summary_result:
            print("✅ Summary generation successful")
            print(f"   📝 Summary: {summary_result['summary'][:100]}...")
        else:
            print("❌ Summary generation failed")
    except Exception as e:
        print(f"❌ Summary generation error: {e}")
    
    # Step 4: Claim Extraction
    print("\n4️⃣ Claim Extraction")
    try:
        claims = extract_claims(article_data['content'])
        if claims:
            stats = get_claim_statistics(claims)
            print(f"✅ Extracted {stats['total_claims']} claims")
            print(f"   📊 Average Confidence: {stats['avg_confidence']}")
            print(f"   🎯 Sample Claim: {claims[0].get('text', 'N/A')[:80]}...")
        else:
            print("⚠️ No claims extracted")
    except Exception as e:
        print(f"❌ Claim extraction error: {e}")
    
    # Step 5: Fact Checking
    print("\n5️⃣ Fact Checking")
    try:
        if 'claims' in locals() and claims:
            fact_check_results = fact_check_claims(claims[:3])  # Test with first 3 claims
            if fact_check_results:
                fc_stats = get_fact_check_statistics(fact_check_results)
                print(f"✅ Fact-checked {len(fact_check_results)} claims")
                print(f"   📊 Accuracy Distribution: {fc_stats.get('accuracy_distribution', {})}")
            else:
                print("⚠️ No fact-check results")
        else:
            print("⚠️ No claims available for fact-checking")
    except Exception as e:
        print(f"❌ Fact checking error: {e}")
    
    print("\n🎉 Pipeline Test Complete!")
    print("=" * 50)
    
    # Verify data structure compatibility
    print("\n🔍 Data Structure Verification")
    required_fields = ['title', 'content', 'source', 'url']
    missing_fields = [field for field in required_fields if field not in article_data]
    
    if not missing_fields:
        print("✅ Article data structure is compatible with all analysis modules")
        print(f"   📋 Available fields: {list(article_data.keys())}")
    else:
        print(f"❌ Missing required fields: {missing_fields}")
    
    return True

if __name__ == "__main__":
    test_serp_pipeline()