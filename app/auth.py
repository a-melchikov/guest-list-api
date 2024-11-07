from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from fastapi.templating import Jinja2Templates
from app.models import User
from app.database import async_session_maker

templates = Jinja2Templates(directory="templates")


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        user = await self.validate_user_credentials(request, username, password)
        if user:
            request.session.update({"user": user.id})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        user_id = request.session.get("user")
        if not user_id:
            return False
        return True

    async def validate_user_credentials(
        self, request: Request, username: str, password: str
    ):
        async with async_session_maker() as session:
            user = await User.get_by_username(session, username)
            if user and user.verify_password(password):
                return user
        return None
