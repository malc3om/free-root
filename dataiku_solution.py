#!/usr/bin/env python3
"""
Dataiku-specific solution for accessing privileged operations.
This script provides alternatives to root access in Dataiku environments.
"""

import os
import sys
import platform
import subprocess
import tempfile
import stat
import urllib.request
import warnings
from pathlib import Path
import shutil
import socket
import getpass
import json

# ANSI Colors
CYAN = '\033[0;36m'
WHITE = '\033[0;37m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
RED = '\033[0;31m'
RESET_COLOR = '\033[0m'

def print_header():
    """Print the header with environment information"""
    print(f"{WHITE}{'='*70}{RESET_COLOR}")
    print(f"{CYAN}                    Dataiku Environment Explorer{RESET_COLOR}")
    print(f"{CYAN}                    Privileged Operations Helper{RESET_COLOR}")
    print(f"{WHITE}{'='*70}{RESET_COLOR}")
    
    # System information
    print(f"Host: {GREEN}{socket.gethostname()}{RESET_COLOR}")
    print(f"User: {GREEN}{getpass.getuser()}{RESET_COLOR}")
    print(f"Python: {GREEN}{sys.version.split()[0]}{RESET_COLOR}")
    print(f"Platform: {GREEN}{platform.platform()}{RESET_COLOR}")
    print(f"Working directory: {GREEN}{os.getcwd()}{RESET_COLOR}")
    
    # Dataiku-specific information
    dataiku_home = os.environ.get('DATAIKU_HOME', 'Not set')
    print(f"DATAIKU_HOME: {GREEN}{dataiku_home}{RESET_COLOR}")
    
    # Check if we're in a container
    in_container = os.path.exists('/.dockerenv')
    print(f"In container: {GREEN}{in_container}{RESET_COLOR}")

def explore_environment():
    """Explore and report on the environment capabilities"""
    print(f"\n{WHITE}{'='*70}{RESET_COLOR}")
    print(f"{CYAN}Exploring Environment Capabilities{RESET_COLOR}")
    print(f"{WHITE}{'='*70}{RESET_COLOR}")
    
    # Check write permissions in key directories
    paths_to_check = [
        '/tmp',
        os.path.expanduser('~'),
        os.environ.get('DATAIKU_HOME', ''),
        '/var/tmp',
        '.'
    ]
    
    print("\nWrite permission check:")
    for path in paths_to_check:
        if path and os.path.exists(path):
            writable = os.access(path, os.W_OK)
            print(f"  {path}: {GREEN if writable else RED}{'WRITABLE' if writable else 'NOT WRITABLE'}{RESET_COLOR}")
    
    # Check for availability of key commands
    print("\nCommand availability:")
    commands_to_check = ['sudo', 'docker', 'kubectl', 'pip', 'apt', 'yum', 'curl', 'wget']
    for cmd in commands_to_check:
        available = shutil.which(cmd) is not None
        print(f"  {cmd}: {GREEN if available else YELLOW}{'AVAILABLE' if available else 'NOT AVAILABLE'}{RESET_COLOR}")
    
    # Check network access
    print("\nNetwork access:")
    try:
        urllib.request.urlopen("https://www.google.com", timeout=3)
        print(f"  Internet access: {GREEN}AVAILABLE{RESET_COLOR}")
    except:
        print(f"  Internet access: {YELLOW}NOT AVAILABLE{RESET_COLOR}")
    
    # Check environment variables
    print("\nRelevant environment variables:")
    relevant_vars = ['PATH', 'PYTHONPATH', 'LD_LIBRARY_PATH', 'DATAIKU_HOME', 'DATAIKU_DATA_DIR']
    for var in relevant_vars:
        if var in os.environ:
            value = os.environ[var]
            if len(value) > 50:
                value = value[:47] + "..."
            print(f"  {var}: {GREEN}{value}{RESET_COLOR}")
    
    # Check installed Python packages
    print("\nKey Python packages:")
    packages_to_check = ['requests', 'numpy', 'pandas', 'dataiku', 'scikit-learn', 'tensorflow']
    for package in packages_to_check:
        try:
            __import__(package)
            print(f"  {package}: {GREEN}INSTALLED{RESET_COLOR}")
        except ImportError:
            print(f"  {package}: {YELLOW}NOT INSTALLED{RESET_COLOR}")

