import os
import logging
from flask import Flask, jsonify
from lightrag import LightRAG, QueryParam
from lightrag.llm import ollama_model_complete, ollama_embedding
from lightrag.utils import EmbeddingFunc
import json

# Set up logging
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

# Define working directory
WORKING_DIR = "/Users/thanikella_nikhil/Projects-Courses/NS/QuizBot/data/emdNS"

if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)

# Initialize the RAG setup
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

# Insert data into the RAG system (ensure you have your data available)
file_path = '/Users/thanikella_nikhil/Projects-Courses/NS/QuizBot/data/out.txt'
with open(file_path, 'r') as f:
    rag.insert(f.read())

# Define the query prompt to ensure JSON format
prompt = '''Respond only in JSON format with no additional text.
Your response should include a list of questions, each with:
- "text" (the question text),
- "options" (an array of four answer choices),
- "correct" (the correct option answer choice's text from the options array generated).

For example:
{
  "questions": [
    {
      "text": "Sample question text?",
      "options": ["Key", "Play", "Station", "Chatgpt"],
      "correct": "Play"
    }
  ]
}

Based on the information from the documents in the knowledge base, generate 4 multiple-choice quiz questions.
The "correct" parameter should have the exact text of the correct answer option from the "options" parameter.
Respond only with valid JSON. Do not write an introduction or summary.'''

# Prompt to correct JSON
fix_prompt = '''Please ensure the JSON is properly formatted as in this example:
{
  "questions": [
    {
      "text": "Sample question text?",
      "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
      "correct": "correct answer option text"
    }
  ]
}
Return only JSON, no additional text.'''

# Initialize Flask app
app = Flask(__name__)

@app.route('/generate-quiz', methods=['GET'])
def generate_quiz():
    # Query the RAG system
    try:
        response = rag.query(prompt, param=QueryParam(mode="naive"))
        logging.info(f"Initial response: {response}")

        # Attempt to parse the JSON response
        try:
            parsed_response = json.loads(response)
            return jsonify(parsed_response), 200
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON: {e}.")
            
            # Request LLM to fix the JSON format
            # fix_response = rag.query(fix_prompt + response, param=QueryParam(mode="global"))
            from json_repair import repair_json
            fix_response = repair_json(response)
            return jsonify(json.loads(fix_response)), 200
            # logging.info(f"Fix response: {fix_response}")
            
            # # Try parsing the fixed JSON
            # try:
            #     parsed_fix_response = json.loads(fix_response)
            #     return jsonify(parsed_fix_response), 200
            # except json.JSONDecodeError as e:
            #     logging.error(f"Error decoding fixed JSON: {e}")
            #     return jsonify({"error": "Invalid response format from the model, even after correction."}), 500

    except Exception as e:
        logging.error(f"Error querying the model: {e}")
        return jsonify({"error": "Error while querying the model."}), 500


if __name__ == '__main__':
    app.run(debug=True)