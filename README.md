# Quiz Bot for Network Security Course

## Project Description
The Quiz Bot is an interactive educational tool designed to enhance learning in network security. It leverages advanced language models and embedding techniques to generate quizzes based on a curated knowledge base derived from network security lecture slides. The bot supports multiple-choice questions (MCQs), true/false questions, and open-ended questions, providing a comprehensive assessment platform for students.

## Documentation
For detailed documentation on the architecture, API usage, and deployment, please refer to the https://github.com/HKUDS/LightRAG/tree/main and Olama

## System Architecture
The system architecture is based on a modular design that includes the following components:
- **User  Interface**: Where users interact with the quiz bot.
- **Application Logic**: Manages quiz flow and user interactions.
- **Large Language Model (LLM)**: Generates questions and evaluates answers.
- **Embedding Models**: Converts text into embeddings for similarity search.
- **Vector Database (Faiss)**: Stores embeddings for fast retrieval.
- **Knowledge Base**: A collection of network security lecture slides converted to text.

![System Architecture]
1.Data Processing Layer
  Text Extraction: Convert course slides to text with PyMuPDF.
  Embedding Generation: Use Transformers (BERT-case) from Hugging Face to convert text into vector embeddings.
2. Embedding and Storage Layer
  Vector Database: Store embeddings in Faiss for efficient similarity search and retrieval.
  Indexing & Serialization: Faiss indexes are saved in JSON format for persistent, fast access during queries.
  ![image](https://github.com/user-attachments/assets/5d2a35f7-9b69-495b-a013-839e380892b1)
3. Query Processing and LLM Layer
  Prompt Engineering: Formulate prompts based on question type (MCQ, True/False, Open-ended).
  LLM (GPT4All-Falcon/Llama): Generate responses using local LLM models with relevant context from Faiss.
4. User Interface (UI) Layer
  Frontend Development: Simple interactive UI using Flask/FastAPI.
  User Interaction: Accepts user input, displays responses, and provides feedback on answer accuracy.

![image](https://github.com/user-attachments/assets/06a806e0-891f-44c9-a91f-0764a0aeedcf)


## Video
A demonstration video of the Quiz Bot can be found nsrag/NS sample demo.mov

## Prerequisites
Before you begin, ensure you have the following installed:
- Python 3.7 or later
- pip (Python package installer)
- A compatible operating system (Linux or Windows)

## Requirements
Install the required packages using pip. You can create a virtual environment for better dependency management.

```bash
pip install -r requirements.txt
