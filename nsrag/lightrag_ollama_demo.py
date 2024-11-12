import os
import logging
from lightrag import LightRAG, QueryParam
from lightrag.llm import ollama_model_complete, ollama_embedding
from lightrag.utils import EmbeddingFunc
import asyncio
import json

WORKING_DIR = "/Users/thanikella_nikhil/Projects-Courses/NS/QuizBot/data/emdNS"

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)

rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=ollama_model_complete,
    llm_model_name="llama3.2:1B",
    llm_model_max_async=4,
    llm_model_max_token_size=32768,
    llm_model_kwargs={"host": "http://localhost:11434", "options": {"num_ctx": 32768}},
    embedding_func=EmbeddingFunc(
        embedding_dim=768,
        max_token_size=8192,
        func=lambda texts: ollama_embedding(
            texts, embed_model="nomic-embed-text", host="http://localhost:11434"
        ),
    ),
)

file_path = '/Users/thanikella_nikhil/Projects-Courses/NS/QuizBot/data/out.txt'
with open(file_path, 'r') as f:
    rag.insert(f.read())

response = rag.query("Generate 4 multiple-choice quiz questions.Each question should include: the question text, four options and correct answer.", param=QueryParam(mode="naive"))
print(response)

# prompt1 = '''Your answer must be in json format without any additional text other than the answer (in json). It should be well structured so that I can create an api for these responses easily. Based on the information from the documents in the knowledge base, generate 5 multiple-choice quiz questions.Each question should include: the question text, four options and correct answer. Respond only with valid JSON. Do not write an introduction or summary.'''
# print(rag.query(prompt1, param=QueryParam(mode="naive")))

# prompt2 = '''Your answer must be in json format without any additional text other than the answer (in json). It should be well structured so that I can create an api for these responses easily. Based on the information from the documents in the knowledge base, Generate 5 True-False quiz questions.Each question should include: the question text and correct answer. Respond only with valid JSON. Do not write an introduction or summary.'''
# print(rag.query(prompt2, param=QueryParam(mode="naive")))

# print(rag.query("Generate 5 MCQ questions on the topic: public key encryption.Each question should include: the question text and correct answer.", param=QueryParam(mode="naive")))

# print(rag.query("Generate 5 open ended questions. Each question should include: the question text and a possible correct answer.", param=QueryParam(mode="naive")))