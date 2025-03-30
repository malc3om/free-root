# FreeRoot - PRoot for Jupyter Notebooks

## Overview

This project provides a Python-based solution to gain root access in restricted environments using PRoot, specifically designed to work in Jupyter Notebooks and other Python environments.

## Features

- Single command installation and execution
- Works in Jupyter Notebooks and other Python environments
- Automatic handling of prompts (no need for manual interaction)
- Compatible with pip-based environments
- Supports x86_64 (amd64) and aarch64 (arm64) architectures

## Usage

### One-line direct execution (RECOMMENDED FOR JUPYTER):

```python
# This method works best for Jupyter notebooks with permission restrictions
!python -c "import urllib.request; exec(urllib.request.urlopen('https://raw.githubusercontent.com/malc3om/free-root/main/direct_runner.py').read().decode())"
```

### Alternative methods:

```python
# Using requests (if available)
!pip install requests && python -c "import requests; exec(requests.get('https://raw.githubusercontent.com/malc3om/free-root/main/freeroot.py').text)"

# Clone and run (not recommended if you have permission issues)
!git clone https://github.com/malc3om/free-root.git
%cd free-root
!python freeroot.py
```

## Troubleshooting

If you encounter errors like:
- "No such file or directory" when using cd
- "python: command not found"
- Permission errors

Use the direct one-line method which creates temporary directories and handles python path issues.

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