import os
import ollama
from typing import List, Dict, Any, Optional
from langchain_groq import ChatGroq
from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
from langchain.schema import Document
import chromadb
from utils import get_language_from_extension
from config import dbloc
from langchain.embeddings.base import Embeddings
from github_search import GitHubCodeSearch

class OllamaEmbeddingWrapper(Embeddings):
    def __init__(self, model_name="nomic-embed-text"):
        self.model_name = model_name
        
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of documents."""
        embeddings = [ollama.embeddings(model=self.model_name, prompt=text)["embedding"] for text in texts]
        print(f"Generated {len(embeddings)} embeddings.")
        return embeddings


    def embed_query(self, text: str) -> List[float]:
        """Generate an embedding for a single query."""
        return ollama.embeddings(model=self.model_name, prompt=text)["embedding"]

class CodeRetriever:
    def __init__(self):
        self.db_path = dbloc 
        self.top_k = 5
        # Initialize embedding model
        self.embedding_model = OllamaEmbeddingWrapper()
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=self.db_path)
        self.github_search = GitHubCodeSearch()
    def retrieve_similar_code(self, code: str, language: str, collection_name: str) -> List[Document]:
        """Retrieve similar code snippets from the vector database."""
        try:
            print(f" Checking for collection '{language}' in ChromaDB...")
            # Check if collection exists using the new API approach
            collection_names = self.client.list_collections()
            
            if collection_name not in collection_names:
                print(f" Collection '{collection_name}' does not exist in ChromaDB. Available collections: {collection_names}")
                return []
                
            # Create Chroma vector store with the embedding function
            print(f" Collection '{language}' found. Connecting to vector store...")            
            vectorstore = Chroma(
                client=self.client,
                collection_name=language,
                embedding_function=self.embedding_model
            )
          
            # Search directly using the text - let Chroma handle the embedding
            results = vectorstore.similarity_search_with_score(
                query = code,
                k= 3,
            )
            # print("Raw results from similarity search:", results)

            if not results:
                print(" No similar code found in ChromaDB.")
                return []
            else:
                print(f" Found {len(results)} similar code snippets in ChromaDB.")

            
            return results
            
        except Exception as e:
            print(f"Error retrieving similar code: {e}")
            import traceback
            traceback.print_exc()
            return []

    
    def store_in_chromadb(self, code_snippets, collection_name: str):
        """Store retrieved GitHub code in ChromaDB."""
        collection = self.client.get_or_create_collection(collection_name)

        for snippet in code_snippets:
            collection.add(
                documents=[snippet["file_url"]],  # Storing file URL
                metadatas=[{"repo": snippet["repo_name"], "path": snippet["file_path"]}]
            )

        print(f"Stored {len(code_snippets)} GitHub snippets in ChromaDB.")        

    def retrieve_knowledge_for_review(self, code: str, file_path: Optional[str] = None, collection_name: str = "default") -> List[Dict[str, Any]]:
        """Retrieve knowledge for code review using ChromaDB or GitHub API based on similarity score."""
        language = get_language_from_extension(file_path) if file_path else "Unknown"
        similar_docs = self.retrieve_similar_code(code, language, collection_name)

        # Determine highest similarity score
        max_score = max((score for _, score in similar_docs), default=0)

        knowledge_base = []  
        if max_score > 300:
            print(" High similarity score (>300) detected! Using GitHub search instead.")
            
            # Perform GitHub search
            github_results = self.github_search.search_code(query=code, language=language)
            extracted_snippets = self.github_search.extract_code_snippets(github_results)
            
            # Store GitHub results in ChromaDB
            self.store_in_chromadb(extracted_snippets, collection_name)

            # Append GitHub search results to knowledge_base
            for snippet in extracted_snippets:
                knowledge_base.append({
                    "content": snippet["file_url"], 
                    "metadata": snippet
                })

        else:
            print("📝 Using ChromaDB results for review.")
            
            # Append ChromaDB results to knowledge_base
            for doc, score in similar_docs:
                knowledge_base.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "similarity_score": score 
                })

        return knowledge_base
