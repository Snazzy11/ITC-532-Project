# ---------- Stage 1: build ----------
FROM python:3.14.8-slim AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

# A virtual environment at a world-readable path, owned by root.
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# ---------- Stage 2: runtime ----------
FROM python:3.14.8-slim AS runtime

# Dependencies are put into opt/venv
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_VERSION=2.0.0

# UID 1000, pip install into /root/.local fails because the user does not have permission
# access root user files.
RUN useradd --create-home --uid 1000 appuser

# /opt/venv arrives as root:root mode 0755, readable and traversable
# by every user in the image, including appuser.
COPY --from=builder /opt/venv /opt/venv

WORKDIR /app
COPY --chown=appuser:appuser app.py .

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8000/health').status==200 else 1)"

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
