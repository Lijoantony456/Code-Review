
import os
import shutil
import argparse
from rich.console import Console
from rich.markdown import Markdown
from utils import get_language_from_extension
from indexed import CodeRepositoryIndexer
from retriever import CodeRetriever
from reviewer import CodeReviewer
from config import codes, dbloc, cache_dir, chunksize, chunkoverlap

# Initialize rich console
console = Console()

# Initialize services
indexer = CodeRepositoryIndexer()
retriever = CodeRetriever()
reviewer = CodeReviewer()

# Base directory for storing uploaded code files
BASE_CODE_DIR = codes

def file_already_exists(file_path: str) -> bool:
    """Check if the file already exists in the local directory."""
    return os.path.exists(file_path)

def save_uploaded_file(file_path: str) -> str:
    """Save file to structured directory based on language."""
    try:
        if not os.path.exists(file_path):
            console.print(f"[bold red]File does not exist: {file_path}[/bold red]")
            return None
        
        file_name = os.path.basename(file_path)
        language = get_language_from_extension(file_name)
        language_folder = os.path.join(BASE_CODE_DIR, language)
        os.makedirs(language_folder, exist_ok=True)

        destination_path = os.path.join(language_folder, file_name)

        if file_already_exists(destination_path):
            console.print(f"[bold yellow]File already exists: {destination_path}[/bold yellow]")
            return destination_path

        shutil.copy(file_path, destination_path)

        console.print(f"[bold green]File saved to: {destination_path}[/bold green]")
        return destination_path
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

def review_file(file_path: str):
    """Read, analyze, and review the provided file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
    except Exception as e:
        console.print(f"[bold red]Error reading file: {e}[/bold red]")
        return

    # Retrieve knowledge from indexed database
    knowledge_base = retriever.retrieve_knowledge_for_review(code, file_path, "default")

    # Perform code review
    review_result = reviewer.review_code(code, file_path, knowledge_base)

    # Display review output in CLI
    console.print("\n[bold cyan]--- CODE REVIEW RESULT ---[/bold cyan]\n")
    console.print(Markdown(review_result["content"]))

def main():
    """Command-line interface for uploading and reviewing files."""
    parser = argparse.ArgumentParser(description="CLI tool for automated code review.")
    parser.add_argument("file", type=str, help="Path to the code file for review.")

    args = parser.parse_args()
    file_path = args.file

    # Process the file
    saved_file_path = save_uploaded_file(file_path)
    if saved_file_path:
        auto_index_and_store(saved_file_path)
        review_file(saved_file_path)

if __name__ == "__main__":
    main()
