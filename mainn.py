# import os
# import typer
# import shutil
# import uvicorn
# from fastapi import FastAPI, File, UploadFile
# from typing import Optional
# from dotenv import load_dotenv
# from rich.console import Console
# from rich.markdown import Markdown
# from utils import load_config, get_language_from_extension
# from indexed import CodeRepositoryIndexer
# from retriever import CodeRetriever
# from reviewer import CodeReviewer
# from config import codes, dbloc, cache_dir, chunksize, chunkoverlap

# # Load environment variables
# load_dotenv()

# # Initialize console for rich output
# console = Console()

# # Create Typer CLI app
# cli_app = typer.Typer(help="RAG-based Code Review System")

# # Create FastAPI app for file upload
# api_app = FastAPI(title="Code Review API", version="1.0")

# # Load configuration
# try:
#     config = {
#         "codes": codes,
#         "dbloc": dbloc,
#         "cache_dir": cache_dir,
#         "chunksize": chunksize,
#         "chunkoverlap": chunkoverlap,
#     }
# except Exception as e:
#     console.print(f"[bold red]Error loading configuration: {e}[/bold red]")
#     raise SystemExit(1)

# # Initialize services
# indexer = CodeRepositoryIndexer()
# retriever = CodeRetriever()
# reviewer = CodeReviewer()

# # Base directory for storing uploaded code files
# BASE_CODE_DIR = codes

# def save_uploaded_file(uploaded_file: UploadFile) -> str:
#     """Save uploaded file in a subfolder based on its language."""
#     try:
#         file_name = uploaded_file.filename
#         language = get_language_from_extension(file_name)
#         language_folder = os.path.join(BASE_CODE_DIR, language)
#         os.makedirs(language_folder, exist_ok=True)

#         file_path = os.path.join(language_folder, file_name)
#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(uploaded_file.file, buffer)

#         console.print(f"[bold green]File saved to: {file_path}[/bold green]")
#         return file_path
#     except Exception as e:
#         console.print(f"[bold red]Error saving file: {e}[/bold red]")
#         return None

# def auto_index_and_store(file_path: str):
#     """Automatically index, extract, and store code in ChromaDB."""
#     console.print(f"[bold yellow]Auto-indexing file: {file_path}[/bold yellow]")
#     try:
#         collection_name = indexer.index_local_codebase(BASE_CODE_DIR, "default")
#         console.print(f"[bold green]File indexed successfully in collection: {collection_name}[/bold green]")
#     except Exception as e:
#         console.print(f"[bold red]Auto-indexing failed: {e}[/bold red]")

# @api_app.post("/upload/")
# async def upload_file(file: UploadFile = File(...)):
#     """API endpoint to upload a code file."""
#     file_path = save_uploaded_file(file)
#     if file_path:
#         auto_index_and_store(file_path)
#         return {"message": "File uploaded and indexed successfully", "file_path": file_path}
#     return {"error": "File upload failed"}

# @cli_app.command()
# def index(
#     local_dir: Optional[str] = typer.Option(None, "--dir", "-d", help="Path to local directory to index"),
#     collection: Optional[str] = typer.Option(None, "--collection", "-c", help="Name of the collection in the vector database")
# ):
#     """Index a local directory for code review."""
#     if not local_dir:
#         console.print("[bold red]Error: A local directory must be provided[/bold red]")
#         raise typer.Exit(1)
    
#     console.print(f"[bold green]Indexing local directory: {local_dir}[/bold green]")
#     collection_name = indexer.index_local_codebase(local_dir, collection or "default")
#     console.print(f"[bold green]Indexing completed. Collection name: {collection_name}[/bold green]")

# @cli_app.command()
# def review(
#     file_path: str = typer.Argument(..., help="Path to the file to review"),
#     collection: str = typer.Option("default", "--collection", "-c", help="Name of the collection to use for retrieval")
# ):
#     """Review a code file using the RAG pipeline."""
#     try:
#         with open(file_path, 'r', encoding='utf-8') as file:
#             code = file.read()
#     except Exception as e:
#         console.print(f"[bold red]Error loading file: {e}[/bold red]")
#         raise typer.Exit(1)

#     console.print(f"[bold]Retrieving knowledge for review...[/bold]")
#     knowledge_base = retriever.retrieve_knowledge_for_review(code, file_path, collection)

#     console.print(f"[bold]Generating code review...[/bold]")
#     review_result = reviewer.review_code(code, file_path, knowledge_base)

#     console.print("\n[bold blue]CODE REVIEW RESULT[/bold blue]\n")
#     console.print(Markdown(review_result))

# @cli_app.command()
# def setup():
#     """Set up the initial environment for the RAG-based code review system."""
#     os.makedirs(BASE_CODE_DIR, exist_ok=True)
#     os.makedirs(dbloc, exist_ok=True)
#     os.makedirs(cache_dir, exist_ok=True)

