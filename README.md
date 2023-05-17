# fastapi-mysql-docker

- FastAPI
- MySQL
- Docker

## Setup

Please install `Docker` and `Docker compose` first.

https://www.docker.com/

After installation, run the following command to create a local Docker container.

```bash
docker-compose build
docker-compose up -d
```

If you want to check the log while Docker container is running, then try to use following command:

```bash
docker-compose up
```

If Docker is running successfully, the API and DB server will be launched as shown in the following:

- API server: http://localhost:8000
- DB server: http://localhost:3306

_Be careful, it won't work if the port is occupied by another application._

If you want to check docker is actually working, then you can check it with following command:

```bash
docker ps
```

If you want to go inside of docker container, then try to use following command:

```bash
docker-compose exec mysql bash
docker-compose exec api bash
```

For shutdown of the docker instance, please use following command:

```bash
docker-compose down
```

## Need a front-end app?

If you need a front-end app for this server-side & DB server.

You can clone the front-end template from:

- https://github.com/qlawmarq/nuxt3-tailwind-auth-app
- https://github.com/qlawmarq/expo-react-native-base
- https://github.com/qlawmarq/next-web-app-template

## Note

### How to check the DB tables in container

You can check the DB data by actually executing a query using the following command:

```bash
docker-compose exec mysql bash
mysql -u root -p
mysql> USE fastapi_app;
mysql> SHOW TABLES;
```

### How to add a library

You may want to add libraries such as requests, in which case follow these steps:

- Add the library to requirements.txt

e.g., if you want to add `requests`:

```
requests==2.30.0
```

Then try a re-build and see.

```
docker-compose build
docker-compose up
```

### Python library packages

Some of the Python packages used in this app are defined in `api/requirements.txt`.
Also you can add other packages there.

### Environment variable

Some of environment variable, like a database name and user is defined in `docker-compose.yml`.
You can customize it as you like.

If you will use docker, then please define your environment variable to `docker-compose.yml`.
However, you will NOT use docker, then please create `.env` file for your API server.

### DB Migrations

When creating DB docker container, docker will create predefined tables in `mysql/db` folder.
That help your team to control versions of database.

The sample table definition has already been created with the name `create_user_table.sql`.

### Save the local DB changes as a dump file

```bash
docker-compose exec database mysqldump -u root -p fastapi_app > mysql/db/dump.sql
```

### API documentation

http://localhost:8000/redoc
