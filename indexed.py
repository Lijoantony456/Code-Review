import os
import ollama
import time
from typing import List, Dict, Any, Optional
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain.schema import Document
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
import chromadb
from parser import parse_code_file
from utils import filter_code_files, is_binary_file, clean_code, get_language_from_extension
from config import codes, dbloc, chunksize, chunkoverlap

class CodeRepositoryIndexer:
    def __init__(self):
        self.db_path = dbloc
        self.base_directory = codes
        self.chunk_size = chunksize
        self.chunk_overlap = chunkoverlap
        
        # Initialize embedding model
        self.embedding_model = OllamaEmbeddings(model="nomic-embed-text")
        
        # Initialize ChromaDB
        os.makedirs(self.db_path, exist_ok=True)
        self.client = chromadb.PersistentClient(path=self.db_path)
    
    def is_file_indexed(self, file_path: str) -> bool:
        """Check if a file's embeddings already exist in ChromaDB."""
        language = get_language_from_extension(file_path)
        collection = self.client.get_or_create_collection(name=language)
        existing_data = collection.get(include=["metadatas"])
        existing_ids = {meta["full_path"] for meta in existing_data["metadatas"] if meta}
        return file_path in existing_ids

    def get_all_files(self, directory: str) -> List[str]:
        """Get all code file paths from a directory."""
        file_paths = []
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if not is_binary_file(file_path):
                    file_paths.append(file_path)
        return filter_code_files(file_paths)
    
    def read_file_content(self, file_path: str) -> Optional[str]:
        """Read and return the content of a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return None

    def create_documents(self, directory: str, language: str) -> List[Document]:
        """Create Document objects from files in a specific language folder."""
        file_paths = self.get_all_files(directory)
        documents = []
        
        for file_path in file_paths:
            if self.is_file_indexed(file_path):
                print(f"Skipping indexed file: {file_path}")
                continue
            
            content = self.read_file_content(file_path)
            if content:
                rel_path = os.path.relpath(file_path, directory)
                
                # Parse code to extract functions, classes, etc.
                parsed_elements = parse_code_file(file_path, content, language)
                
                for element in parsed_elements:
                    doc = Document(
                        page_content=element["content"],
                        metadata={
                            "source": rel_path,
                            "language": language,
                            "type": element["type"],
                            "name": element["name"],
                            "full_path": file_path
                        }
                    )
                    documents.append(doc)
        
        return documents

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks."""
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
        )
        return splitter.split_documents(documents)

    def index_local_codebase(self, directory: str) -> str:
        """Index the entire local codebase, avoiding duplicates and monitoring for new files."""
        collection_name = None  # Initialize collection_name

        for language in os.listdir(directory):
            language_path = os.path.join(directory, language)
            if os.path.isdir(language_path):
                print(f"Checking {language} code from {language_path}...")

                # Create documents from files
                documents = self.create_documents(language_path, language)
                if not documents:
                    print(f"No valid documents found for {language}")
                    continue

                # Split into chunks
                chunks = self.split_documents(documents)
                print(f"Created {len(chunks)} chunks for {language}")

                # Store in vector DB, ensuring no duplicates
                try:
                    collection = self.client.get_or_create_collection(name=language)
                    existing_data = collection.get(include=["metadatas"])
                    existing_ids = {meta["full_path"] for meta in existing_data["metadatas"] if meta}
                except Exception as e:
                    print(f"Error accessing collection for {language}: {e}")
                    existing_ids = set()

                new_chunks = [chunk for chunk in chunks if chunk.metadata["full_path"] not in existing_ids]
                if new_chunks:
                    vectorstore = Chroma(
                        client=self.client,
                        collection_name=language,
                        embedding_function=self.embedding_model
                    )
                    print(f"Generating embeddings for {len(new_chunks)} documents in {language}...")
                    vectorstore.add_documents(new_chunks)
                    print(f"Indexed {len(new_chunks)} new chunks for {language}")
                    
                    # **Verify storage by retrieving from DB**
                    collection = self.client.get_collection(language)
                    docs = collection.get(include=["documents", "metadatas"])
                    print(f" ChromaDB now contains {len(docs['documents'])} documents for {language}.")

                    
                    collection_name = language  
                else:
                    print(f"No new documents to add for {language}")

        return collection_name 