FROM python:3.9

WORKDIR /app

# Update the ENV information to the correct your production MySQL infos.
ENV APP_SECRET_STRING=P4ssW0rd
ENV DATABASE_USERNAME=appuser
ENV DATABASE_PASSWORD=P4ssW0rd
ENV DATABASE=fastapi_app
ENV DATABASE_HOST=127.0.0.1
ENV DATABASE_SOCKET=3306

RUN pip install --upgrade pip
COPY . .
RUN pip install --no-cache-dir -r  requirements.txt

ENV PORT 8080
EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]