# import os
# import ollama
# from typing import List, Dict, Any, Optional
# from langchain_groq import ChatGroq
# # from langchain.vectorstores import Chroma
# from langchain_community.vectorstores import Chroma
# from langchain.schema import Document
# from langchain_chroma import Chroma
# import chromadb
# from utils import get_language_from_extension
# from config import dbloc


# class CodeRetriever:
#     def __init__(self):
#         # self.config = config
#         self.db_path = dbloc  # Updated to use "dbloc" from config.py
#         self.top_k = 3
        
#         # Initialize embedding model
#         self.embedding_model = ollama.embeddings(model='nomic-embed-text')

#         # Initialize ChromaDB client
#         self.client = chromadb.PersistentClient(path=self.db_path)

#     def retrieve_similar_code(self, code: str, language: str, collection_name: str) -> List[Document]:
#         """Retrieve similar code snippets from the vector database."""
#         try:
#             vectorstore = Chroma(
#                 client=self.client,
#                 collection_name=collection_name,
#                 embedding_function=self.embedding_model
#             )
            
#             # Search in vector database
#             results = vectorstore.similarity_search(
#                 query=code,
#                 k=self.top_k,
#                 filter={"language": language} if language != "Unknown" else None
#             )
            
#             return results
#         except Exception as e:
#             print(f"Error retrieving similar code: {e}")
#             return []
            
#     def retrieve_knowledge_for_review(self, code: str, file_path: Optional[str] = None, collection_name: str = "default") -> List[Dict[str, Any]]:
#         """Retrieve relevant knowledge for code review."""
#         language = get_language_from_extension(file_path) if file_path else "Unknown"
        
#         # Try to retrieve similar code from vector database
#         similar_docs = self.retrieve_similar_code(code, language, collection_name)
        
#         # Log retrieval status
#         if similar_docs:
#             print(f"✅ Found {len(similar_docs)} similar code snippets in ChromaDB.")
#         else:
#             print("⚠️ No similar code found in ChromaDB.")

#         # Convert Document objects to dictionaries for easier handling
#         knowledge_base = []
#         for doc in similar_docs:
#             knowledge_base.append({
#                 "content": doc.page_content,
#                 "metadata": doc.metadata
#             })
            
#         return knowledge_base


# import os
# import ollama
# from typing import List, Dict, Any, Optional
# from langchain_groq import ChatGroq
# from langchain_community.vectorstores import Chroma
# from langchain_chroma import Chroma
# from langchain.schema import Document
# import chromadb
# from utils import get_language_from_extension
# from config import dbloc
# from langchain.embeddings.base import Embeddings

# class OllamaEmbeddingWrapper(Embeddings):
#     def __init__(self, model_name="nomic-embed-text"):
#         self.model_name = model_name

#     def embed_documents(self, texts: List[str]) -> List[List[float]]:
#         """Generate embeddings for a list of documents."""
#         return [ollama.embeddings(model=self.model_name, prompt=text)["embedding"] for text in texts]

#     def embed_query(self, text: str) -> List[float]:
#         """Generate an embedding for a single query."""
#         return ollama.embeddings(model=self.model_name, prompt=text)["embedding"]

# class CodeRetriever:
#     def __init__(self):
#         self.db_path = dbloc  # Use "dbloc" from config.py
#         self.top_k = 5
        
#         # Initialize embedding model
#         self.embedding_model = OllamaEmbeddingWrapper()
        
#         # Initialize ChromaDB client
#         self.client = chromadb.PersistentClient(path=self.db_path)

#     def retrieve_similar_code(self, code: str, language: str, collection_name: str) -> List[Document]:
#         """Retrieve similar code snippets from the vector database."""
#         try:
#             # if collection_name not in [col.name for col in self.client.list_collections()]:
#             #     print(f"⚠️ Collection '{collection_name}' does not exist in ChromaDB.")
#             #     return []
#             vectorstore = Chroma(
#                 client=self.client,
#                 collection_name=collection_name,
#                 embedding_function=self.embedding_model#.embed_documents  # Correctly calling embeddings
#             )
            
#             # Generate embedding for the query
#             query_embedding = self.embedding_model.embed_query(text=code)
            