def attempt_privilege_operation():
    """Attempt to find ways to perform privileged operations"""
    print(f"\n{WHITE}{'='*70}{RESET_COLOR}")
    print(f"{CYAN}Attempting Privileged Operations{RESET_COLOR}")
    print(f"{WHITE}{'='*70}{RESET_COLOR}")
    
    # Try to create a file in /tmp
    temp_filename = os.path.join(tempfile.gettempdir(), f"dataiku_test_{os.getpid()}.txt")
    try:
        with open(temp_filename, 'w') as f:
            f.write("Test file for Dataiku permissions")
        print(f"Created test file: {GREEN}{temp_filename}{RESET_COLOR}")
        os.remove(temp_filename)
        print(f"Successfully removed test file")
    except Exception as e:
        print(f"Failed to create/remove file in temp directory: {RED}{str(e)}{RESET_COLOR}")
    
    # Check if Docker is available and can be used
    if shutil.which('docker'):
        print("\nDocker is available. Checking if it can be used:")
        try:
            result = subprocess.run(['docker', 'ps'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
            if result.returncode == 0:
                print(f"{GREEN}Docker is usable! You can run containers.{RESET_COLOR}")
                print("Example to get a root shell: docker run -it --rm ubuntu bash")
            else:
                print(f"{RED}Docker is installed but not usable: {result.stderr}{RESET_COLOR}")
        except Exception as e:
            print(f"{RED}Error checking Docker: {str(e)}{RESET_COLOR}")
    
    # Check if kubectl is available and can be used
    if shutil.which('kubectl'):
        print("\nKubernetes (kubectl) is available. Checking if it can be used:")
        try:
            result = subprocess.run(['kubectl', 'get', 'pods'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
            if result.returncode == 0:
                print(f"{GREEN}kubectl is usable! You can access Kubernetes.{RESET_COLOR}")
            else:
                print(f"{RED}kubectl is installed but not usable: {result.stderr}{RESET_COLOR}")
        except Exception as e:
            print(f"{RED}Error checking kubectl: {str(e)}{RESET_COLOR}")
    
    # Check for sudo capabilities
    if shutil.which('sudo'):
        print("\nSudo is available. Checking if it can be used (without providing a password):")
        try:
            result = subprocess.run(['sudo', '-n', 'id'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
            if result.returncode == 0:
                print(f"{GREEN}Sudo is usable without password! You can run commands as root.{RESET_COLOR}")
                print("Example: sudo id")
            else:
                print(f"{RED}Sudo requires a password or is not available to your user.{RESET_COLOR}")
        except Exception as e:
            print(f"{RED}Error checking sudo: {str(e)}{RESET_COLOR}")

def provide_recommendations():
    """Provide recommendations based on the environment"""
    print(f"\n{WHITE}{'='*70}{RESET_COLOR}")
    print(f"{CYAN}Recommendations for Dataiku{RESET_COLOR}")
    print(f"{WHITE}{'='*70}{RESET_COLOR}")
    
    print(f"""
1. {GREEN}Using Containerized Execution{RESET_COLOR}:
   Dataiku provides a containerized execution environment. This allows your code
   to run in a container with more permissions than your user account.
   
   To use this:
   - Go to Administration > Settings > Containerized execution
   - Set up a containerized execution configuration
   - In your code recipes, select this execution environment

2. {GREEN}Accessing External Resources{RESET_COLOR}:
   You can set up connections to external systems with higher privileges:
   - SSH connections
   - Server command connections
   - Cloud provider connections (AWS, GCP, Azure)
   
3. {GREEN}Code Environments{RESET_COLOR}:
   Create a custom code environment with the packages you need
   installed with proper permissions.
   
4. {GREEN}API Services{RESET_COLOR}:
   Create a separate service outside Dataiku with the privileges
   you need, and call it via API.
   
5. {GREEN}File Operations{RESET_COLOR}:
   Most file operations can be done in your Dataiku project storage
   space without needing root access.
   
6. {GREEN}Container Services{RESET_COLOR}:
   If you have Docker access, you can create services in containers
   with root access and communicate with them.
""")

def main():
    print_header()
    explore_environment()
    attempt_privilege_operation()
    provide_recommendations()
    
    print(f"\n{WHITE}{'='*70}{RESET_COLOR}")
    print(f"{CYAN}                    Execution Complete{RESET_COLOR}")
    print(f"{WHITE}{'='*70}{RESET_COLOR}")

if __name__ == "__main__":
    main()