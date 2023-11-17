# Dockerfile for development
FROM python:3.12-slim-bookworm

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r  requirements.txt

EXPOSE 8000
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]