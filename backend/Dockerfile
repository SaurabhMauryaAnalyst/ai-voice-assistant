# ─── STAGE 1: INSTALL DEPENDENCIES ───────────────────────
FROM python:3.12-slim AS deps

WORKDIR /app

# Install system build tools needed by some pip packages (gcc for C extensions)
# --no-install-recommends keeps it minimal
# Clean apt cache immediately to reduce layer size
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (cache optimization — same as npm)
COPY requirements.txt .

# Install all Python packages
# --no-cache-dir: don't cache pip downloads (saves ~50MB)
RUN pip install --no-cache-dir -r requirements.txt


# ─── STAGE 2: RUNTIME ────────────────────────────────────
# Fresh slim Python image — no build tools
FROM python:3.12-slim

WORKDIR /app

# Copy installed packages from Stage 1 (not the build tools, just the packages)
COPY --from=deps /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=deps /usr/local/bin /usr/local/bin

# Copy application source code
COPY app/ ./app/

# Security: run as non-root user
# If the app is compromised, attacker has limited permissions
RUN useradd -m -u 1001 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# 4 workers handles ~80 concurrent WebSocket connections
CMD ["uvicorn", "app.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "4"]

# Final image size: ~380MB  (vs ~900MB without multi-stage)