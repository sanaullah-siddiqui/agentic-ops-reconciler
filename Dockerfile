FROM python:3.12-slim AS builder

WORKDIR /build
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim AS runtime

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/install/bin:$PATH"

RUN useradd --create-home --uid 10001 appuser
COPY --from=builder /install /install
COPY app/ ./app/
COPY data/ ./data/

RUN mkdir -p /app/output && chown -R appuser:appuser /app
USER appuser

CMD ["python", "-m", "app.main"]