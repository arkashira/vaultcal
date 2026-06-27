<h3 align="center">🧮 vaultcal</h3>

<div align="center">
  <a href="https://github.com/your-org/vaultcal/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License: MIT"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10%2B-blue.svg" alt="Python 3.10+"></a>
  <a href="https://github.com/your-org/vaultcal/actions"><img src="https://img.shields.io/github/actions/workflow/status/your-org/vaultcal/ci.yml?branch=main&label=build" alt="Build Status"></a>
  <a href="https://github.com/your-org/vaultcal/stargazers"><img src="https://img.shields.io/github/stars/your-org/vaultcal?style=flat" alt="Stars"></a>
</div>

---  

# 🚀 vaultcal  
**Power developers with simple, reliable arithmetic functions.** A minimal Python package that provides clean `add`, `subtract`, `multiply`, and `divide` utilities out‑of‑the‑box.

## Why vaultcal?

- **Zero‑dependency** – No external libraries; pure‑Python implementation keeps your environment lightweight.  
- **Crystal‑clear API** – Each function is type‑annotated and documented with examples.  
- **Predictable behavior** – Consistent error handling (e.g., `ZeroDivisionError` for divide).  
- **Ready for testing** – Comes with a tiny test suite that runs with the standard library.  
- **Ideal starter kit** – Perfect for learning packaging, CI pipelines, or building a CLI wrapper.  
- **Built for automation** – Small footprint makes it easy to embed in CI/CD or sandbox environments.  

## Feature Overview

| Feature | Description |
|---------|-------------|
| `add(a, b)` | Returns the sum of `a` and `b`. |
| `subtract(a, b)` | Returns the difference `a - b`. |
| `multiply(a, b)` | Returns the product of `a` and `b`. |
| `divide(a, b)` | Returns the quotient `a / b`; raises `ZeroDivisionError` on `b == 0`. |
| Type hints | Full static‑typing support for IDEs and linters. |
| Docs & examples | Inline docstrings with usage snippets. |

## Tech Stack

- **Python** – Core language for the library.

## Project Structure

```
vaultcal/
├─ business/      # (optional) business‑logic placeholders
├─ docs/          # documentation assets (README, PRD, etc.)
├─ src/           # source code (the `vaultcal` package)
│   └─ vaultcal/  # module with arithmetic functions
├─ tests/         # unit tests using unittest
├─ pyproject.toml # build system configuration
├─ setup.py       # legacy installer script
└─ README.md      # this file
```

## Getting Started

```bash
# 1️⃣ Clone the repository
git clone https://github.com/your-org/vaultcal.git
cd vaultcal

# 2️⃣ Install the package in editable mode
pip install -e .

# 3️⃣ Verify the installation
python -c "import vaultcal; print(vaultcal.add(2, 3))"
# => 5
```

### Running the test suite

```bash
# Uses the built‑in unittest framework (no extra deps)
python -m unittest discover -s tests
```

## Deploy

The package is ready to be published to PyPI.

```bash
# Build distribution archives
python -m build

# Upload to PyPI (requires a PyPI token)
python -m twine upload dist/*
```

## Status

🟢 **Active –** latest commit `83850bc` (feat: real, sandbox‑tested implementation) adds the final arithmetic implementations and passes all tests.

## Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

Distributed under the **MIT License**. See `LICENSE` for more information.