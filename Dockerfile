FROM python:3.12-slim
WORKDIR /app
RUN useradd --create-home --uid 10001 appuser
COPY pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir .
USER appuser
EXPOSE 8000
CMD ["uvicorn", "profile_sync.main:app", "--host", "0.0.0.0", "--port", "8000"]
