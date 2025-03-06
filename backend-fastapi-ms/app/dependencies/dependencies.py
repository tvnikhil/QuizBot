from config import *
import instructor
from openai import OpenAI
# from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
import warnings
warnings.filterwarnings("ignore")
# from config import *
from secretKeys import *

API_KEY = api_keys[0]
import os
os.environ["GOOGLE_API_KEY"]=api_keys[0]

# def get_instructor_client():
#     return instructor.from_openai(
#         OpenAI(
#             base_url=BASE_URL,
#             api_key=API_KEY,
#         ),
#         mode=instructor.Mode.JSON,
#     )

def get_instructor_client():
    return instructor.from_openai(
        OpenAI(
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            api_key=api_keys[0],
        ),
        mode=instructor.Mode.JSON,
    )

# def get_db():
#     # embeddings = OllamaEmbeddings(model="nomic-embed-text")
#     embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url="http://34.174.202.104:11434")
#     return Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

def get_db():
    gemini_embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    return Chroma(persist_directory="/Users/thanikella_nikhil/Projects-Courses/NS/QuizBot/backend-fastapi-ms/chroma/chroma-gemini", embedding_function=gemini_embeddings)