from openai import OpenAI
from flask import Flask, request, jsonify
from flask_cors import CORS
from pydanticModels import *
import instructor
from dbInit import getDBInstance
import warnings
warnings.filterwarnings("ignore")
from prompts import *
from langchain.prompts import ChatPromptTemplate


app = Flask(__name__)
CORS(app)

# enables `response_model` in create call
client = instructor.from_openai(
    OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama",  # required, but unused
    ),
    mode=instructor.Mode.JSON,
)

db = getDBInstance()
@app.route('/open_ended', methods=['GET'])
def generateOpenEndedQuestions():
    try:
        results = db.similarity_search_with_score("Explain Kerberos", k=7)
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        sources = [doc.metadata.get("id", None)[:-2] for doc, _score in results]
        
        promptTemplate = ChatPromptTemplate.from_template(OPEN_ENDED_QUESTION_PROMPT)
        question="Explain Kerberos and why is it used?"
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
        return jsonify(final_response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        

@app.route('/generate_quiz', methods=['GET'])
def generateQuiz():
    try:
        question="Explain Kerberos"
        results = db.similarity_search_with_score(question, k=7)
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        sources = [doc.metadata.get("id", None)[:-2] for doc, _score in results]
        
        promptTemplate = ChatPromptTemplate.from_template(QUIZ_TOPIC_QUESTION_PROMPT)
        prompt = promptTemplate.format(context=context_text)

        response = client.chat.completions.create(
            model="llama3.2:latest",
            temperature=0.2,
            messages=[
                { "role": "system", "content": QUIZ_TOPIC_SYS_INSTR,},
                { "role": "user", "content": prompt,}
            ],
            response_model=MCQArr,
        )

        final_response = {
            "quiz": response.model_dump(),
            "sources": sources
        }

        return jsonify(final_response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)