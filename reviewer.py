import os
from typing import List, Dict, Any, Optional
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from utils import get_language_from_extension

class CodeReviewer:
    def __init__(self):
        # Initialize LLM
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=os.environ.get("GROQ_API_KEY"),
            temperature=0.5
        )

    def format_knowledge_base(self, knowledge_base: List[Dict[str, Any]]) -> str:
        """Format the knowledge base for inclusion in the prompt."""
        # print("\n[DEBUG] Received knowledge base:", knowledge_base)  # Debugging

        if not knowledge_base:
            # print("[DEBUG] No similar code patterns found.")  # Debugging
            return "No similar code patterns found in the knowledge base."
        
        formatted = "RELATED CODE SNIPPETS FROM KNOWLEDGE BASE:\n\n"
        
        for i, item in enumerate(knowledge_base, 1):
            metadata = item.get("metadata", {})
            content = item.get("content", "")

            # print(f"\n[DEBUG] Formatting snippet {i}:")
            # print("[DEBUG] Metadata:", metadata)
            # print("[DEBUG] Content (first 100 chars):", content[:100])  # Debugging

            snippet = (
                f"SNIPPET {i}:\n"
                f"Source: {metadata.get('source', 'Unknown')}\n"
                f"Type: {metadata.get('type', 'Unknown')}\n"
                f"Language: {metadata.get('language', 'Unknown')}\n"
                f"Code:\n```\n{content[:1000]}{'...' if len(content) > 1000 else ''}\n```\n\n"
            )
            
            formatted += snippet
            
            if i >= 3:
                formatted += f"... and {len(knowledge_base) - 3} more snippets (summarized to avoid token limits)"
                break

        return formatted

    def create_review_prompt(self, code: str, knowledge_base: List[Dict[str, Any]], language: str) -> str:
        """Create a prompt for the code review."""
        formatted_knowledge_base = self.format_knowledge_base(knowledge_base)

        # print("\n[DEBUG] Final formatted knowledge base included in prompt:")
        # print(formatted_knowledge_base)  # Debugging

        template = """
        You are an expert code reviewer with deep knowledge of software development best practices, design patterns, and security considerations. Your task is to review the provided code and provide actionable, constructive feedback.

        # CODE TO REVIEW
        ```{language}
        {code}
        ```

        # KNOWLEDGE BASE
        {knowledge_base}

        # REVIEW INSTRUCTIONS
        Please perform a thorough code review, focusing on:

        1. Code Quality:
           - Readability and maintainability
           - Code organization and structure
           - Naming conventions
           - Comments and documentation

        2. Best Practices:
           - Language-specific best practices
           - Design patterns and architectural considerations
           - Performance optimizations

        3. Potential Issues:
           - Bugs and logic errors
           - Security vulnerabilities
           - Edge cases and error handling
           - Resource management

        4. Refactoring Suggestions:
           - Clear, actionable refactoring steps
           - Code examples where appropriate

        # REQUESTED OUTPUT FORMAT
        Please structure your response as follows:

        ## Summary
        [A brief summary of the overall code quality and main issues]

        ## Strengths
        [List the strengths of the code]

        ## Issues and Suggestions
        [Detailed explanation of issues found with specific suggestions for improvement]

        ## Refactoring Steps
        [Step-by-step refactoring instructions with code examples where appropriate]

        ## Final Recommendations
        [Final recommendations and priority order for addressing issues]
        """

        return ChatPromptTemplate.from_template(template).format(
            code=code,
            knowledge_base=formatted_knowledge_base,
            language=language
        )

    def review_code(self, code: str, file_path: Optional[str] = None, knowledge_base: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """Review the provided code and return feedback along with knowledge base metadata."""
        language = get_language_from_extension(file_path) if file_path else "Unknown"
        
        
        if knowledge_base is None:
            knowledge_base = []

        # # Extracting metadata separately for returning in response
        # retrieved_metadata = [item.get("metadata", {}) for item in knowledge_base]
        
        # Extract metadata and similarity score separately for returning in response
        retrieved_metadata = [
            {
                "metadata": item.get("metadata", {}),
                "similarity_score": item.get("similarity_score") if "similarity_score" in item else "N/A"  # Default to 0.0 if missing
            }
            for item in knowledge_base
        ]

        print("\n[DEBUG] Extracted metadata from knowledge base:")
        # Create the review prompt
        prompt_text = self.create_review_prompt(code, knowledge_base, language)

        print("\n[DEBUG] Sending prompt to LLM...")  # Debugging
        
        # Get the review response
        review_result = self.llm.invoke(prompt_text)

        print("\n[DEBUG] LLM Response received.")  # Debugging
        
        return {
            # "review": review_result,
            "content": review_result.content,
            "retrieved_metadata": retrieved_metadata,
            
        }
