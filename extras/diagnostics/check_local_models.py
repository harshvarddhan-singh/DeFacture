"""
Check for local model availability and provide setup instructions

This script checks if the required dependencies for local model inference are installed
and provides instructions for setting up the local Phi-2 model if needed.
"""

import importlib.util
import logging
import os
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def check_torch_installation():
    """Check if PyTorch is installed and working"""
    torch_spec = importlib.util.find_spec("torch")
    if torch_spec is None:
        return False
    
    try:
        import torch
        logger.info(f"PyTorch version: {torch.__version__}")
        # Check CUDA availability
        if torch.cuda.is_available():
            logger.info(f"CUDA available: {torch.cuda.get_device_name(0)}")
            logger.info(f"CUDA version: {torch.version.cuda}")
            return True
        else:
            logger.info("CUDA not available, will use CPU for inference (slower)")
            return True
    except ImportError as e:
        logger.error(f"Error importing torch: {e}")
        return False

def check_transformers_installation():
    """Check if Transformers is installed and working"""
    transformers_spec = importlib.util.find_spec("transformers")
    if transformers_spec is None:
        return False
    
    try:
        import transformers
        logger.info(f"Transformers version: {transformers.__version__}")
        return True
    except ImportError as e:
        logger.error(f"Error importing transformers: {e}")
        return False

def check_phi2_model_cache():
    """Check if Phi-2 model is cached locally"""
    try:
        from transformers import AutoTokenizer
        # Try to load just the tokenizer to check if model is cached
        tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2", local_files_only=True)
        logger.info("Phi-2 model found in local cache")
        return True
    except Exception as e:
        logger.warning(f"Phi-2 model not found in local cache: {e}")
        return False

def main():
    """Check local model availability and provide setup instructions"""
    print("\n========== DeFacture Local Model Check ==========\n")
    
    # Check PyTorch installation
    print("Checking PyTorch installation...")
    torch_available = check_torch_installation()
    if not torch_available:
        print("\n❌ PyTorch not found. Please install PyTorch:")
        print("   pip install torch torchvision torchaudio\n")
    else:
        print("✓ PyTorch installation looks good\n")
    
    # Check Transformers installation
    print("Checking Transformers installation...")
    transformers_available = check_transformers_installation()
    if not transformers_available:
        print("\n❌ Transformers not found. Please install Transformers:")
        print("   pip install transformers\n")
    else:
        print("✓ Transformers installation looks good\n")
    
    # Check for Phi-2 model in cache
    if torch_available and transformers_available:
        print("Checking for local Phi-2 model...")
        phi2_available = check_phi2_model_cache()
        if not phi2_available:
            print("\n❌ Phi-2 model not found in local cache.")
            print("   To download the model, run:")
            print("   python -c \"from transformers import AutoModelForCausalLM, AutoTokenizer; AutoModelForCausalLM.from_pretrained('microsoft/phi-2'); AutoTokenizer.from_pretrained('microsoft/phi-2')\"\n")
        else:
            print("✓ Phi-2 model found in local cache\n")
    
    # Summary
    print("\n========== Summary ==========\n")
    if torch_available and transformers_available and (phi2_available if torch_available and transformers_available else False):
        print("✓ All dependencies for local model inference are available")
        print("✓ Local Phi-2 model is ready for use")
        print("  - You can select 'Phi-2 (Local)' in the UI for faster analysis")
    else:
        print("⚠️ Some dependencies for local model inference are missing")
        print("  - The application will fall back to API calls or mock data")
        print("  - Follow the instructions above to enable local model inference")
    
    print("\n===============================\n")

if __name__ == "__main__":
    main()