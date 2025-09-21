"""
Simple test to verify if we can load the Phi-2 tokenizer
"""

from transformers import AutoTokenizer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Test loading the Phi-2 tokenizer"""
    print("Attempting to load Phi-2 tokenizer...")
    try:
        tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2")
        print(f"Successfully loaded Phi-2 tokenizer (vocabulary size: {len(tokenizer)})")
        print("Tokenizer type:", type(tokenizer))
        print("Sample tokenization:", tokenizer("Hello, world!"))
    except Exception as e:
        print(f"Error loading Phi-2 tokenizer: {e}")

if __name__ == "__main__":
    main()