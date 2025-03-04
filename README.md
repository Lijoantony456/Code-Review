# Code Review System

## Overview
The **Code Review System** is an AI-powered tool designed to automate the process of reviewing code. It utilizes a **Retrieval-Augmented Generation (RAG) pipeline** to analyze code submissions, retrieve similar code snippets from a local repository or GitHub (if necessary), and provide structured feedback. This system helps developers improve code quality by detecting issues, suggesting optimizations, and enforcing best practices.

## Features
- **Automated Code Review**: Uses an LLM to review submitted code.
- **RAG Pipeline**: Retrieves relevant code snippets for contextual understanding.
- **ChromaDB Integration**: Stores and retrieves vectorized code snippets for similarity search.
- **GitHub API Support**: Fetches external code references when necessary.
- **CLI-Based Interface**: Allows users to upload files and view reviews directly from the terminal.
- **Local Code Indexing**: Indexes and retrieves code from a local repository.

## Tech Stack
- **Programming Language**: Python
- **Framework**: LangChain
- **Database**: ChromaDB
- **LLM Provider**: Groq
- **Embeddings Model**: Ollama

## Project Structure
```
code-review-system/
│── codes/                   # Indexed code database
│── dbloc/                   # Location of vector embeddings    
│── config.py                # Configuration settings
│── parser.py                # To parse codes
│── indexed.py               # Local codebase indexing
│── retriever.py             # Code retrieval module
│── github_search.py         # To search code on github
│── reviewer.py              # Code review module
│── cli_review.py            # CLI interface for uploading and reviewing files
│── main_backup.py           # API-based interface (optional)
│── utils.py                 # Utility functions
│── requirements.txt         # Dependencies
│── README.md                # Project documentation
```

## Usage
### **CLI Mode (Recommended)**
1. **Run the CLI tool**
   ```sh
   python cli_review.py /path/to/your/code.py
   ```
2. **View the review in the terminal**
   - The system will analyze your code and return a structured review with issues, strengths, and refactoring suggestions.

### **API Mode (Optional)**
1. **Run the API server**
   ```sh
   python main.py
   ```
2. **Use the API Endpoints**
   - **Upload a file**:
     ```sh
     curl -X POST -F "file=@/path/to/code.py" http://127.0.0.1:6000/upload/
     ```
   - **Review a file**:
     ```sh
     curl -X POST -F "file=@/path/to/code.py" http://127.0.0.1:6000/review/
     ```

## How It Works
1. **Code Submission**: Users submit a file via CLI or API.
2. **Knowledge Retrieval**: The system searches for similar code snippets in ChromaDB.
   - If no relevant matches are found, it queries GitHub (if threshold criteria are met).
3. **Prompt Construction**: The retrieved knowledge and submitted code are combined into a structured prompt for the LLM.
4. **Code Review Generation**: The LLM analyzes the code and provides feedback.
5. **Output**: The review is displayed in the CLI or returned via API.


