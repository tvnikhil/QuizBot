from fastapi import APIRouter, Depends

from config import *
from dependencies.dependencies import *
from models.pydanticModels import *
from prompts.quiz_prompt_template import *

import warnings
warnings.filterwarnings("ignore")
from langchain.prompts import ChatPromptTemplate

from pydantic import BaseModel

class Query(BaseModel):
    topic: str

router = APIRouter()

@router.get("/hello")
def hello():
    return {"message": "Hello World"}