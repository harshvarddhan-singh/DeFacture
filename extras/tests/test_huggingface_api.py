"""
Test script for Hugging Face API integration

This script tests that the Hugging Face API integration is working properly.
"""

import os
import sys
from tools.huggingface_api import get_api_key, huggingface_context_analysis

def test_api_key():
    """Test that we can get the API key"""
    print("Testing API key retrieval...")
    
    api_key = get_api_key()
    if api_key:
        print(f"✓ API key found (length: {len(api_key)})")
        # Mask the key for security
        masked_key = api_key[:4] + "*" * (len(api_key) - 8) + api_key[-4:] if len(api_key) > 8 else "****"
        print(f"  Key starts with: {masked_key}")
        return True
    else:
        print("✘ API key not found")
        return False

def test_mock_analysis():
    """Test the mock analysis"""
    print("\nTesting mock analysis...")
    
    sample_text = "This is a test article for mock analysis."
    
    try:
        result = huggingface_context_analysis(sample_text, model="mock")
        print("✓ Mock analysis successful")
        print(f"  - Perspective: {result['perspective']}")
        print(f"  - Bias indicators: {result['bias_indicators']}")
        print(f"  - Historical context: {result['historical_context']}")
        print(f"  - Missing context: {result['missing_context']}")
        return True
    except Exception as e:
        print(f"✘ Error in mock analysis: {e}")
        return False

def main():
    """Run tests for Hugging Face API integration"""
    print("\n===== TESTING HUGGINGFACE API INTEGRATION =====\n")
    
    api_key_ok = test_api_key()
    mock_ok = test_mock_analysis()
    
    print("\n===== TEST RESULTS =====")
    print(f"API key test: {'✓ PASSED' if api_key_ok else '✘ FAILED'}")
    print(f"Mock analysis test: {'✓ PASSED' if mock_ok else '✘ FAILED'}")
    
    if api_key_ok and mock_ok:
        print("\n✓ All API tests passed!")
        sys.exit(0)
    else:
        print("\n✘ Some tests failed. Check logs for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()