from flask import Flask, jsonify, request
import json
import logging
from lightrag import LightRAG, QueryParam
from lightrag.llm import ollama_model_complete, ollama_embedding
from lightrag.utils import EmbeddingFunc

app = Flask(__name__)

WORKING_DIR = "/Users/thanikella_nikhil/Projects-Courses/NS/data/emdNS"
file_path = '/Users/thanikella_nikhil/Projects-Courses/NS/data/out.txt'
prompt = '''
Generate a JSON object containing an array of 10 quiz questions. Each question should have: a question string, an options array with four options, each labeled with numbers (1, 2, 3, 4) and containing the option text, a correct_answer integer representing the correct option number (matching one of the option labels from 1 to 4).
Output only the JSON object in the specified format without any additional text.
Example of Expected JSON Format:
{
    {
      "question": "What is the purpose of public-key encryption?",
      "options": [
        { "1": "To encrypt sensitive information" },
        { "2": "To decrypt encrypted information" },
        { "3": "To authenticate messages" },
        { "4": "To secure data in transit" }
      ],
      "correct_answer": 1
    },
    {
      "question": "What is the difference between a public and private key in RSA?",
      "options": [
        { "1": "Public keys are longer than private keys" },
        { "2": "Private keys can be used to decrypt messages" },
        { "3": "Public keys are used for encryption, while private keys are used for decryption" },
        { "4": "Private keys must be kept secret at all times" }
      ],
      "correct_answer": 3
    }
}
'''

# Initialize logger
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

# Initialize LightRAG
rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=ollama_model_complete,
    llm_model_name="llama3.2:1b",
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

@app.route('/generate-quiz', methods=['GET'])
def generate_quiz():
    try:
        # Read the file synchronously (no async needed here)
        with open(file_path, 'r') as f:
            content = f.read()

        # Insert the content into the LightRAG model
        rag.insert(content)  # No await needed since we're not in an async function

        # Query the model to generate quiz data
        quiz_data_raw = rag.query(prompt, param=QueryParam(mode="hybrid"))
        print(quiz_data_raw)
        quiz_data = json.loads(quiz_data_raw)
        print()
        print()
        print(jsonify(quiz_data))
        print()
        print()
        print(type(quiz_data))
        return jsonify(quiz_data)

    except json.JSONDecodeError as e:
        return jsonify({"error": f"JSON decode error: {e}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
