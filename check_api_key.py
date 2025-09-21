from config.config import API_KEYS
import os

print("Environment variable directly:", os.environ.get("SERP_API_KEY"))
print("From API_KEYS:", API_KEYS.get("serp_api"))
