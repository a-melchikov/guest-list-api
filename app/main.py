import asyncio
import uvicorn
import sqladmin

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from app.routers import router
from app.database import engine
from .admin import GuestListAdmin, TableAdmin
from .auth import AdminAuth
from .create_admin_user import create_admin_user
from .config import settings

templates = Jinja2Templates(directory="templates")

main_app = FastAPI(
    default_response_class=ORJSONResponse,
)

admin = sqladmin.Admin(
    app=main_app,
    engine=engine,
    authentication_backend=AdminAuth(secret_key=settings.SECRET_KEY),
)

admin.add_view(GuestListAdmin)
admin.add_view(TableAdmin)

main_app.include_router(router=router, prefix="/api")


@main_app.get("/login", response_class=HTMLResponse, include_in_schema=False)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@main_app.post("/login", include_in_schema=False)
async def login_post(request: Request):
    auth_backend = AdminAuth(secret_key=settings.SECRET_KEY)
    is_authenticated = await auth_backend.login(request)
    if is_authenticated:
        return RedirectResponse(url="/admin/")
    return templates.TemplateResponse(
        "login.html", {"request": request, "error": "Invalid credentials"}
    )


async def start_application():
    await create_admin_user()
    uvicorn.run("app.main:main_app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    asyncio.run(start_application())
