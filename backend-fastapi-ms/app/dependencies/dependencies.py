from config import *
import instructor
from openai import OpenAI

from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
import warnings
warnings.filterwarnings("ignore")
from config import *

def get_instructor_client():
    return instructor.from_openai(
        OpenAI(
            base_url=BASE_URL,
            api_key=API_KEY,
        ),
        mode=instructor.Mode.JSON,
    )

def get_db():
    embeddings = OllamaEmbeddings(model="nomic-embed-text", base_url=BASE_URL, api_key=API_KEY)
    return Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)