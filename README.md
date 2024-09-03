## Technologies

- [Python 3.12.5](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [Docker](https://www.docker.com/)

## Interactive API Documentation

![screencapture-localhost-8000-docs-2024-09-03-14_43_18](https://github.com/user-attachments/assets/2a65fc93-e7e8-4854-9753-3c4ebbdf7e8e)

## How To Run

### Pre-requisites

- Docker installed
- Any IDE that supports Python (VSCode, or PyCharm recommended)

### Step-by-step Guide

1. Clone the repository

```bash
git clone https://github.com/mochacr0/fastapi-assignment.git
```

2. Change directory to the project folder

```bash
cd your-project-folder
```

3. Build and run the Docker containers using Docker Composer

```bash
docker compose up --build
```

4. Once the containers are up and running, you can access the API documentation at http://localhost:8000/docs


5. For demonstration purposes, you can use the following credentials to login:

   |          |   User   |  Admin   | 
   | :-------:|:--------:|:--------:| 
   | Username |  `user`  | `admin`  |
   | Password | `string` | `string` |

6. To stop the containers, enter the terminal and press `Ctrl + C` to stop the containers. If you want to remove the
   containers, run the following command to stop and remove the containers:

```bash
docker compose down
```

 


