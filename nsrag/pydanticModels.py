from pydantic import BaseModel
from typing import List

class MCQ(BaseModel):
    question_text: str
    options: list[str]
    correct_answer: str

class MCQArr(BaseModel):
    mcqs: list[MCQ]

class Answer(BaseModel):
    ans: str