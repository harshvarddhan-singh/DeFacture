"""
Simple script to check if environment variables are loaded correctly from .env
"""
import os
import sys
from pathlib import Path

# Get the project root directory
root_dir = Path(__file__).parent

print(f"Project root directory: {root_dir}")
print(f".env file exists: {(root_dir / '.env').exists()}")
print(f".env file content:")

try:
    with open(root_dir / '.env', 'r') as f:
        env_content = f.read()
        print(env_content)
except Exception as e:
    print(f"Error reading .env file: {e}")

print("\nTrying to load .env with python-dotenv:")
try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=root_dir / '.env')
    print("dotenv loaded successfully")
except ImportError:
    print("python-dotenv not installed")
except Exception as e:
    print(f"Error loading .env with dotenv: {e}")

print("\nEnvironment variables:")
print(f"SERP_API_KEY: {os.environ.get('SERP_API_KEY', 'Not set')}")
print(f"LANGCHAIN_API_KEY: {os.environ.get('LANGCHAIN_API_KEY', 'Not set')}")
print(f"GOOGLE_SEARCH_API_KEY: {os.environ.get('GOOGLE_SEARCH_API_KEY', 'Not set')}")