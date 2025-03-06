import os
import time
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.schema.document import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import warnings
from secretKeys import *

warnings.filterwarnings("ignore")

# Path to the markdown files generated from your images
final_md_path = "/Users/thanikella_nikhil/Projects-Courses/NS/QuizBot/backend-fastapi-ms/data/data1md"

current_api_key_index = 0

def get_embeddings():
    """
    Set the current API key in the environment and initialize the embeddings model.
    """
    os.environ["GOOGLE_API_KEY"] = api_keys[current_api_key_index]
    return GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

def rotate_api_key():
    """
    Rotate to the next API key.
    """
    global current_api_key_index
    current_api_key_index = (current_api_key_index + 1) % len(api_keys)
    print(f"Rotated API key. Now using key index: {current_api_key_index}")

# Text splitter configuration
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=650,
    chunk_overlap=90,
    length_function=len,
)

def calculate_chunk_ids(chunks):
    """
    Calculate unique chunk IDs based on the source (file name) and the chunk index.
    """
    last_source = None
    current_chunk_index = 0
    for chunk in chunks:
        source = chunk.metadata.get("source")
        if source == last_source:
            current_chunk_index += 1
        else:
            current_chunk_index = 0
        chunk_id = f"{source}:{current_chunk_index}"
        chunk.metadata["id"] = chunk_id
        last_source = source
    return chunks

def add_to_chroma(enriched_chunks: list[Document], max_retries=3):
    """
    Add new document chunks to the Chroma vector store if they do not already exist.
    If an error occurs (e.g. due to API key issues), rotate the key and retry.
    """
    attempts = 0
    while attempts < max_retries:
        try:
            embeddings = get_embeddings()
            db = Chroma(
                persist_directory="/Users/thanikella_nikhil/Projects-Courses/NS/QuizBot/backend-fastapi-ms/chroma/chroma-gemini",
                embedding_function=embeddings
            )
            # Retrieve existing document IDs from the database
            existing_ids = set(db.get()["ids"])
            
            new_chunks = []
            for chunk in enriched_chunks:
                chunk_id = chunk.metadata.get("id")
                if chunk_id not in existing_ids:
                    new_chunks.append(chunk)
            
            if new_chunks:
                print(f"Adding {len(new_chunks)} new documents to ChromaDB.")
                new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
                db.add_documents(new_chunks, ids=new_chunk_ids)
                db.persist()
            else:
                print("No new documents to add.")
            return  # Success; exit the retry loop.
        except Exception as e:
            attempts += 1
            print(f"Error adding to Chroma on attempt {attempts}: {e}")
            rotate_api_key()
            time.sleep(5)
    print("Failed to add documents to Chroma after maximum retries.")

# Process every markdown file in the directory
for filename in os.listdir(final_md_path):
    if filename.lower().endswith(".md"):
        file_path = os.path.join(final_md_path, filename)
        print(f"Processing file: {filename}")
        with open(file_path, "r", encoding="utf-8") as f:
            full_text = f.read()
        
        # Split the full text into document chunks
        chunks = text_splitter.create_documents([full_text])
        enriched_documents = []
        # Use the file name (without extension) as the source metadata
        source_name, _ = os.path.splitext(filename)
        
        for idx, doc in enumerate(chunks):
            doc.metadata = {"source": source_name, "chunk_index": idx}
            enriched_documents.append(doc)
        
        # Calculate unique IDs for the chunks
        enriched_documents = calculate_chunk_ids(enriched_documents)
        
        # Optionally, print out each chunk's ID and source
        for doc in enriched_documents:
            print(f"Chunk ID: {doc.metadata['id']}, Source: {doc.metadata['source']}")
        
        # Add the new documents to Chroma with API key rotation on error
        add_to_chroma(enriched_documents)
        
        # Sleep for 1 seconds between processing files to manage rate limits
        time.sleep(1)