#     console.print("[bold green]Environment setup completed.[/bold green]")
#     console.print("Ensure the following environment variables are set:")
#     console.print("  - GROQ_API_KEY: Your Groq API key")

# @cli_app.command()
# def run_api(host: str = "127.0.0.1", port: int = 8001):
#     """Run the FastAPI server for file uploads."""
#     uvicorn.run(api_app, host=host, port=port)

# # if __name__ == "__main__":
# #     cli_app()

# if __name__ == "__main__":
#     if len(os.sys.argv) == 1:
#         run_api()
#     else:
#         cli_app()




# import os
# import shutil
# import uvicorn
# from fastapi import FastAPI, File, UploadFile
# from dotenv import load_dotenv
# from rich.console import Console
# from rich.markdown import Markdown
# from utils import load_config, get_language_from_extension
# from indexed import CodeRepositoryIndexer
# from retriever import CodeRetriever
# from reviewer import CodeReviewer
# from config import codes, dbloc, cache_dir, chunksize, chunkoverlap

# # Load environment variables
# load_dotenv()

# # Initialize console for rich output
# console = Console()

# # Create FastAPI app for file upload
# api_app = FastAPI(title="Code Review API", version="1.0")

# # Load configuration
# try:
#     config = {
#         "codes": codes,
#         "dbloc": dbloc,
#         "cache_dir": cache_dir,
#         "chunksize": chunksize,
#         "chunkoverlap": chunkoverlap,
#     }
# except Exception as e:
#     console.print(f"[bold red]Error loading configuration: {e}[/bold red]")
#     raise SystemExit(1)

# # Initialize services
# indexer = CodeRepositoryIndexer()
# retriever = CodeRetriever()
# reviewer = CodeReviewer()

# # Base directory for storing uploaded code files
# BASE_CODE_DIR = codes

# def save_uploaded_file(uploaded_file: UploadFile) -> str:
#     """Save uploaded file in a subfolder based on its language."""
#     try:
#         file_name = uploaded_file.filename
#         language = get_language_from_extension(file_name)
#         language_folder = os.path.join(BASE_CODE_DIR, language)
#         os.makedirs(language_folder, exist_ok=True)

#         file_path = os.path.join(language_folder, file_name)
#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(uploaded_file.file, buffer)

#         console.print(f"[bold green]File saved to: {file_path}[/bold green]")
#         return file_path
#     except Exception as e:
#         console.print(f"[bold red]Error saving file: {e}[/bold red]")
#         return None

# # def auto_index_and_store(file_path: str) -> None:
# #     """Automatically index, extract, and store code in ChromaDB."""
# #     console.print(f"[bold yellow]Auto-indexing file: {file_path}[/bold yellow]")
# #     try:
# #         collection_name = indexer.index_local_codebase(BASE_CODE_DIR)
# #         console.print(f"[bold green]File indexed successfully in collection: {collection_name}[/bold green]")
# #     except Exception as e:
# #         console.print(f"[bold red]Auto-indexing failed: {e}[/bold red]")

# def auto_index_and_store(file_path: str) -> None:
#     """Automatically index, extract, and store code in ChromaDB."""
#     console.print(f"[bold yellow]Auto-indexing file: {file_path}[/bold yellow]")
#     try:
#         collection_name = indexer.index_local_codebase(BASE_CODE_DIR)
#         if collection_name:
#             console.print(f"[bold green]File indexed successfully in collection: {collection_name}[/bold green]")
#         else:
#             console.print("[bold yellow]No new documents were indexed.[/bold yellow]")
#     except Exception as e:
#         console.print(f"[bold red]Auto-indexing failed: {e}[/bold red]")


# @api_app.post("/upload/")
# async def upload_file(file: UploadFile = File(...)):
#     """API endpoint to upload a code file."""
#     file_path = save_uploaded_file(file)
#     if file_path:
#         auto_index_and_store(file_path)
#         return {"message": "File uploaded and indexed successfully", "file_path": file_path}
#     return {"error": "File upload failed"}

# # @api_app.post("/review/")
# # async def review_code(code: str, file_path: str = None):
# #     if not code:
# #         raise HTTPException(status_code=400, detail="Code cannot be empty.")
    
# #     knowledge_base = retriever.retrieve_knowledge_for_review(code, file_path)
# #     review_result = reviewer.review_code(code, file_path, knowledge_base)
    
# #     return {"review": review_result}

# @api_app.post("/review/")
# async def review_file(file: UploadFile = File(...)):
#     """API endpoint to upload a code file and get a review."""
#     file_path = save_uploaded_file(file)
#     if not file_path:
#         return {"error": "File upload failed"}
    
