# Quiz Bot for Network Security Course

## Project Description

The Quiz Bot is an interactive educational tool designed to enhance learning in network security. It leverages advanced language models and embedding techniques to generate quizzes based on a curated knowledge base derived from network security lecture slides. The bot supports multiple-choice questions (MCQs), true/false questions, and open-ended questions, providing a comprehensive assessment platform for students.

Full stack app for this project is in development. We are using reactjs for frontend, flask for the backend and chromadb to store vector embeddings. 

## System Architecture

The system architecture is based on a modular design that includes the following components:

1. Data Processing Layer
   Text Extraction: Convert course slides to text with PyMuPDF.
   Embedding Generation: Used nomic-embed from Ollama to convert text into vector embeddings.

2. Embedding and Storage Layer
   Vector Database: Store embeddings in chromadb for efficient similarity search and retrieval.

3. Query Processing and LLM Layer
   Prompt Engineering: Formulate prompts based on question type (MCQ, True/False, Open-ended).
   LLM (Llama 3.2): Generate responses using local LLM models with relevant context from Faiss.

4. User Interface (UI) Layer
   Frontend Development: Simple interactive UI using React and Flask.
   User Interaction: Accepts user input, displays responses, and provides feedback on answer accuracy.

To run the program for generating quiz and true/false questions using your RAG application, follow these clear steps:

### Prerequisites:

Before running the program, ensure the following:

1. _Python 3.x_ is installed on your system.
2. _pip_ package manager is available for installing Python libraries.
3. _Ollama_ is installed and running locally as an API at http://localhost:11434. You need this for querying the model and getting embeddings.

### Setup the Project

1. _Set up your project directory:_

   - Create a directory for your project (e.g., QuizBot).
   - Inside your project directory, create a folder for storing embeddings (e.g., data/emdNS), and another folder (e.g., data/out.txt) for reading input data.

2. _Modify the Code:_

   - Copy and paste the code from the previous steps into a Python file (e.g., quizbot.py).
   - Update the file_path variables with the correct paths where your embeddings and data are stored.

3. _Create the Embedding Data:_

   - Make sure you have some data that can be processed and indexed. In this case, the file /Users/thanikella_nikhil/Projects-Courses/NS/QuizBot/data/out.txt should contain relevant text for generating quiz questions.

   If you do not have a sample file, you can create a plain text file with random content or any text related to quiz topics.

4. _Ensure the Ollama API is running:_
   - Start the Ollama model API using:
     bash
     ollama run --model llama3.2 --host localhost --port 11434

### Running the Program

1. _Start the Python Program:_

   - Once everything is set up, open a terminal/command prompt and navigate to the directory where your quizbot.py script is located.
   - Run the script:
     bash
     python rag.py

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.7 or later
- pip (Python package installer)
- A compatible operating system (Linux or Windows)

## Requirements

Install the required packages using pip. You can create a virtual environment for better dependency management.
