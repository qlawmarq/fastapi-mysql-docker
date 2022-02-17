# fastapi-mysql-docker

- FastAPI
- MySQL
- Docker

## Setup

Please install `Docker` and `Docker compose` first.

The following versions have been tested.

```bash
docker --version
  Docker version 20.10.8, build 3967b7d
docker-compose -v  
  docker-compose version 1.29.2, build 5becea4c
```

After installation, run the following command to create a local Docker container.

```bash
docker-compose build
docker-compose up -d
```

If you want to check the log while Docker container is running, then try to use following command:

```bash
docker-compose up
```

API server will start on http://localhost:8000.
And DB server will start on http://localhost:3306.
Also, you can check API document on http://localhost:8000/redoc.

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

- https://github.com/masaiborg/expo-react-native-base
- https://github.com/masaiborg/nuxt3-tailwind-sample-auth-app

## Note

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