#     auto_index_and_store(file_path)
    
#     try:
#         with open(file_path, "r", encoding="utf-8") as f:
#             code = f.read()
#     except Exception as e:
#         return {"error": f"Error reading file: {e}"}
    
#     knowledge_base = retriever.retrieve_knowledge_for_review(code, file_path, "default")
#     review_result = reviewer.review_code(code, file_path, knowledge_base)
    
#     return {"review": review_result}


# if __name__ == "__main__":
#     uvicorn.run(api_app, host="127.0.0.1", port=6000)




# import os
# import shutil
# import uvicorn
# from fastapi import FastAPI, File, UploadFile
# from dotenv import load_dotenv
# from rich.console import Console
# from rich.markdown import Markdown
# from utils import load_config, get_language_from_extension
# from indexed import CodeRepositoryIndexer
# from retriever import CodeRetriever
# from reviewer import CodeReviewer
# from config import codes, dbloc, cache_dir, chunksize, chunkoverlap

# # Load environment variables
# load_dotenv()

# # Initialize console for rich output
# console = Console()

# # Create FastAPI app for file upload
# api_app = FastAPI(title="Code Review API", version="1.0")

# # Load configuration
# try:
#     config = {
#         "codes": codes,
#         "dbloc": dbloc,
#         "cache_dir": cache_dir,
#         "chunksize": chunksize,
#         "chunkoverlap": chunkoverlap,
#     }
# except Exception as e:
#     console.print(f"[bold red]Error loading configuration: {e}[/bold red]")
#     raise SystemExit(1)

# # Initialize services
# indexer = CodeRepositoryIndexer()
# retriever = CodeRetriever()
# reviewer = CodeReviewer()

# # Base directory for storing uploaded code files
# BASE_CODE_DIR = codes

# def file_already_exists(file_path: str) -> bool:
#     """Check if the file already exists in the local directory."""
#     return os.path.exists(file_path)

# def save_uploaded_file(uploaded_file: UploadFile) -> str:
#     """Save uploaded file if it does not already exist."""
#     try:
#         file_name = uploaded_file.filename
#         language = get_language_from_extension(file_name)
#         language_folder = os.path.join(BASE_CODE_DIR, language)
#         os.makedirs(language_folder, exist_ok=True)
        
#         file_path = os.path.join(language_folder, file_name)
        
#         if file_already_exists(file_path):
#             console.print(f"[bold yellow]File already exists: {file_path}[/bold yellow]")
#             return file_path

#         with open(file_path, "wb") as buffer:
#             shutil.copyfileobj(uploaded_file.file, buffer)

#         console.print(f"[bold green]File saved to: {file_path}[/bold green]")
#         return file_path
#     except Exception as e:
#         console.print(f"[bold red]Error saving file: {e}[/bold red]")
#         return None

# def auto_index_and_store(file_path: str) -> None:
#     """Automatically index the file if it is not already indexed."""
#     console.print(f"[bold yellow]Checking if file needs to be indexed: {file_path}[/bold yellow]")
    
#     if indexer.is_file_indexed(file_path):
#         console.print(f"[bold yellow]File already indexed, skipping: {file_path}[/bold yellow]")
#         return
    
#     try:
#         collection_name = indexer.index_local_codebase(BASE_CODE_DIR)
#         if collection_name:
#             console.print(f"[bold green]File indexed successfully in collection: {collection_name}[/bold green]")
#         else:
#             console.print("[bold yellow]No new documents were indexed.[/bold yellow]")
#     except Exception as e:
#         console.print(f"[bold red]Auto-indexing failed: {e}[/bold red]")

# @api_app.post("/upload/")
# async def upload_file(file: UploadFile = File(...)):
#     """API endpoint to upload a code file."""
#     file_path = save_uploaded_file(file)
#     if file_path:
#         auto_index_and_store(file_path)
#         return {"message": "File uploaded and indexed successfully", "file_path": file_path}
#     return {"error": "File upload failed"}

# @api_app.post("/review/")
# async def review_file(file: UploadFile = File(...)):
#     """API endpoint to upload a code file and get a review."""
#     file_path = save_uploaded_file(file)
#     if not file_path:
#         return {"error": "File upload failed"}
    
#     auto_index_and_store(file_path)
    
#     try:
#         with open(file_path, "r", encoding="utf-8") as f:
#             code = f.read()
#     except Exception as e:
#         return {"error": f"Error reading file: {e}"}
    
#     knowledge_base = retriever.retrieve_knowledge_for_review(code, file_path, "default")
#     review_result = reviewer.review_code(code, file_path, knowledge_base)
    
#     return {"review": review_result}

# if __name__ == "__main__":
#     uvicorn.run(api_app, host="127.0.0.1", port=6000)




