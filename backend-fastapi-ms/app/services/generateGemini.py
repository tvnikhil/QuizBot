import warnings
warnings.filterwarnings("ignore")
from langchain_community.vectorstores import Chroma
from openai import OpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
warnings.filterwarnings("ignore")
from secretKeys import *
os.environ["GOOGLE_API_KEY"] = api_keys[0]

def get_db():
    gemini_embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    return Chroma(persist_directory="/Users/thanikella_nikhil/Projects-Courses/NS/QuizBot/backend-fastapi-ms/chroma/chroma-gemini", embedding_function=gemini_embeddings)

db = get_db()
# query = "What is symmetric encryption?"
query = "how are public keys distributed?"
results = db.similarity_search_with_score(query, k=10)
context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
sources = [doc.metadata.get("id", None) for doc, _score in results]

prompt = f"""You are given the following context:

{context_text}

Based on the above context, please answer the following question. Explain it very clearly. It is okay even if it is long.

Question: {query}
"""
# print(context_text)
API_KEY = api_keys[0]
client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=API_KEY,
)

sys_instr = "You are a helpful assistant which answers to the user's queries"

response = client.chat.completions.create(
    model="gemini-2.0-flash",
    messages=[
        {"role": "system", "content": sys_instr},
        {"role": "user", "content": prompt},
    ],
)

print(response.choices[0].message.content)
print(sources)