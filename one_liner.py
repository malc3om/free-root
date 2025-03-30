#!/usr/bin/env python3
"""
This script is designed to be run as a one-liner in Python environments such as Jupyter notebooks.
It downloads and executes the freeroot.py script without requiring any user interaction.

Usage:
!pip install requests && python -c "import requests; exec(requests.get('https://raw.githubusercontent.com/malc3om/free-root/main/one_liner.py').text)"
"""

import os
import sys
import platform
import subprocess
import tempfile
import shutil
import stat
from pathlib import Path
import requests

# Function to download the main script and execute it
def download_and_run():
    try:
        # Download the main script
        response = requests.get('https://raw.githubusercontent.com/malc3om/free-root/main/freeroot.py')
        response.raise_for_status()
        
        # Execute the script
        exec(response.text)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Make sure requests is installed
    try:
        import requests
    except ImportError:
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        import requests
    
    # Run the main function
    download_and_run()