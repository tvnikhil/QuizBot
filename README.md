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


To run the program for generating quiz and true/false questions using your RAG application with LightRAG, follow these clear steps:

### Prerequisites:
Before running the program, ensure the following:
1. *Python 3.x* is installed on your system.
2. *pip* package manager is available for installing Python libraries.
3. *Ollama* is installed and running locally as an API at http://localhost:11434. You need this for querying the model and getting embeddings.
4. *LightRAG* and *other dependencies* like httpx and lightrag should be installed. If not, install them using:
   bash
   pip install light-rag httpx
   

### Setup the Project
1. *Set up your project directory:*
   - Create a directory for your project (e.g., QuizBot).
   - Inside your project directory, create a folder for storing embeddings (e.g., data/emdNS), and another folder (e.g., data/out.txt) for reading input data.

2. *Modify the Code:*
   - Copy and paste the code from the previous steps into a Python file (e.g., quizbot.py).
   - Update the WORKING_DIR and file_path variables with the correct paths where your embeddings and data are stored.

3. *Create the Embedding Data:*
   - Make sure you have some data that LightRAG can process and index. In this case, the file /Users/thanikella_nikhil/Projects-Courses/NS/QuizBot/data/out.txt should contain relevant text for generating quiz questions.
   
   If you do not have a sample file, you can create a plain text file with random content or any text related to quiz topics.

4. *Ensure the Ollama API is running:*
   - Start the Ollama model API using:
     bash
     ollama run --model llama3.2 --host localhost --port 11434
     

### Running the Program

1. *Start the Python Program:*
   - Once everything is set up, open a terminal/command prompt and navigate to the directory where your quizbot.py script is located.
   - Run the script:
     bash
     python quizbot.py
     

2. *Check the Output:*
   - The program will generate and print the quiz and true/false questions directly in the terminal. Example output:
     
     Quiz Questions:
     Question: What is the purpose of public-key encryption?
     1. To encrypt sensitive information
     2. To decrypt encrypted information
     3. To authenticate messages
     4. To secure data in transit
     Answer: 1

     Question: What is the key characteristic of stream ciphers?
     1. High security
     2. Low computational complexity
     3. Statistically random
     4. Correlation immunity
     Answer: 2

     True/False Questions:
     Question: Is NS easy?
     Answer: True
     
     Question: Is NS complex?
     Answer: False
     

3. *Troubleshoot:*
   - If you encounter issues, ensure that:
     - The Ollama service is running and the correct port (11434) is open.
     - The file paths (WORKING_DIR, file_path) are correct and accessible.
     - The Python dependencies (light-rag, httpx) are installed correctly.

By following these steps, the program should generate and display quiz and true/false questions in the specified plain text format. Let me know if you face any issues!

## Video
A demonstration video of the Quiz Bot can be found https://github.com/Aditya-Bhargav-dev/QuizBot/nsrag/NS sample demo.mov

## Prerequisites
Before you begin, ensure you have the following installed:
- Python 3.7 or later
- pip (Python package installer)
- A compatible operating system (Linux or Windows)

## Requirements
Install the required packages using pip. You can create a virtual environment for better dependency management.

```bash
pip install -r requirements.txt