#             # Search in vector database
#             results = vectorstore.similarity_search_by_vector(
#                 query_embedding,
#                 k= 5,
#                 filter={"language": language} if language != "Unknown" else None
#             )
            
#             if not results:
#                 print("⚠️ No similar code found in ChromaDB.")
#             else:
#                 print(f"✅ Found {len(results)} similar code snippets in ChromaDB.")
            
#             return results
#         except Exception as e:
#             print(f"Error retrieving similar code: {e}")
#             return []
            
#     def retrieve_knowledge_for_review(self, code: str, file_path: Optional[str] = None, collection_name: str = "default") -> List[Dict[str, Any]]:
#         """Retrieve relevant knowledge for code review."""
#         language = get_language_from_extension(file_path) if file_path else "Unknown"
        
#         # Try to retrieve similar code from vector database
#         similar_docs = self.retrieve_similar_code(code, language, collection_name)
        
#         # Convert Document objects to dictionaries for easier handling
#         knowledge_base = []
#         for doc in similar_docs:
#             knowledge_base.append({
#                 "content": doc.page_content,
#                 "metadata": doc.metadata
#             })
            
#         return knowledge_base


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
        
    # def embed_documents(self, texts: List[str]) -> List[List[float]]:
    #     """Generate embeddings for a list of documents."""
    #     return [ollama.embeddings(model=self.model_name, prompt=text)["embedding"] for text in texts]
        
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
        self.db_path = dbloc  # Use "dbloc" from config.py
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
            
            # Debug: Print input code snippet before searching
            # print(f"Searching for similar code using the following query:\n{code[:300]}...")  # Print first 300 chars



            # Search directly using the text - let Chroma handle the embedding
            results = vectorstore.similarity_search_with_score(
                query = code,
                k= 3,
                # kwargs={
                #     "score_threshold": 0.4
                # }
                # filter={"language": language} if language != "Unknown" else None
            )
            # print("Raw results from similarity search:", results)

            # retriever = vectorstore.as_retriever(
            #     search_type = "similarity_score_threshold",
            #     search_kwargs={
            #        "score_threshold": 0.1,
            #         "k": 3
            #     }

            #     # filter={"language": language} if language != "Unknown" else None
            # )
            # results = retriever.

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
    
    # def retrieve_knowledge_for_review(self, code: str, file_path: Optional[str] = None, collection_name: str = "default") -> List[Dict[str, Any]]:
    #     """Retrieve relevant knowledge for code review."""
    #     language = get_language_from_extension(file_path) if file_path else "Unknown"
        
    #     # Try to retrieve similar code from vector database
    #     similar_docs = self.retrieve_similar_code(code, language, collection_name)
        
    #     # Convert Document objects to dictionaries for easier handling
    #     # knowledge_base = []
    #     # for doc in similar_docs:
    #     #     knowledge_base.append({
    #     #         "content": doc.page_content,
    #     #         "metadata": doc.metadata
    #     #     })
    #    # Convert Document-score tuples to dictionaries for easier handling
    #     knowledge_base = []
    #     for doc, score in similar_docs:  # Correctly unpack (Document, score)
    #         knowledge_base.append({
    #             "content": doc.page_content,
    #             "metadata": doc.metadata,
    #             "similarity_score": score  # Optional: store similarity score
    #         })
            
    #     return knowledge_base


    def retrieve_knowledge_for_review(self, code: str, file_path: Optional[str] = None, collection_name: str = "default") -> List[Dict[str, Any]]:
        """Retrieve knowledge for code review using ChromaDB or GitHub API based on similarity score."""
        language = get_language_from_extension(file_path) if file_path else "Unknown"
        similar_docs = self.retrieve_similar_code(code, language, collection_name)

        # Determine highest similarity score
        max_score = max((score for _, score in similar_docs), default=0)

        knowledge_base = []  # Ensure output is always in list-dict format

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
                    "content": snippet["file_url"],  # Store the file URL for reference
                    "metadata": snippet
                })

        else:
            print(" Using ChromaDB results for review.")
            
            # Append ChromaDB results to knowledge_base
            for doc, score in similar_docs:
                knowledge_base.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "similarity_score": score  # Optional: Store similarity score
                })

        return knowledge_base
