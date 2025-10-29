# Contributing to KMS_lib

We welcome improvements to documentation, code, or datasets.

## Development setup
1. Clone the repository and create a virtual environment (Python 3.11 or Conda).
2. Install dependencies from `requirements.txt` or `environment.yml`.
3. Run `pytest -q` to confirm all tests pass.
4. Format code using `black .` and lint with `ruff check .` (optional if installed).

## Code style
- Follow PEP 8.
- Keep functions short and documented.
- Write meaningful commit messages: `feat: add semantic retrieval`, `fix: handle empty query`.

## Testing
Add tests in `tests/` for any new module. Use synthetic data only.
