import os
import requests

class GitHubCodeSearch:
    def __init__(self):
        self.api_key = os.getenv("GITHUB_API_KEY")
        self.headers = {"Authorization": f"token {self.api_key}"}
        self.base_url = "https://api.github.com/search/code"

    def search_code(self, query: str, language: str = "python", per_page: int = 5):
        """Search GitHub for code similar to the given query."""
        params = {
            "q": f"{query} language:{language}",
            "sort": "indexed",
            "order": "desc",
            "per_page": per_page
        }

        response = requests.get(self.base_url, headers=self.headers, params=params)

        if response.status_code == 200:
            results = response.json().get("items", [])
            return results  
        else:
            print(f"GitHub API Error: {response.status_code}, {response.json()}")
            return []

    def extract_code_snippets(self, results):
        """Extract meaningful code snippets from GitHub search results."""
        snippets = []
        for item in results:
            file_url = item.get("html_url")  
            repo_name = item.get("repository", {}).get("full_name", "Unknown Repo")

            snippet = {
                "file_url": file_url,
                "repo_name": repo_name,
                "file_path": item.get("path", "Unknown Path")
            }
            snippets.append(snippet)

        return snippets
