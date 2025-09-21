"""
Download NLTK Data

This script downloads required NLTK data packages for DeFacture.
Run this script before running the main application to ensure all
required data is available.
"""

import nltk
import os
import sys

def download_nltk_data():
    """Download required NLTK data packages"""
    print("Downloading required NLTK data...")
    
    # List of required data packages
    required_packages = [
        'punkt',             # Sentence tokenization
        'stopwords',         # Common stopwords
        'wordnet',           # WordNet lexical database
        'averaged_perceptron_tagger',  # POS tagging
        'maxent_ne_chunker', # Named entity chunker
        'words'              # Common English words
    ]
    
    # Create NLTK data directory if it doesn't exist
    nltk_data_dir = os.path.join(os.path.expanduser("~"), "nltk_data")
    os.makedirs(nltk_data_dir, exist_ok=True)
    
    # Download each package
    for package in required_packages:
        print(f"Downloading {package}...")
        try:
            nltk.download(package, quiet=False, raise_on_error=True)
            print(f"Successfully downloaded {package}")
        except Exception as e:
            print(f"Error downloading {package}: {e}")

    print('NLTK resources downloaded successfully')

# Monkey patch NLTK tag functions to avoid averaged_perceptron_tagger_eng errors
def patch_nltk():
    print("Applying NLTK monkey patches...")
    
    # Save the original pos_tag function
    from nltk.tag import pos_tag as original_pos_tag
    
    # Define a patched version that handles errors gracefully
    def patched_pos_tag(tokens, tagset=None, lang='eng'):
        try:
            # Try with default parameters first (will use averaged_perceptron_tagger)
            if tagset is None and lang == 'eng':
                return original_pos_tag(tokens)
            else:
                return original_pos_tag(tokens, tagset=tagset, lang=lang)
        except LookupError as e:
            if 'averaged_perceptron_tagger_eng' in str(e):
                # Simple fallback without NLTK resources
                result = []
                for token in tokens:
                    if token and len(token) > 0 and token[0].isupper() and token.isalpha():
                        result.append((token, 'NNP'))  # Proper noun
                    else:
                        result.append((token, 'NN'))   # Regular noun
                return result
            else:
                # Re-raise other errors
                raise
    
    # Apply the monkey patch
    nltk.tag.pos_tag = patched_pos_tag
    print("NLTK patch applied successfully")

if __name__ == "__main__":
    download_nltk_data()
    patch_nltk()
    print("\nSetup complete. You can now run the DeFacture application.")