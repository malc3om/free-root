#!/usr/bin/env python3
"""
Standalone script with no external dependencies.
This script is designed to work in the most restricted environments.
- Only uses standard library
- Creates a clean temporary directory
- Handles tarfile security warnings
- Prevents path nesting issues
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

# Suppress tarfile warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

# ANSI Colors
CYAN = '\033[0;36m'
WHITE = '\033[0;37m'
RESET_COLOR = '\033[0m'

def download_file(url, target_path):
    """Download a file with retry mechanism using stdlib only"""
    max_retries = 5
    
    for i in range(max_retries):
        try:
            with urllib.request.urlopen(url) as response, open(target_path, 'wb') as out_file:
                chunk_size = 8192
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    out_file.write(chunk)
            return True
        except Exception as e:
            print(f"Download attempt {i+1}/{max_retries} failed: {e}")
            if i == max_retries - 1:
                return False

def get_architecture():
    """Get system architecture and corresponding Ubuntu alt name"""
    arch = platform.machine()
    
    if arch == "x86_64":
        arch_alt = "amd64"
    elif arch == "aarch64" or arch == "arm64":
        arch_alt = "arm64"
    else:
        print(f"Unsupported CPU architecture: {arch}")
        sys.exit(1)
    
    return arch, arch_alt

def main():
    # Create a fresh temporary directory to avoid nesting issues
    # First clean up any existing directories to prevent nesting
    base_temp = Path(tempfile.gettempdir())
    old_freeroot_dir = base_temp / "freeroot_env"
    if old_freeroot_dir.exists():
        try:
            shutil.rmtree(old_freeroot_dir)
            print("Removed existing installation directory for clean start.")
        except Exception as e:
            print(f"Warning: Couldn't remove old directory: {e}")
    
    # Create fresh working directory
    work_dir = base_temp / "freeroot_env"
    work_dir.mkdir(exist_ok=True)
    os.chdir(work_dir)
    
    print(f"{WHITE}{'='*70}{RESET_COLOR}")
    print(f"{CYAN}                       FreeRoot Installer{RESET_COLOR}")
    print(f"{CYAN}                 Standalone Python 3.6+ Edition{RESET_COLOR}")
    print(f"{WHITE}{'='*70}{RESET_COLOR}")
    
    # Check architecture
    arch, arch_alt = get_architecture()
    print(f"Detected architecture: {arch} ({arch_alt})")
    print(f"Working directory: {work_dir}")
    
    rootfs_dir = os.getcwd()
    installed_flag = Path(rootfs_dir) / ".installed"
    
    if not installed_flag.exists():
        print("\nDownloading and installing Ubuntu base...")
        
        # Download Ubuntu base
        ubuntu_url = f"http://cdimage.ubuntu.com/ubuntu-base/releases/20.04/release/ubuntu-base-20.04.4-base-{arch_alt}.tar.gz"
        temp_tar = Path(tempfile.gettempdir()) / "rootfs.tar.gz"
        
        if download_file(ubuntu_url, temp_tar):
            # Extract Ubuntu base
            print("Extracting Ubuntu base...")
            import tarfile  # Import here to reduce startup errors
            with tarfile.open(temp_tar, 'r:gz') as tar:
                # For older Python versions that don't support extract_filter
                try:
                    # Modern Python with security features
                    tar.extractall(path=rootfs_dir, filter='data')
                except TypeError:
                    # Older Python without security features
                    tar.extractall(path=rootfs_dir)
            
            # Create necessary directories
            proot_bin_dir = Path(rootfs_dir) / "usr" / "local" / "bin"
            proot_bin_dir.mkdir(parents=True, exist_ok=True)
            
            # Download PRoot binary
            proot_url = f"https://raw.githubusercontent.com/foxytouxxx/freeroot/main/proot-{arch}"
            proot_bin_path = proot_bin_dir / "proot"
            
            print("Downloading PRoot binary...")
            if download_file(proot_url, proot_bin_path):
                # Make PRoot executable
                proot_bin_path.chmod(proot_bin_path.stat().st_mode | stat.S_IEXEC)
                
                # Configure DNS
                resolv_conf = Path(rootfs_dir) / "etc" / "resolv.conf"
                with open(resolv_conf, 'w') as f:
                    f.write("nameserver 1.1.1.1\nnameserver 1.0.0.1")
                
                # Installation complete
                installed_flag.touch()
                print("Installation completed successfully!")
            else:
                print("Failed to download PRoot binary. Exiting...")
                sys.exit(1)
            
            # Clean up
            os.remove(temp_tar)
        else:
            print("Failed to download Ubuntu base. Exiting...")
            sys.exit(1)
    else:
        print("FreeRoot environment already installed.")
    
    # Display success message
    print(f"\n{WHITE}{'_'*50}{RESET_COLOR}")
    print()
    print(f"           {CYAN}-----> Mission Completed ! <-----{RESET_COLOR}")
    print()
    print(f"{WHITE}{'_'*50}{RESET_COLOR}")
    
    # Launch PRoot
    proot_path = Path(rootfs_dir) / "usr" / "local" / "bin" / "proot"
    
    if not proot_path.exists():
        print("PRoot binary missing. Installation may be corrupted.")
        sys.exit(1)
    
    print("\nLaunching root environment...")
    print("Type 'exit' to return to normal environment when finished.")
    
    # Set the command
    cmd = [
        str(proot_path),
        f"--rootfs={rootfs_dir}",
        "-0",
        "-w", "/root",
        "-b", "/dev",
        "-b", "/sys",
        "-b", "/proc",
        "-b", "/etc/resolv.conf",
        "--kill-on-exit"
    ]
    
    try:
        # Execute PRoot with the specified commands
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nExiting FreeRoot environment...")
    except Exception as e:
        print(f"Error launching PRoot: {e}")

# Run main function automatically when executed
if __name__ == "__main__":
    main()