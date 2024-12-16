# Quiz Bot for Network Security Course

## Project Description

The Quiz Bot is an interactive educational tool designed to enhance learning in network security. It leverages advanced language models and embedding techniques to generate quizzes based on a curated knowledge base derived from network security lecture slides. The bot supports multiple-choice questions (MCQs), true/false questions, and open-ended questions, providing a comprehensive assessment platform for students.

## System Architecture

The system architecture is based on a modular design that includes the following components:

1. Data Processing Layer
   Text Extraction: Convert course slides to text with PyMuPDF.
   Embedding Generation: Used nomic-embed from Ollama to convert text into vector embeddings.

2. Embedding and Storage Layer
   Vector Database: Store embeddings in chromadb for efficient similarity search and retrieval.

3. Query Processing and LLM Layer
   Prompt Engineering: Formulate prompts based on question type (MCQ, True/False, Open-ended).
   LLM (Llama 3.2:8B): Generate responses using local LLM models with relevant context from Faiss.

4. User Interface (UI) Layer
   Frontend Development: Simple interactive UI using React and Flask.
   User Interaction: Accepts user input, displays responses, and provides feedback on answer accuracy.

To run the program for generating quiz and true/false questions using your RAG application, follow these clear steps:

### Prerequisites

Before running the program, ensure the following:

1. _Python 3.x_ is installed on your system.
2. _pip_ package manager is available for installing Python libraries.
3. _Ollama_ is installed and running locally as an API at <http://localhost:11434>. You need this for querying the model and getting embeddings.

### Setup the Project

1. _Set up your project directory:_

   - Clone this repo.
   - Update the file_path variables with the correct paths where your embeddings and data are stored. (if required)

2. _Create the Embedding Data:_ (if required or use the current repo's embeddings)

   - Make sure you have some data that can be processed and indexed. Run the load.py after putting the documents in the data directory.

3. _Ensure the Ollama API is running:_

### Running the Program

1. _Start the Python Program:_

   - Once everything is set up, open a terminal/command prompt and navigate to the directory where your rag.py script is located.
   - Run the script:
     bash
     python rag.py

2. _Check the Output:_

   - Follow on screen instructions to generate questions or ask questions about documents.

## Requirements

Install the required packages using pip. You can create a virtual environment for better dependency management.
