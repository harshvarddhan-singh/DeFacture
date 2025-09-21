"""
Diagnostic script for Phi-2 model loading issues

This script provides detailed diagnostics for why the Phi-2 model might not be loading properly.
"""

import os
import sys
import logging
import importlib.util
import platform
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_system_info():
    """Check system information"""
    print("\n==== SYSTEM INFORMATION ====")
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Python version: {platform.python_version()}")
    print(f"Platform: {platform.platform()}")
    print(f"Processor: {platform.processor()}")
    
    # Check memory
    try:
        import psutil
        mem = psutil.virtual_memory()
        print(f"Memory: {mem.total / (1024**3):.2f} GB (Available: {mem.available / (1024**3):.2f} GB)")
    except ImportError:
        print("Memory: Could not determine (psutil not installed)")

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("\n==== DEPENDENCY CHECK ====")
    
    dependencies = [
        "torch", 
        "transformers", 
        "streamlit", 
        "nltk", 
        "numpy", 
        "huggingface_hub"
    ]
    
    for package in dependencies:
        spec = importlib.util.find_spec(package)
        if spec is None:
            print(f"❌ {package}: Not installed")
            continue
            
        try:
            module = importlib.import_module(package)
            if hasattr(module, '__version__'):
                print(f"✅ {package}: v{module.__version__}")
            else:
                print(f"✅ {package}: Installed (version unknown)")
        except ImportError as e:
            print(f"❌ {package}: Error importing ({e})")

def check_cache_dir():
    """Check Hugging Face cache directory"""
    print("\n==== HUGGING FACE CACHE ====")
    
    # Check default cache location
    home_dir = os.path.expanduser("~")
    cache_dirs = [
        os.path.join(home_dir, ".cache", "huggingface"),  # Linux/Mac
        os.path.join(home_dir, "AppData", "Local", "huggingface", "cache")  # Windows
    ]
    
    cache_dir = None
    for dir_path in cache_dirs:
        if os.path.exists(dir_path):
            cache_dir = dir_path
            print(f"Cache directory found at: {cache_dir}")
            break
    
    if cache_dir is None:
        print("❌ No Hugging Face cache directory found")
        return
        
    # Check if Phi-2 model is in cache
    phi2_dirs = []
    for root, dirs, _ in os.walk(cache_dir):
        if "phi-2" in root.lower():
            phi2_dirs.append(root)
    
    if phi2_dirs:
        print(f"✅ Found {len(phi2_dirs)} directories related to Phi-2:")
        for dir_path in phi2_dirs:
            dir_size = get_dir_size(dir_path)
            print(f"  - {dir_path} ({format_size(dir_size)})")
    else:
        print("❌ No Phi-2 model files found in cache")
        
    # Check total cache size
    cache_size = get_dir_size(cache_dir)
    print(f"Total cache size: {format_size(cache_size)}")

def get_dir_size(path):
    """Get directory size in bytes"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total_size += os.path.getsize(fp)
    return total_size

def format_size(size_in_bytes):
    """Format size in bytes to human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} TB"

def check_torch_cuda():
    """Check PyTorch CUDA availability"""
    print("\n==== PYTORCH CUDA CHECK ====")
    
    try:
        import torch
        print(f"PyTorch version: {torch.__version__}")
        
        if torch.cuda.is_available():
            print(f"✅ CUDA available: {torch.cuda.get_device_name(0)}")
            print(f"CUDA version: {torch.version.cuda}")
            print(f"GPU count: {torch.cuda.device_count()}")
            for i in range(torch.cuda.device_count()):
                print(f"  GPU {i}: {torch.cuda.get_device_name(i)}")
                print(f"    Memory: {torch.cuda.get_device_properties(i).total_memory / (1024**3):.2f} GB")
        else:
            print("❌ CUDA not available, will use CPU only")
            
    except ImportError:
        print("❌ Could not import torch")
    except Exception as e:
        print(f"❌ Error checking CUDA: {e}")

def check_transformers_config():
    """Check Transformers configuration"""
    print("\n==== TRANSFORMERS CONFIG ====")
    
    try:
        import transformers
        print(f"Transformers version: {transformers.__version__}")
        
        # Check if transformers is configured properly
        try:
            from transformers import AutoTokenizer
            print("✅ AutoTokenizer import successful")
        except Exception as e:
            print(f"❌ Error importing AutoTokenizer: {e}")
            
        try:
            from transformers import AutoModelForCausalLM
            print("✅ AutoModelForCausalLM import successful")
        except Exception as e:
            print(f"❌ Error importing AutoModelForCausalLM: {e}")
            
    except ImportError:
        print("❌ Could not import transformers")

def try_minimal_model_load():
    """Try to load a minimal model to test basic functionality"""
    print("\n==== MINIMAL MODEL TEST ====")
    
    try:
        from transformers import AutoTokenizer
        print("Trying to load a small tokenizer (GPT-2) to test basic functionality...")
        tokenizer = AutoTokenizer.from_pretrained("gpt2")
        print(f"✅ Successfully loaded GPT-2 tokenizer (vocabulary size: {len(tokenizer)})")
    except Exception as e:
        print(f"❌ Error loading GPT-2 tokenizer: {e}")

def main():
    """Run diagnostic checks"""
    print("\n===== PHI-2 MODEL DIAGNOSTIC TOOL =====")
    
    check_system_info()
    check_dependencies()
    check_cache_dir()
    check_torch_cuda()
    check_transformers_config()
    try_minimal_model_load()
    
    print("\n===== DIAGNOSTIC COMPLETE =====")
    
if __name__ == "__main__":
    main()