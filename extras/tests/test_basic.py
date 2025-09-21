"""
Simple test for DeFacture app components
"""

import sys
import os

def test_imports():
    """Test that we can import all necessary modules"""
    print("Testing imports...")
    
    try:
        print("Importing streamlit...")
        import streamlit as st
        print("✓ Streamlit import successful")
    except ImportError as e:
        print(f"✘ Error importing streamlit: {e}")
        return False

    try:
        print("Importing analysis module...")
        from tools.analysis import context_analysis_chain
        print("✓ Analysis module import successful")
    except ImportError as e:
        print(f"✘ Error importing analysis module: {e}")
        return False
        
    try:
        print("Checking for local models module...")
        import importlib.util
        spec = importlib.util.find_spec("tools.local_models")
        if spec is None:
            print("✘ Local models module not found")
            return False
        print("✓ Local models module found")
    except Exception as e:
        print(f"✘ Error checking for local models: {e}")
        return False
    
    return True

def test_file_structure():
    """Test that all required files exist"""
    print("\nChecking file structure...")
    
    required_files = [
        "main.py",
        "tools/analysis.py",
        "tools/huggingface_api.py",
        "tools/local_models.py",
        "ui_components/analysis_tabs.py",
        "check_local_models.py"
    ]
    
    all_files_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ Found {file_path}")
        else:
            print(f"✘ Missing {file_path}")
            all_files_exist = False
    
    return all_files_exist

def main():
    """Run basic tests for DeFacture app"""
    print("\n===== BASIC TESTS FOR DEFACTURE APP =====\n")
    
    imports_ok = test_imports()
    files_ok = test_file_structure()
    
    print("\n===== TEST RESULTS =====")
    print(f"Imports test: {'✓ PASSED' if imports_ok else '✘ FAILED'}")
    print(f"File structure test: {'✓ PASSED' if files_ok else '✘ FAILED'}")
    
    if imports_ok and files_ok:
        print("\n✓ All basic tests passed!")
        sys.exit(0)
    else:
        print("\n✘ Some tests failed. Check logs for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()