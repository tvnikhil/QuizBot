from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import *
from routes import open_ended, quiz

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(open_ended.router)
app.include_router(quiz.router)