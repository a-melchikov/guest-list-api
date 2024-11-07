# Guest List API

Это приложение представляет собой API для управления гостевыми списками.

## Стек технологий

- **FastAPI**
- **SQLAlchemy**
- **Alembic**
- **PostgreSQL**
- **Pydantic**
- **Pydantic Settings**
- **Docker**
- **SQLAdmin**

## Установка и запуск через Docker

Клонируйте репозиторий:

```bash
git clone https://github.com/your-username/guest-list-api.git
cd guest-list-api
```

Создайте файл .env в корне проекта, и укажите параметры для подключения к базе данных PostgreSQL:

```env
DB_HOST=127.0.0.1
DB_PORT=5433
DB_NAME=guestbook_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_ECHO=False
ADMIN_NAME=admin
ADMIN_PASSWORD=foo
SECRET_KEY=JDoQxz9T0wt6NQ7bZ_-y0Jb0tQj_2Yp9U0EUSz2hxj6oCJtBQFgM9FoeF0ZqAx9I
```

Для запуска приложения и всех необходимых сервисов, выполните команду:

```bash
docker compose up --build
```

## Доступ к приложению

Приложение будет работать по следующему адресу:

- API: <http://127.0.0.1:8000/docs>
- Административная панель: <http://127.0.0.1:8000/admin>

Логин: admin

Пароль: foo
