# Patrick Star

A playful automation bot that generates random, humorous customer queries and submits them to a Shopify chat widget. Designed for testing, fun, and creative automation, Patrick Star simulates unique customer interactions and notifies you via Discord and ntfy.

## Description

Patrick Star is a Python-based automation tool that creates random customer personas and queries, then submits them to a Shopify chat widget using Selenium. It ensures each query, first name, and last name is unique (using diskcache), and notifies you of each submission via Discord and ntfy. The project is modular, robust, and designed for easy testing and extension.

## Getting Started

### Dependencies

- Python 3.10+
- macOS (tested on Darwin 24.5.0)
- [uv](https://github.com/astral-sh/uv) for dependency management (recommended)
- Google Chrome (for Selenium)
- ChromeDriver (matching your Chrome version)
- The following Python packages (see `requirements.txt`):
  - diskcache
  - requests
  - discord_webhook
  - python-dotenv
  - selenium
  - pytest, pytest-mock (for testing)
  - ruff (for linting)

### Installing

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd patrick-star
   ```
2. **Set up a virtual environment (recommended):**
   ```sh
   python -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies:**
   ```sh
   uv pip install -r requirements.txt
   # or, if not using uv:
   pip install -r requirements.txt
   ```
4. **Set up environment variables:**
   Create a `.env` file in the project root with the following keys:
   ```env
   URL=<your_shopify_store_url>
   NTFY_URL=<your_ntfy_url>
   WEBHOOK=<your_discord_webhook_url>
   ```
5. **Ensure Chrome and ChromeDriver are installed and compatible.**

### Executing program

To run the main automation script:

```sh
python main.py
```

To run tests:

```sh
pytest
```

To lint the codebase:

```sh
ruff check .
```

## Help

- If you encounter issues with ChromeDriver, ensure it matches your installed Chrome version.
- For environment variable issues, check your `.env` file and ensure all required keys are present.
- To clear the cache for testing, uncomment the `DiskCache.clear_cache()` line in `main.py`.

To see available pytest options:

```sh
pytest --help
```

---

Inspired by the spirit of fun automation and the wisdom of Uncle Tito.
