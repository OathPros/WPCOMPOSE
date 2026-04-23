from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes.web import router as web_router

app = FastAPI(title="York AI Web Composer", version="0.1.0")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(web_router)
