# Dockerfile for production
# NOTE: some of the ENV variables are just for example purposes. Update them to your own production values.
FROM python:3.12-slim-bookworm

WORKDIR /app

# Update the ENV information to the correct your production MySQL infos.
ENV APP_SECRET_STRING=AppS3rcr3t
ENV DATABASE_USERNAME=appuser
ENV DATABASE_PASSWORD=P4ssw0rd
ENV DATABASE=fastapi_app
ENV DATABASE_HOST=127.0.0.1
ENV DATABASE_PORT=3306

COPY . .
RUN pip install --no-cache-dir -r  requirements.txt

ENV PORT 8080
EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]