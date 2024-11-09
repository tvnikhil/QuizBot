# Quiz Bot for Network Security Course

## Project Description
The Quiz Bot is an interactive educational tool designed to enhance learning in network security. It leverages advanced language models and embedding techniques to generate quizzes based on a curated knowledge base derived from network security lecture slides. The bot supports multiple-choice questions (MCQs), true/false questions, and open-ended questions, providing a comprehensive assessment platform for students.

## Documentation
For detailed documentation on the architecture, API usage, and deployment, please refer to the 

## System Architecture
The system architecture is based on a modular design that includes the following components:
- **User  Interface**: Where users interact with the quiz bot.
- **Application Logic**: Manages quiz flow and user interactions.
- **Large Language Model (LLM)**: Generates questions and evaluates answers.
- **Embedding Models**: Converts text into embeddings for similarity search.
- **Vector Database (Faiss)**: Stores embeddings for fast retrieval.
- **Knowledge Base**: A collection of network security lecture slides converted to text.

![System Architecture Diagram]

## Video
A demonstration video of the Quiz Bot can be found 

## Prerequisites
Before you begin, ensure you have the following installed:
- Python 3.7 or later
- pip (Python package installer)
- A compatible operating system (Linux or Windows)

## Requirements
Install the required packages using pip. You can create a virtual environment for better dependency management.

```bash
pip install -r requirements.txt
