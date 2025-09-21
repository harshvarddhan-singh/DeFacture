"""
Hugging Face API Setup for DeFacture Project

This script helps users configure their Hugging Face API token
for context analysis in the DeFacture application.

It checks for existing API keys, prompts users to enter their token if missing,
validates the token, and saves it to the .env file.
"""

import os
import sys
import logging
import requests
import subprocess
from pathlib import Path
from dotenv import load_dotenv, find_dotenv, set_key

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_huggingface_api_key():
    """Check if Hugging Face API key is already configured"""
    # Try to load from .env first
    env_path = find_dotenv()
    if env_path:
        load_dotenv(env_path)
    
    # Check if key exists in environment
    hf_api_key = os.environ.get("HUGGINGFACE_API_KEY")
    
    if hf_api_key:
        logger.info("✅ Hugging Face API key found in environment")
        return True, hf_api_key
    else:
        logger.warning("❌ Hugging Face API key not found")
        return False, None

def validate_api_key(api_key):
    """Test if the provided API key is valid by making a simple request"""
    if not api_key:
        return False
    
    # Using a simple model to validate the token
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    try:
        response = requests.get(
            "https://api-inference.huggingface.co/models", 
            headers=headers
        )
        
        if response.status_code == 200:
            logger.info("✅ Hugging Face API key is valid")
            return True
        else:
            logger.error(f"❌ API key validation failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        logger.error(f"❌ Error validating API key: {str(e)}")
        return False

def save_api_key(api_key):
    """Save API key to .env file"""
    try:
        env_path = find_dotenv()
        if not env_path:
            # Create .env file if it doesn't exist
            env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
            with open(env_path, 'w') as f:
                f.write("# Environment variables for DeFacture\n")
        
        # Save key to .env file
        set_key(env_path, "HUGGINGFACE_API_KEY", api_key)
        logger.info(f"✅ API key saved to {env_path}")
        return True
    except Exception as e:
        logger.error(f"❌ Error saving API key: {str(e)}")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    requirements = [
        "requests",
        "python-dotenv"
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
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
        logger.info("✅ All dependencies installed successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Error installing dependencies: {str(e)}")
        return False

def get_api_key_from_user():
    """Prompt user to enter their Hugging Face API key"""
    print("\n" + "="*80)
    print("🤗 Hugging Face API Setup")
    print("="*80)
    print("\nDeFacture needs a Hugging Face API key for context analysis.")
    print("If you don't have one, you can get it for free at: https://huggingface.co/settings/tokens")
    print("\nYour API key will be stored in a local .env file and not shared.")
    
    api_key = input("\nPlease enter your Hugging Face API key: ").strip()
    return api_key if api_key else None

def show_huggingface_info():
    """Show information about Hugging Face API usage"""
    print("\n" + "="*80)
    print("ℹ️ About Hugging Face API Usage")
    print("="*80)
    print("\nDeFacture uses the Hugging Face Inference API for context analysis of articles.")
    print("The API is used to:")
    print("  - Extract claims from articles")
    print("  - Analyze context and detect potential misinformation")
    print("  - Generate context-aware summaries")
    print("\nThe free tier of Hugging Face API allows for:")
    print("  - 30,000 requests per month for most models")
    print("  - Rate limits apply (typically 9 requests/minute)")
    print("\nFor more information, visit: https://huggingface.co/pricing")
    print("="*80 + "\n")

def setup_huggingface_api():
    """Main setup function"""
    print("\n🤗 Setting up Hugging Face API for DeFacture...\n")
    
    # Check and install dependencies
    missing_packages = check_dependencies()
    if missing_packages and not install_dependencies(missing_packages):
        print("\n❌ Setup failed. Please install missing dependencies manually.")
        sys.exit(1)
    
    # Reload modules if they were installed
    if missing_packages:
        try:
            if "python-dotenv" in missing_packages:
                global load_dotenv, find_dotenv, set_key
                from dotenv import load_dotenv, find_dotenv, set_key
            if "requests" in missing_packages:
                global requests
                import requests
        except ImportError:
            print("\n❌ Failed to reload required modules. Please restart the script.")
            sys.exit(1)
    
    # Check for existing API key
    has_key, existing_key = check_huggingface_api_key()
    
    if has_key:
        print("\n✅ Found existing Hugging Face API key.")
        if validate_api_key(existing_key):
            print("\n✅ Your API key is valid and ready to use.")
            return True
        else:
            print("\n❌ Your existing API key is invalid or has expired.")
            should_update = input("Would you like to update it? (y/n): ").lower() == 'y'
            if not should_update:
                print("\n⚠️ DeFacture will use mock data for context analysis.")
                return False
    
    # Show info about Hugging Face API
    show_huggingface_info()
    
    # Get API key from user
    api_key = get_api_key_from_user()
    
    if not api_key:
        print("\n❌ No API key provided. DeFacture will use mock data for context analysis.")
        return False
    
    # Validate API key
    if not validate_api_key(api_key):
        print("\n❌ The provided API key is invalid. Please check and try again.")
        return False
    
    # Save API key
    if save_api_key(api_key):
        print("\n🎉 Hugging Face API setup completed successfully!")
        print("\nYou can now use DeFacture with full context analysis capabilities.")
        return True
    else:
        print("\n❌ Failed to save API key. Please check file permissions and try again.")
        return False

if __name__ == "__main__":
    setup_huggingface_api()