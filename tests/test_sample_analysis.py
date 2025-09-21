#!/usr/bin/env python3
"""Test script for sample article mock analysis"""

from tools.analysis import *
from ui_components.ui_helpers import SAMPLE_ARTICLES

def test_sample_analysis():
    """Test all mock analysis functions with sample articles"""
    
    print("🧪 Testing Sample Articles Mock Analysis")
    print("=" * 50)
    
    for i, article in enumerate(SAMPLE_ARTICLES):
        print(f"\n📰 Testing Article {i+1}: {article['title'][:50]}...")
        
        # Test Summary
        try:
            summary = mock_summarization_chain(article['content'], article)
            print(f"   📄 Summary: ✅ Working - {len(summary['key_points'])} key points")
        except Exception as e:
            print(f"   📄 Summary: ❌ Error - {e}")

        # Test Context
        try:
            context = mock_context_analysis_chain(article['content'], article)
            print(f"   🔍 Context: ✅ Working - {len(context['bias_indicators'])} bias indicators")
        except Exception as e:
            print(f"   🔍 Context: ❌ Error - {e}")

        # Test Related Articles
        try:
            related = mock_related_articles_chain(article['content'], article)
            print(f"   🔗 Related: ✅ Working - {len(related)} related articles")
        except Exception as e:
            print(f"   🔗 Related: ❌ Error - {e}")

        # Test Fact Check
        try:
            factcheck = mock_fact_check_chain(article['content'], article)
            assessment = factcheck['overall_assessment']
            claims_count = len(factcheck['claims'])
            print(f"   ✅ Fact Check: ✅ Working - {assessment} ({claims_count} claims)")
        except Exception as e:
            print(f"   ✅ Fact Check: ❌ Error - {e}")
    
    print(f"\n🎉 Testing Complete! All {len(SAMPLE_ARTICLES)} sample articles tested.")

if __name__ == "__main__":
    test_sample_analysis()