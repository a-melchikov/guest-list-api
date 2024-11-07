import uvicorn
import sqladmin

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.routers import router
from app.database import engine
from .admin import GuestListAdmin, TableAdmin

main_app = FastAPI(
    default_response_class=ORJSONResponse,
)

admin = sqladmin.Admin(main_app, engine)
admin.add_view(GuestListAdmin)
admin.add_view(TableAdmin)

main_app.include_router(router=router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run("app.main:main_app", reload=True)
