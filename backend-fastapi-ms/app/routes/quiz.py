from fastapi import APIRouter, Depends

from config import *
from dependencies.dependencies import *
from models.pydanticModels import *
from prompts.quiz_prompt_template import *

import warnings
warnings.filterwarnings("ignore")
from langchain.prompts import ChatPromptTemplate

router = APIRouter()

@router.post("/generate_quiz")
def generateQuiz(
    query: Query,
    db=Depends(get_db),
    client=Depends(get_instructor_client),
):
    try:
        question=f"Explain {query.text}"
        results = db.similarity_search_with_score(question, k=10)
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        sources = [doc.metadata.get("id", None)[:-2] for doc, _score in results]
        
        promptTemplate = ChatPromptTemplate.from_template(QUIZ_TOPIC_QUESTION_PROMPT)
        prompt = promptTemplate.format(context=context_text)

        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            temperature=0.1,
            messages=[
                { "role": "system", "content": QUIZ_TOPIC_SYS_INSTR,},
                { "role": "user", "content": prompt,}
            ],
            response_model=MCQArr,
        )

        # print(response)

        final_response = {
            "quiz": response.model_dump(),
            "sources": sources
        }

        return {"finalResponse": final_response}
    except Exception as e:
        return {"Error": str(e)}