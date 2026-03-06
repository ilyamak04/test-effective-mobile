FROM python:3.13-slim

WORKDIR /app

COPY app.py .

ENV PORT=8080

RUN useradd -r -s /sbin/nologin appuser

USER appuser

EXPOSE ${PORT}

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request, os; urllib.request.urlopen(f'http://localhost:{os.environ[\"PORT\"]}/health')" || exit 1

ENTRYPOINT ["python", "app.py"]
