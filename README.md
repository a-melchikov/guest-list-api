Libraries:
alembic
sqlalchemy
fastapi
postgresql
pydantic
pydantic-settings

env example:

```env
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=guestbook_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_ECHO=False
```

docker:

```bash
docker compose up --build
```

migration create:

```bash
alembic -c app/alembic.ini revision --autogenerate -m "Create ..."
```

migration update:

```bash
alembic -c app/alembic.ini upgrade head
```
