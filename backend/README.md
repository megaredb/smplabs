# Backend - Local Development Guide

Welcome to the backend part of our project! This step-by-step guide will help you run the server for local development. We are not using Docker for now to keep things simple.

## Prerequisites

To work with the backend, you will need:
- **Python** (version 3.14 or higher is recommended)
- **uv** — a modern and extremely fast Python package manager. If you haven't installed it yet, check the [official uv documentation](https://github.com/astral-sh/uv) (usually installed via `curl -LsSf https://astral.sh/uv/install.sh | sh` on Linux/macOS or `pip install uv`).

---

## Step 1. Environment Variables

The application requires some basic configuration and keys to run. 
In the root directory of the whole project (one level above the `backend` folder), you will find a `.env.example` file. 
Create a copy of it and name it `.env`.

If you are in the project root, run:
```bash
cp .env.example .env
```
*(The default values inside are usually enough to start developing, but if you need specific keys, ask the team).*

---

## Step 2. Install Dependencies

Navigate to the `backend` folder in your terminal. We need to install all the required Python libraries.
Thanks to `uv`, this is very fast:

```bash
uv sync
```

This command reads the `uv.lock` file, automatically creates a virtual environment in the `.venv` folder, and installs all necessary dependencies there.

---

## Step 3. Start the Development Server

After a successful installation, you can start the server! Run the following command:

```bash
uv run fastapi dev
```

> *(This command uses FastAPI's built-in server with hot-reloading. The entry point is already configured in `pyproject.toml`)*

The server will start. Open in your browser:
- **`http://localhost:8000`** — the main entry point.
- **`http://localhost:8000/docs`** — interactive API documentation (Swagger UI), where you can test API requests directly from the browser.

---

## ⚠️ Pre-commit Requirements

Before making a commit, it is **mandatory** to check your code using `ruff` and `ty`. These tools help maintain code quality and catch errors early.

Run the following commands in the `backend` directory:
```bash
# Run Ruff to check for formatting and linting errors
uv run ruff check .

# Run Ty for type checking
uv run ty
```
Please ensure both commands pass without errors before committing your changes.

Happy coding! If you encounter any errors at any step, be sure to ask for help.
