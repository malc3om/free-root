#!/usr/bin/env python3
"""
Special version that builds a minimal rootfs with busybox.
This works around symlink issues and missing shell problems.
- Downloads and extracts a minimal rootfs
- Sets up busybox for essential commands
- Works in Python 3.6 environments
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

# Suppress warnings
warnings.filterwarnings("ignore")

# ANSI Colors
CYAN = '\033[0;36m'
WHITE = '\033[0;37m'
RESET_COLOR = '\033[0m'

def download_file(url, target_path):
    """Download a file with retry mechanism using stdlib only"""
    max_retries = 5
    
    for i in range(max_retries):
        try:
            print(f"Downloading from {url}...")
            with urllib.request.urlopen(url) as response, open(target_path, 'wb') as out_file:
                chunk_size = 8192
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0
                
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    downloaded += len(chunk)
                    out_file.write(chunk)
                    
                    # Show progress for large files
                    if total_size > 1000000:
                        percent = int(downloaded * 100 / total_size)
                        sys.stdout.write(f"\rDownload progress: {percent}% ({downloaded} / {total_size} bytes)")
                        sys.stdout.flush()
                
                if total_size > 1000000:
                    print()  # Newline after progress
            
            print(f"Download completed: {target_path}")
            return True
        except Exception as e:
            print(f"Download attempt {i+1}/{max_retries} failed: {e}")
            if i == max_retries - 1:
                return False

def get_architecture():
    """Get system architecture and corresponding alt name"""
    arch = platform.machine()
    
    if arch == "x86_64":
        arch_alt = "amd64"
        busybox_url = "https://busybox.net/downloads/binaries/1.35.0-x86_64-linux-musl/busybox"
    elif arch == "aarch64" or arch == "arm64":
        arch_alt = "arm64"
        busybox_url = "https://busybox.net/downloads/binaries/1.35.0-aarch64-linux-musl/busybox"
    else:
        print(f"Unsupported CPU architecture: {arch}")
        sys.exit(1)
    
    return arch, arch_alt, busybox_url

def create_minimal_rootfs(rootfs_dir):
    """Create a minimal rootfs with busybox"""
    print("Creating minimal rootfs with busybox...")
    
    # Create basic directory structure
    for dir_path in [
        "bin", "dev", "etc", "home", "lib", "proc", "root", 
        "sys", "tmp", "usr/bin", "usr/lib", "usr/local/bin", "var"
    ]:
        os.makedirs(os.path.join(rootfs_dir, dir_path), exist_ok=True)
    
    # Download busybox
    _, _, busybox_url = get_architecture()
    busybox_path = os.path.join(rootfs_dir, "bin", "busybox")
    
    if download_file(busybox_url, busybox_path):
        # Make busybox executable
        os.chmod(busybox_path, 0o755)
        
        # Create basic shell symlinks
        essential_cmds = [
            "sh", "ls", "cat", "echo", "cp", "mv", "rm", "mkdir", 
            "chmod", "chown", "ps", "mount", "umount", "kill", 
            "grep", "find", "tar", "gzip", "gunzip", "wget"
        ]
        
        # Create symlinks in bin
        for cmd in essential_cmds:
            link_path = os.path.join(rootfs_dir, "bin", cmd)
            try:
                os.symlink("busybox", link_path)
            except FileExistsError:
                pass
        
        # Create resolv.conf
        with open(os.path.join(rootfs_dir, "etc", "resolv.conf"), 'w') as f:
            f.write("nameserver 1.1.1.1\nnameserver 1.0.0.1\n")
        
        # Create a basic /etc/passwd file
        with open(os.path.join(rootfs_dir, "etc", "passwd"), 'w') as f:
            f.write("root:x:0:0:root:/root:/bin/sh\n")
        
        print("Minimal rootfs created successfully!")
        return True
    else:
        print("Failed to download busybox.")
        return False

def main():
    # Create a fresh temporary directory
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
    print(f"{CYAN}                Minimal BusyBox Rootfs Edition{RESET_COLOR}")
    print(f"{WHITE}{'='*70}{RESET_COLOR}")
    
    # Check architecture
    arch, arch_alt, _ = get_architecture()
    print(f"Detected architecture: {arch} ({arch_alt})")
    print(f"Working directory: {work_dir}")
    
    rootfs_dir = os.getcwd()
    installed_flag = Path(rootfs_dir) / ".installed"
    
    if not installed_flag.exists():
        print("\nBuilding minimal rootfs...")
        
        if create_minimal_rootfs(rootfs_dir):
            # Download PRoot binary
            proot_bin_dir = Path(rootfs_dir) / "usr" / "local" / "bin"
            proot_bin_dir.mkdir(parents=True, exist_ok=True)
            
            proot_url = f"https://raw.githubusercontent.com/foxytouxxx/freeroot/main/proot-{arch}"
            proot_bin_path = proot_bin_dir / "proot"
            
            print("Downloading PRoot binary...")
            if download_file(proot_url, proot_bin_path):
                # Make PRoot executable
                proot_bin_path.chmod(proot_bin_path.stat().st_mode | stat.S_IEXEC)
                
                # Installation complete
                installed_flag.touch()
                print("Installation completed successfully!")
            else:
                print("Failed to download PRoot binary. Exiting...")
                sys.exit(1)
        else:
            print("Failed to build minimal rootfs. Exiting...")
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
        "--kill-on-exit",
        "/bin/sh"
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