import os
import shutil
import uvicorn
from fastapi import FastAPI, File, UploadFile
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from utils import load_config, get_language_from_extension
from indexed import CodeRepositoryIndexer
from retriever import CodeRetriever
from reviewer import CodeReviewer
from config import codes, dbloc, cache_dir, chunksize, chunkoverlap

# Load environment variables
load_dotenv()

# Initialize console for rich output
console = Console()

# Create FastAPI app for file upload
api_app = FastAPI(title="Code Review API", version="1.0")

# Load configuration
try:
    config = {
        "codes": codes,
        "dbloc": dbloc,
        "cache_dir": cache_dir,
        "chunksize": chunksize,
        "chunkoverlap": chunkoverlap,
    }
except Exception as e:
    console.print(f"[bold red]Error loading configuration: {e}[/bold red]")
    raise SystemExit(1)

# Initialize services
indexer = CodeRepositoryIndexer()
retriever = CodeRetriever()
reviewer = CodeReviewer()

# Base directory for storing uploaded code files
BASE_CODE_DIR = codes

def file_already_exists(file_path: str) -> bool:
    """Check if the file already exists in the local directory."""
    return os.path.exists(file_path)

def save_uploaded_file(uploaded_file: UploadFile) -> str:
    """Save uploaded file if it does not already exist."""
    try:
        file_name = uploaded_file.filename
        language = get_language_from_extension(file_name)
        language_folder = os.path.join(BASE_CODE_DIR, language)
        os.makedirs(language_folder, exist_ok=True)
        
        file_path = os.path.join(language_folder, file_name)
        
        if file_already_exists(file_path):
            console.print(f"[bold yellow]File already exists: {file_path}[/bold yellow]")
            return file_path

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(uploaded_file.file, buffer)

        console.print(f"[bold green]File saved to: {file_path}[/bold green]")
        return file_path
    except Exception as e:
        console.print(f"[bold red]Error saving file: {e}[/bold red]")
        return None

def auto_index_and_store(file_path: str) -> None:
    """Automatically index the file if it is not already indexed."""
    console.print(f"[bold yellow]Checking if file needs to be indexed: {file_path}[/bold yellow]")
    
    if indexer.is_file_indexed(file_path):
        console.print(f"[bold yellow]File already indexed, skipping: {file_path}[/bold yellow]")
        return
    
    try:
        collection_name = indexer.index_local_codebase(BASE_CODE_DIR)
        if collection_name:
            console.print(f"[bold green]File indexed successfully in collection: {collection_name}[/bold green]")
        else:
            console.print("[bold yellow]No new documents were indexed.[/bold yellow]")
    except Exception as e:
        console.print(f"[bold red]Auto-indexing failed: {e}[/bold red]")

@api_app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """API endpoint to upload a code file."""
    file_path = save_uploaded_file(file)
    if file_path:
        auto_index_and_store(file_path)
        return {"message": "File uploaded and indexed successfully", "file_path": file_path}
    return {"error": "File upload failed"}

@api_app.post("/review/")
async def review_file(file: UploadFile = File(...)):
    """API endpoint to upload a code file and get a review."""
    file_path = save_uploaded_file(file)
    if not file_path:
        return {"error": "File upload failed"}
    
    auto_index_and_store(file_path)
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
    except Exception as e:
        return {"error": f"Error reading file: {e}"}
    
    knowledge_base = retriever.retrieve_knowledge_for_review(code, file_path, "default")
    review_result = reviewer.review_code(code, file_path, knowledge_base)
    
    return {"review": review_result}

if __name__ == "__main__":
    uvicorn.run(api_app, host="127.0.0.1", port=6000)




