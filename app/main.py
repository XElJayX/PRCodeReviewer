from fastapi import FastAPI
from app.api.webhook import router
from dotenv import load_dotenv

load_dotenv()

app=FastAPI()

app.include_router(router)

