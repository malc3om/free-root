# FreeRoot - PRoot for Jupyter Notebooks

## Overview

This project provides a Python-based solution to gain root access in restricted environments using PRoot, specifically designed to work in Jupyter Notebooks and other Python environments.

## Features

- Single command installation and execution
- Works in Jupyter Notebooks and other Python environments
- Automatic handling of prompts (no need for manual interaction)
- Compatible with highly restricted environments
- Supports x86_64 (amd64) and aarch64 (arm64) architectures

## Usage

### 💪 Standalone One-Line (BEST FOR PYTHON 3.6+):

```python
# Works with Python 3.6+ in the most restricted environments
!python3 -c "import urllib.request; exec(urllib.request.urlopen('https://raw.githubusercontent.com/malc3om/free-root/main/standalone.py').read().decode())"
```

This method:
- Uses **only** standard library modules
- Cleans up existing directories to prevent nesting issues
- Handles tarfile security warnings
- Runs in temporary directories for permission safety

### Alternative methods:

```python
# Using standard library (if you need a simpler version)
!python3 -c "import urllib.request; exec(urllib.request.urlopen('https://raw.githubusercontent.com/malc3om/free-root/main/stdlib_runner.py').read().decode())"

# Using requests (if available and you have install permissions)
!pip install requests && python3 -c "import requests; exec(requests.get('https://raw.githubusercontent.com/malc3om/free-root/main/freeroot.py').text)"
```

## Troubleshooting

If you encounter errors like:
- "ModuleNotFoundError: No module named 'requests'"
- "Permission denied" errors with pip
- Path nesting issues
- Tarfile security warnings

Use the **Standalone One-Line** method above which addresses all these issues.

## After Getting Root

Once the root environment is launched, you can:
- Run `whoami` to confirm you have root access
- Install packages with `apt update && apt install <package>`
- Access system files and directories normally protected
- Type `exit` when finished to return to normal environment

## Supported Architectures

- x86_64 (amd64)
- aarch64 (arm64)

## License

This project is released under the MIT License.

## Credits

Based on the [freeroot](https://github.com/foxytouxxx/freeroot) project by foxytouxxx.
Original PRoot code by [dxomg](https://github.com/dxomg)

---

**Note:** This script is intended for educational and experimental purposes. Use it responsibly and at your own risk.