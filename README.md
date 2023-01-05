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

- https://github.com/cymagix/nuxt3-tailwind-sample-auth-app
- https://github.com/cymagix/expo-react-native-base
- https://github.com/cymagix/next-web-app-template

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

### API documentation

http://localhost:8000/redoc
