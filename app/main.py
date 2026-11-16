"""PrePulse backend - FastAPI entrypoint."""

from fastapi import FastAPI

app = FastAPI(title="PrePulse API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness check used by CI, load balancers and monitoring."""
    return {"status": "ok"}
