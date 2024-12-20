from fastapi import APIRouter, Depends

from config import *
from dependencies.dependencies import *
from models.pydanticModels import *
from prompts.open_ended import *
from prompts.quiz import *

import warnings
warnings.filterwarnings("ignore")
from langchain.prompts import ChatPromptTemplate

router = APIRouter()

@router.get("/open_ended")
def generateOpenEndedQuestions(
    db=Depends(get_db),
    client=Depends(get_instructor_client),
):
    try:
        results = db.similarity_search_with_score("explain Kerberos", k=7)
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        sources = [doc.metadata.get("id", None)[:-2] for doc, _score in results]
        
        promptTemplate = ChatPromptTemplate.from_template(OPEN_ENDED_QUESTION_PROMPT)
        question="What is Kerberos?"
        prompt = promptTemplate.format(context=context_text, question=question)
        
        response = client.chat.completions.create(
            model="llama3.2:latest",
            temperature=0.1,
            messages=[
                { "role": "system", "content": OPEN_ENDED_SYS_INSTR,},
                { "role": "user", "content": prompt,}
            ],
            response_model=Answer,
        )

        final_response = {
            "answer": response.ans,
            "sources": sources
        }
        return {"finalResponse": final_response}
    except Exception as e:
        return {"Error": str(e)}