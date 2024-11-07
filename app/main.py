import uvicorn

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.routers import router


main_app = FastAPI(
    default_response_class=ORJSONResponse,
)

main_app.include_router(router=router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("app.main:main_app", reload=True)
