# Dockerfile for production
# NOTE: some of the ENV variables are just for example purposes. Update them to your own production values.
FROM python:3.12-slim-bookworm

WORKDIR /app

# Update the ENV information to the correct your production MySQL infos.
ENV APP_SECRET_STRING=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
ENV DATABASE_USERNAME=appuser
ENV DATABASE_PASSWORD=i4bP188nFsI1
ENV DATABASE=fastapi_app
ENV DATABASE_HOST=127.0.0.1
ENV DATABASE_SOCKET=3306

COPY . .
RUN pip install --no-cache-dir -r  requirements.txt

ENV PORT 8080
EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]