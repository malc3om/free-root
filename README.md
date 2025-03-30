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

### One-line execution:

```python
!pip install requests && python -c "import requests; exec(requests.get('https://raw.githubusercontent.com/malc3om/free-root/main/freeroot.py').text)"
```

### Alternative method:

```python
# Step 1: Clone the repository
!git clone https://github.com/malc3om/free-root.git

# Step 2: Run the Python script
%cd free-root
!python freeroot.py
```

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