from app.api import router
from fastapi import FastAPI

def create_app() -> FastAPI:
    app = FastAPI(title="Interview Flow Service", version="1.0.0")
    app.include_router(router)
    return app