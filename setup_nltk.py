"""
NLTK Data Installer for DeFacture Project

This script downloads all required NLTK data packages needed for the project.
Run this after installing requirements to ensure all NLP functionality works correctly.
"""

import nltk
import sys

def download_nltk_data():
    """Download all required NLTK data packages"""
    
    required_packages = [
        'punkt',          # Sentence tokenization
        'stopwords',      # Common stopwords
        'averaged_perceptron_tagger',  # Part-of-speech tagging
        'maxent_ne_chunker',  # Named entity recognition
        'words'           # English word list
    ]
    
    print("📦 Installing NLTK data packages...")
    
    for package in required_packages:
        print(f"  - Downloading {package}...")
        try:
            nltk.download(package)
            print(f"    ✅ {package} installed successfully")
        except Exception as e:
            print(f"    ❌ Error installing {package}: {str(e)}")
            
    print("\n✅ NLTK setup complete!")
    print("You can now run the DeFacture application with all NLP capabilities.")

if __name__ == "__main__":
    download_nltk_data()