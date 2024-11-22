from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain_community.embeddings.ollama import OllamaEmbeddings
import warnings
warnings.filterwarnings("ignore")
from prompt_templates import *
import random

TOPICS = [
    "OSI architecture", "Symmetric Encryption", "Rijndael", "Entropy",
    "Pseudorandom Number Generator", "Block and Stream Ciphers", "RC4 Stream Cipher",
    "Public-Key Cryptography", "RSA", "Attack approaches", "Homomorphic encryption",
    "Message authentication", "Hash functions and Requirements for secure hash functions",
    "Secure Hash Function", "Length Extension Attacks", "Message Authentication Code",
    "HMAC", "Authenticated Encryption", "TLS 1.0 Lucky 13 Attack", "Digital Signatures",
    "Hybrid Encryption", "symmetric key distribution", "Diffie-Hellman Key Exchange"
]

CHROMA_PATH = "chroma2"

model = Ollama(model="llama3.2:latest")
db = Chroma(persist_directory=CHROMA_PATH, embedding_function=OllamaEmbeddings(model="nomic-embed-text"))

def get_response_and_sources(query_text, template):
    results = db.similarity_search_with_score(query_text, k=10)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in results])
    prompt_template = ChatPromptTemplate.from_template(template)
    prompt = prompt_template.format(context=context_text, question=query_text)
    response_text = model.invoke(prompt)
    sources = [doc.metadata.get("id", None)[:-2] for doc, _ in results]
    formatted_response = f"Response: {response_text}\n\n\nCitations: {sources}"
    return formatted_response, context_text, sources

def open_questions(question):
    response, _, _ = get_response_and_sources(question, OPEN_ENDED_QUESTION_PROMPT)
    return response

def generate_mcq_quiz():
    print("Generating a general MCQ Quiz:")
    selected_topics = random.sample(TOPICS, 2)
    db_query = f"Give me a set of multiple-choice questions on {', '.join(selected_topics)}."
    results = db.similarity_search_with_score(db_query, k=7)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in results])

    prompt_template = ChatPromptTemplate.from_template(QUIZ_MCQ_GENERAL_PROMPT)
    prompt = prompt_template.format(context=context_text)
    response_text = model.invoke(prompt)
    sources = [doc.metadata.get("id", None)[:-2] for doc, _ in results]
    print(f"Response: {response_text}\n\n\nCitations: {sources}")

    user_answers = input("\nGive your answers like this: 1. A 2. B 3. C 4. D 5. A\n")
    eval_prompt_template = ChatPromptTemplate.from_template(EVAL_QUIZ_MCQ_GENERAL_PROMPT)
    eval_prompt = eval_prompt_template.format(context=context_text, questions=response_text, usrAns=user_answers)
    eval_response = model.invoke(eval_prompt)
    print(f"Evaluation: {eval_response}\n\n\nCitations: {sources}")

def generate_tf_quiz():
    print("Generating a general T/F Quiz:")
    selected_topics = random.sample(TOPICS, 2)
    db_query = f"Give me a set of true/false questions on {', '.join(selected_topics)}."
    results = db.similarity_search_with_score(db_query, k=7)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in results])

    prompt_template = ChatPromptTemplate.from_template(QUIZ_TF_GENERAL_PROMPT)
    prompt = prompt_template.format(context=context_text)
    response_text = model.invoke(prompt)
    sources = [doc.metadata.get("id", None)[:-2] for doc, _ in results]
    print(f"Response: {response_text}\n\n\nCitations: {sources}")

    user_answers = input("\nGive your answers like this: 1. True 2. False 3. True 4. False 5. True\n")
    eval_prompt_template = ChatPromptTemplate.from_template(EVAL_QUIZ_TF_GENERAL_PROMPT)
    eval_prompt = eval_prompt_template.format(context=context_text, questions=response_text, usrAns=user_answers)
    eval_response = model.invoke(eval_prompt)
    print(f"Evaluation: {eval_response}\n\n\nCitations: {sources}")

def generate_mcq_quiz_by_topic(topic):
    print(f"Generating MCQ Quiz on {topic}")
    db_query = f"Give me information about {topic}"
    response, context_text, sources = get_response_and_sources(db_query, QUIZ_MCQ_TOPIC_PROMPT)
    print(response)

    user_answers = input("\nGive your answers like this: 1. A 2. B 3. C 4. D 5. A\n")
    eval_prompt_template = ChatPromptTemplate.from_template(EVAL_QUIZ_MCQ_TOPIC_PROMPT)
    eval_prompt = eval_prompt_template.format(context=context_text, questions=response, usrAns=user_answers)
    eval_response = model.invoke(eval_prompt)
    print(f"Evaluation: {eval_response}\n\n\nCitations: {sources}")

def generate_tf_quiz_by_topic(topic):
    print(f"Generating T/F Quiz on {topic}")
    db_query = f"Give me information about {topic}"
    response, context_text, sources = get_response_and_sources(db_query, QUIZ_TF_TOPIC_PROMPT)
    print(response)

    user_answers = input("\nGive your answers like this: 1. True 2. False 3. True 4. False 5. True\n")
    eval_prompt_template = ChatPromptTemplate.from_template(EVAL_QUIZ_TF_TOPIC_PROMPT)
    eval_prompt = eval_prompt_template.format(context=context_text, questions=response, usrAns=user_answers)
    eval_response = model.invoke(eval_prompt)
    print(f"Evaluation: {eval_response}\n\n\nCitations: {sources}")

if __name__ == "__main__":
    while True:
        menu = '''
        1. Open-ended questions
        2. Quiz MCQ
        3. Quiz MCQ by topic
        4. Quiz T/F
        5. Quiz T/F by topic
        6. Exit
        '''
        print(menu)
        option = int(input("Select a mode: "))
        
        if option == 6:
            print("Bye")
            break
        elif option == 1:
            question = input("What's your question?: ")
            print(open_questions(question))
        elif option == 2:
            generate_mcq_quiz()
        elif option == 3:
            topic = input("On which topic?: ")
            generate_mcq_quiz_by_topic(topic)
        elif option == 4:
            generate_tf_quiz()
        elif option == 5:
            topic = input("On which topic?: ")
            generate_tf_quiz_by_topic(topic)