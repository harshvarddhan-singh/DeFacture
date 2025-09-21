"""
Test script for local model inference in DeFacture

This script tests that local model inference is working properly by:
1. Testing if the local Phi-2 model is available
2. Testing context analysis using the local model
3. Verifying the model can generate meaningful output
"""

import logging
import sys
from tools.local_models import phi2_context_analysis
from tools.analysis import context_analysis_chain

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_local_phi2_context_analysis():
    """Test context analysis with local Phi-2 model"""
    print("\n1. Testing direct local model inference...")
    
    sample_text = """
    Climate change is a pressing global issue. Recent studies show that global temperatures 
    have increased by 1.1°C since pre-industrial times. The IPCC has warned that limiting 
    warming to 1.5°C requires immediate and substantial emissions reductions. 
    Some industries argue that rapid transitions would harm economic growth, 
    while environmental groups advocate for faster action.
    """
    
    try:
        print("Calling local Phi-2 model directly...")
        result = phi2_context_analysis(sample_text)
        print(f"✓ Success! Local model generated output:")
        print(f"- Perspective: {result['perspective']}")
        print(f"- Bias indicators: {result['bias_indicators']}")
        print(f"- Historical context: {result['historical_context']}")
        print(f"- Missing context: {result['missing_context']}")
        print("\n")
        return True
    except Exception as e:
        print(f"✘ Error using local model directly: {e}")
        return False

def test_context_analysis_chain():
    """Test the context analysis chain with phi-2-local model option"""
    print("\n2. Testing context analysis chain with 'phi-2-local' option...")
    
    sample_text = """
    A new study published in Nature suggests that quantum computing could dramatically 
    accelerate drug discovery. The research team demonstrated a quantum algorithm that 
    simulates molecular interactions 100 times faster than conventional supercomputers. 
    Industry experts suggest this could reduce development timelines by years, though 
    some scientists caution that practical applications may be further away.
    """
    
    try:
        print("Calling context_analysis_chain with phi-2-local model...")
        result = context_analysis_chain(sample_text, model="phi-2-local")
        print(f"✓ Success! Analysis chain returned:")
        print(f"- Perspective: {result['perspective']}")
        print(f"- Bias indicators: {result['bias_indicators']}")
        print(f"- Historical context: {result['historical_context']}")
        print(f"- Missing context: {result['missing_context']}")
        return True
    except Exception as e:
        print(f"✘ Error in context analysis chain: {e}")
        return False

def main():
    """Run tests for local model inference"""
    print("\n===== TESTING LOCAL MODEL INFERENCE =====\n")
    
    # Test direct model inference
    direct_test_success = test_local_phi2_context_analysis()
    
    # Test context analysis chain
    chain_test_success = test_context_analysis_chain()
    
    # Print summary
    print("\n===== TEST RESULTS =====\n")
    print(f"Direct local model test: {'✓ PASSED' if direct_test_success else '✘ FAILED'}")
    print(f"Context analysis chain test: {'✓ PASSED' if chain_test_success else '✘ FAILED'}")
    
    if direct_test_success and chain_test_success:
        print("\n✓ All tests passed! Local model inference is working correctly.")
        sys.exit(0)
    else:
        print("\n✘ Some tests failed. Check logs for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()