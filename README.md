# fastapi-mysql-docker

## Elements

- FastAPI
- MySQL
- Docker

---

## Setup development environment (Docker compose)

Please install [`Docker` and `Docker compose`](https://www.docker.com/) first.

## Manual setup

After installation, run the following command to create a local Docker container.

```sh
docker-compose up
```

If Docker is running successfully, the API and DB server will be launched as shown in the following:

- API server: http://localhost:8000
- API Docs: http://localhost:8000/v1/docs
- DB server: http://localhost:3306

_Be careful, it won't work if the port is occupied by another application._

## Setup with the VS Code Dev Containers extension

The above setup can be used for development, but you can also setup dev env with using the [VS Code Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).

- Install VS code and the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).
- Run the `Dev Containers: Open Folder in Container...` command from the Command Palette or quick actions Status bar item, and select the project folder.
- Wait until the building of the application is finished, then access the application url

---

## Note

### How to enable Python code formatter (black) and linter (flake8) with VSCode extension

If you're [VS Code](https://code.visualstudio.com/) user, you can easily setup Python code formatter (black) and linter (flake8) by simply installing the extensions.

Automatic formatting settings have already been defined [`.vscode/settings.json`](./.vscode/settings.json).

Just install following:

- [Black Formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)
- [Flake8](https://marketplace.visualstudio.com/items?itemName=ms-python.flake8)

If you are using the Dev Container, this configuration is already done in [the Dev Container settings](./.devcontainer/devcontainer.json), so you can skip it.

### How to check the DB tables in container

Use following command to go inside of docker container:

```sh
docker-compose exec mysql sh
```

Then use `mysql` command to execute a query:

```sh
mysql -u root -p
mysql> USE fastapi_app;
mysql> SHOW TABLES;
mysql> SELECT * FROM user;
```

Your initial MySQL password is defined in `mysql/local.env`.

### How to add a library

Python libraries used in this app are defined in `api/requirements.txt`.

Also you may want to add libraries such as requests, in which case follow these steps:

- Add the library to requirements.txt

e.g., if you want to add `requests`:

```
requests==2.30.0
```

Then try a re-build and see.

```sh
docker-compose down
docker-compose build
docker-compose up
```

### Environment variable

Some of environment variable, like a database name and user is defined in `docker-compose.yml` or `Dockerfile`.

### DB Migrations

When creating DB docker container, docker will create predefined tables in `mysql/db` folder.
That help your team to control versions of database.

The sample table definition has already been created with the name `create_user_table.sql`.

### Save the local DB changes as a dump file

If you need to share local DB changes with other developers, you can use `mysqldump` to create a backup and share it with them.

To create a `dump.sql', run the following command:

```sh
docker-compose exec database mysqldump -u root -p fastapi_app > mysql/db/dump.sql
```

Then, to reinitialize the DB, remove the named volumes declared in the "volumes" section of the Compose file.

https://docs.docker.com/engine/reference/commandline/compose_down/

```sh
docker-compose down -v
```

Then, run `docker-compose up` to launch the development environment.  
And confirm that your DB changes are reflected.
