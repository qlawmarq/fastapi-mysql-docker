# Dockerfile for development
FROM python:3.11-slim-bookworm

WORKDIR /app

RUN pip install --upgrade pip
COPY . .
RUN pip install --no-cache-dir -r  requirements.txt

EXPOSE 8000
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]