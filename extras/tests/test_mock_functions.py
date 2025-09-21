"""
Test for mock functionality in DeFacture

This script tests that the mock functions work correctly without requiring any external models or APIs.
"""

import sys
from tools.analysis import mock_context_analysis_chain, mock_summarization_chain, mock_related_articles_chain

def test_mock_context():
    """Test mock context analysis"""
    print("Testing mock context analysis...")
    
    sample_text = "This is a sample article for testing."
    
    try:
        result = mock_context_analysis_chain(sample_text)
        print("✓ Mock context analysis successful")
        print(f"  - Perspective: {result['perspective']}")
        print(f"  - Bias indicators: {result['bias_indicators']}")
        print(f"  - Historical context: {result['historical_context']}")
        print(f"  - Missing context: {result['missing_context']}")
        return True
    except Exception as e:
        print(f"✘ Error in mock context analysis: {e}")
        return False

def test_mock_summary():
    """Test mock summarization"""
    print("\nTesting mock summarization...")
    
    sample_text = "This is a sample article for testing."
    
    try:
        result = mock_summarization_chain(sample_text)
        print("✓ Mock summarization successful")
        print(f"  Summary: {result}")
        return True
    except Exception as e:
        print(f"✘ Error in mock summarization: {e}")
        return False

def test_mock_related():
    """Test mock related articles"""
    print("\nTesting mock related articles...")
    
    sample_text = "This is a sample article for testing."
    
    try:
        result = mock_related_articles_chain(sample_text)
        print("✓ Mock related articles successful")
        print(f"  Found {len(result)} related articles")
        for i, article in enumerate(result):
            print(f"  {i+1}. {article['title']} ({article['source']})")
        return True
    except Exception as e:
        print(f"✘ Error in mock related articles: {e}")
        return False

def main():
    """Run tests for mock functionality"""
    print("\n===== TESTING MOCK FUNCTIONALITY =====\n")
    
    context_ok = test_mock_context()
    summary_ok = test_mock_summary()
    related_ok = test_mock_related()
    
    print("\n===== TEST RESULTS =====")
    print(f"Mock context test: {'✓ PASSED' if context_ok else '✘ FAILED'}")
    print(f"Mock summary test: {'✓ PASSED' if summary_ok else '✘ FAILED'}")
    print(f"Mock related test: {'✓ PASSED' if related_ok else '✘ FAILED'}")
    
    if context_ok and summary_ok and related_ok:
        print("\n✓ All mock functionality tests passed!")
        sys.exit(0)
    else:
        print("\n✘ Some tests failed. Check logs for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()