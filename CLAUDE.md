# PrePulse Backend

PrePulse is a bachelor project (datamatiker) by Marcus and Najib for the company **Preface**.
It automatically analyses server logs, detects operational failures and security threats
(e.g. brute force, port scanning, HTTP 500 errors) and uses a constrained AI agent
(Claude API) to explain incidents and suggest fixes.

Key principles:
- Personal data is **masked before any AI call**.
- Actions require **human approval with MFA** - the AI never acts on its own.

This repo is the backend: `PrePulse-Tech/prepulse-backend`.

## Stack
- Python 3.13 + FastAPI (entrypoint: `app/main.py`)
- pytest + httpx (TestClient) for tests, ruff for lint/format
- PostgreSQL planned later
- Dependencies: `requirements.txt` (runtime), `requirements-dev.txt` (dev/CI)
- Tool config in `pyproject.toml`

## Commands (Git Bash on Windows, venv in `.venv`)
```bash
source .venv/Scripts/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload   # run locally -> http://127.0.0.1:8000/health
ruff check . && ruff format --check .
pytest
```

## Configuration
- Settings live in `app/config.py` (pydantic-settings), read from env vars and a local `.env`.
- Secrets are typed as `SecretStr`; `.env.example` lists the expected variables.

## CI
`.github/workflows/ci.yml` runs on every pull request and on push to `main`:
Security (gitleaks scan of full git history) -> Build (install + import check)
-> Lint (ruff) -> Test (pytest).

## Workflow rules
- Work is tracked on a GitHub Projects board with issues.
- Use feature branches named `feature/<issue-no>-<short-name>` and pull requests;
  reference the issue in the PR (`Closes #<no>`).
- **Never commit or push directly to `main`.**
- Ask before pushing or creating pull requests.
- Keep things simple - this is a foundation, not finished features.
- Never commit secrets; `.env` is git-ignored.
