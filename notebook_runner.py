#!/usr/bin/env python3
"""
This script is specifically designed for running in Jupyter notebooks.
It provides a simple function to execute the freeroot environment with a single function call.

Example usage in a notebook cell:
```python
import requests
exec(requests.get('https://raw.githubusercontent.com/malc3om/free-root/main/notebook_runner.py').text)
run_freeroot()
```
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path
import requests

def run_freeroot():
    """
    Main function to download and run the freeroot environment.
    This function handles all the steps required to setup and execute the root environment.
    """
    print("Starting FreeRoot environment setup...")
    
    # Make sure requests is installed
    try:
        import requests
    except ImportError:
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        import requests
    
    # Download the main script
    try:
        response = requests.get('https://raw.githubusercontent.com/malc3om/free-root/main/freeroot.py')
        response.raise_for_status()
        
        # Execute the script
        exec(response.text)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

# Only run automatically if called directly, not when imported
if __name__ == "__main__":
    run_freeroot()