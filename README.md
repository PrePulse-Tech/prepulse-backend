<p align="center">
  <img src="assets/P_w_s.jpg" alt="PrePulse Logo" width="220"/>
</p>

# PrePulse Backend (Inception Phase)

This is the backend architecture for **PrePulse**, developed as a major project in collaboration with Preface.

**Status:** The project is in the initial setup phase. Architecture and core functionalities are currently being defined.

## Technologies
* **Language:** Python

## Purpose
To build a robust backend system focused on system monitoring, log analysis, and integrated IT security measures.

## Project Team & Collaboration

This project is developed as a major project in collaboration with **Preface**.

**Team Members (Students):**
*   **Najib Nawabi** (GitHub: [@CodeByNajib](https://github.com/CodeByNajib))
    *   Email (Student): `nana0001@stud.ek.dk`
    *   Email (Personal): `jivonajib1990@gmail.com`
*   **Marcus Lieber Heilstrup** (GitHub: [@MarcusLieberH](https://github.com/MarcusLieberH))
    *   Email (Student): `mahe0009@stud.ek.dk`
    *   Email (Personal): `marcus.heilstrup98@gmail.com`

**Product Owner (Preface):**
*   **Christian Rasmussen**
    *   Title: Partner / IT Chef
    *   Email: `kontakt@preface.dk`

## Getting Started
This project is currently under active development. Further instructions for setup and deployment will be added as the project progresses.

## Configuration & Secrets

Configuration is read from environment variables (see [`app/config.py`](app/config.py)).
**Never commit real keys** – CI runs [gitleaks](https://github.com/gitleaks/gitleaks) on every pull request and fails if a secret is found.

| Variable | Purpose |
|---|---|
| `ANTHROPIC_API_KEY` | Claude API key for the AI agent |
| `DATABASE_URL` | PostgreSQL connection string |
| `INGEST_API_KEY` | Key log sources use when sending logs |

### Locally
1. Copy the example file: `cp .env.example .env`
2. Fill in your own values in `.env`. The file is git-ignored and stays on your machine.
3. The app loads `.env` automatically on startup.

### In GitHub
If a workflow needs a secret, add it under
**Settings → Secrets and variables → Actions → New repository secret**, using the same name as in `.env.example`.
Use it in a workflow as `${{ secrets.ANTHROPIC_API_KEY }}`. GitHub hides the value in logs.

If a key is ever committed by mistake, **rotate it immediately** (create a new key and revoke the old one). Removing it from the code is not enough, because it stays in the git history.
