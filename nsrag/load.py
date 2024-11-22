from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.vectorstores.chroma import Chroma
from langchain_community.embeddings.ollama import OllamaEmbeddings
import warnings
warnings.filterwarnings("ignore")

CHROMA_PATH = "chroma"
DATA_PATH = "data"

def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=80)
    return text_splitter.split_documents(documents)

documents = PyPDFDirectoryLoader(DATA_PATH).load()
chunks = split_documents(documents)
db = Chroma(persist_directory=CHROMA_PATH, embedding_function=OllamaEmbeddings(model="nomic-embed-text"))
for idx, chunk in enumerate(chunks):
    source = chunk.metadata.get("source", "Unknown Source")
    page = chunk.metadata.get("page", "Unknown Page")
    chunk.metadata["page_info"] = f"{source}:{page}:{idx}"
db.add_documents(chunks, ids=[chunk.metadata["page_info"] for chunk in chunks])
db.persist()  # Save changes to disk