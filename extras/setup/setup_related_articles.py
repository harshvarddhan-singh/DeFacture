"""
Setup Related Articles Environment

This script helps set up the environment for the related articles feature by:
1. Checking if required dependencies are installed
2. Downloading necessary NLTK data
3. Downloading sentence-transformers model
4. Installing other required packages
"""

import os
import sys
import logging
import subprocess
from pathlib import Path
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_dependencies():
    """Check if required dependencies are installed"""
    requirements = [
        "sentence-transformers",
        "nltk",
        "numpy",
        "transformers",
        "torch"
    ]
    
    missing = []
    for package in requirements:
        try:
            __import__(package.replace("-", "_"))
            logger.info(f"✅ {package} is installed")
        except ImportError:
            missing.append(package)
            logger.warning(f"❌ {package} is missing")
    
    return missing

def install_dependencies(missing_packages):
    """Install missing dependencies"""
    if not missing_packages:
        return True
    
    logger.info(f"Installing missing dependencies: {', '.join(missing_packages)}")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install"] + missing_packages,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error installing packages: {e}")
        return False

def download_nltk_data():
    """Download required NLTK data"""
    import nltk
    
    nltk_packages = [
        "punkt",
        "stopwords",
        "averaged_perceptron_tagger",
        "words"
    ]
    
    for package in nltk_packages:
        try:
            nltk.download(package, quiet=True)
            logger.info(f"✅ Downloaded NLTK package: {package}")
        except Exception as e:
            logger.error(f"❌ Error downloading NLTK package {package}: {e}")
    
    return True

def download_sentence_transformers_model():
    """Download the sentence-transformers model"""
    try:
        logger.info("Downloading sentence-transformers model...")
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        logger.info(f"✅ Successfully downloaded sentence-transformers model")
        return True
    except Exception as e:
        logger.error(f"❌ Error downloading sentence-transformers model: {e}")
        return False

def download_explanation_model():
    """Download the explanation model"""
    try:
        logger.info("Downloading explanation model (flan-t5-small)...")
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        
        tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
        model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")
        
        logger.info(f"✅ Successfully downloaded explanation model")
        return True
    except Exception as e:
        logger.error(f"❌ Error downloading explanation model: {e}")
        return False

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Setup Related Articles Environment")
    
    parser.add_argument("--install-deps", action="store_true", help="Install missing dependencies")
    parser.add_argument("--download-nltk", action="store_true", help="Download NLTK data")
    parser.add_argument("--download-models", action="store_true", help="Download sentence-transformers and explanation models")
    parser.add_argument("--all", action="store_true", help="Perform all setup steps")
    
    args = parser.parse_args()
    
    # Check if any actions were specified
    if not (args.install_deps or args.download_nltk or args.download_models or args.all):
        parser.print_help()
        return
    
    # Check for missing dependencies
    missing_packages = check_dependencies()
    
    # Install missing dependencies
    if args.install_deps or args.all:
        if missing_packages:
            logger.info("Installing missing dependencies...")
            if not install_dependencies(missing_packages):
                logger.error("Failed to install dependencies. Please install them manually.")
                return
        else:
            logger.info("All required packages are already installed.")
    
    # Download NLTK data
    if args.download_nltk or args.all:
        logger.info("Downloading NLTK data...")
        download_nltk_data()
    
    # Download models
    if args.download_models or args.all:
        logger.info("Downloading required models...")
        download_sentence_transformers_model()
        download_explanation_model()
    
    logger.info("Setup completed!")

if __name__ == "__main__":
    main()