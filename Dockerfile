FROM python:3.12.2-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN python -m venv /install \
    && /install/bin/pip install --upgrade pip \
    && /install/bin/pip install --no-cache-dir -r requirements.txt

COPY . .

FROM python:3.12.2-slim

RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

COPY --from=builder /install /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY --from=builder /app /app

EXPOSE 8000

USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]