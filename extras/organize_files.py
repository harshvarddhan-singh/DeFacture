"""
Script to organize DeFacture project files.

This script moves non-essential Python files to an 'extras' directory
to clean up the root directory of the project.
"""

import os
import shutil
from pathlib import Path

# Create extras directory if it doesn't exist
extras_dir = Path("extras")
extras_dir.mkdir(exist_ok=True)

# Create subdirectories in extras
diagnostics_dir = extras_dir / "diagnostics"
setup_dir = extras_dir / "setup"
tests_dir = extras_dir / "tests"
diagnostics_dir.mkdir(exist_ok=True)
setup_dir.mkdir(exist_ok=True)
tests_dir.mkdir(exist_ok=True)

# Files to move to extras/diagnostics
diagnostic_files = [
    "check_api_key.py",
    "check_env.py",
    "check_local_models.py",
    "diagnose_phi2_model.py",
    "refactoring_summary.py"
]

# Files to move to extras/setup
setup_files = [
    "setup_huggingface_api.py",
    "setup_nltk.py",
    "setup_related_articles.py",
    "fix_nltk_issues.py",
    "cleanup_complete.py"
]

# Files to move to extras/tests
test_files = [
    "test_basic.py",
    "test_huggingface_api.py",
    "test_keyword_extraction.py",
    "test_local_models.py",
    "test_mock_functions.py",
    "test_phi2_tokenizer.py",
    "test_ui_local_model.py"
]

# Move diagnostic files
for file in diagnostic_files:
    if os.path.exists(file):
        shutil.move(file, diagnostics_dir / file)
        print(f"Moved {file} to extras/diagnostics/")

# Move setup files
for file in setup_files:
    if os.path.exists(file):
        shutil.move(file, setup_dir / file)
        print(f"Moved {file} to extras/setup/")

# Move test files
for file in test_files:
    if os.path.exists(file):
        shutil.move(file, tests_dir / file)
        print(f"Moved {file} to extras/tests/")

print("\nCleanup complete. Unnecessary files have been moved to the 'extras' directory.")
print("- Core application files remain in the root directory")
print("- Diagnostic tools are in extras/diagnostics/")
print("- Setup scripts are in extras/setup/")
print("- Informal tests are in extras/tests/")
print("- Formal tests remain in the 'tests' directory")