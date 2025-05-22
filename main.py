import os
from pathlib import Path

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_singlestore import SingleStoreVectorStore
from singlestoredb.server import docker


def setup_database(s2db):
    """Initialize the SingleStore database."""
    with s2db.connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS testdb")


def load_code_documents(directory_path):
    """Load code files from a directory and convert to Document objects."""
    documents = []
    code_extensions = {'.py', '.js', '.java', '.cpp', '.c',
                       '.h', '.hpp', '.cs', '.go', '.rs', '.ts', '.jsx', '.tsx', '.prisma'}

    # Directories to exclude
    exclude_dirs = {
        'venv', 'env', '.venv', '.env',  # Python virtual environments
        'node_modules',  # Node.js dependencies
        '.git',  # Git repository
        '__pycache__', '.pytest_cache',  # Python cache
        'build', 'dist',  # Build directories
        '.idea', '.vscode',  # IDE settings
        'target',  # Rust/Java build
        '.mypy_cache',  # Python type checking
    }

    for root, dirs, files in os.walk(directory_path):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for file in files:
            file_path = Path(root) / file
            if file_path.suffix in code_extensions:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Create a relative path for better readability
                        rel_path = os.path.relpath(file_path, directory_path)
                        # Use a hash of the file path as the ID to ensure uniqueness
                        doc_id = str(hash(rel_path))
                        documents.append(
                            Document(
                                page_content=content,
                                metadata={
                                    "file_path": rel_path,
                                    "file_type": file_path.suffix,
                                    "file_name": file_path.name
                                },
                                id=doc_id
                            )
                        )
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    return documents


def main():
    """
    Run a code repository Q&A application using SingleStoreDB vector store and LLaMA.

    This example demonstrates:
    1. Setting up a vector database with SingleStoreDB
    2. Embedding code files with Ollama
    3. Creating a retrieval-based QA system that answers questions about code
    """
    print("Starting SingleStoreDB server for vector storage...")
    with docker.start(license="") as s2db:
        setup_database(s2db)

        # Get the directory path from user input
        directory_path = input(
            "\nEnter the path to your code repository or directory: ").strip()
        if not os.path.exists(directory_path):
            print(f"Error: Directory '{directory_path}' does not exist.")
            return

        print(f"\nLoading and embedding code files from {directory_path}...")
        documents = load_code_documents(directory_path)
        if not documents:
            print("No code files found in the specified directory.")
            return

        print(f"Found {len(documents)} code files.")
        embedding = OllamaEmbeddings(model="mxbai-embed-large")

        # Set up vector store with the embedded documents
        vector_store = SingleStoreVectorStore(
            embedding=embedding,
            host=s2db.connection_url,
            database="testdb",
            table_name="code_documents",
        )
        vector_store.add_documents(documents)

        # Create retriever that fetches the 3 most relevant code snippets for each query
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})

        print("Initializing LLaMA 3.2 model...")
        model = OllamaLLM(model="llama3.2")

        # Define prompt template with clean formatting
        template = """
You are an expert in answering questions about code.

Here are some relevant code snippets: {reviews}

Here is the question: {question}

Please provide a detailed answer based on the code snippets above. If the code snippets don't contain enough information to answer the question, please say so.
"""
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | model

        print("\n------------------------------------------")
        print("Code Repository Question & Answer System")
        print(
            "Ask questions about the code, and the system will find relevant code snippets")
        print("and generate an answer based on those snippets.")
        print("------------------------------------------\n")

        while True:
            user_input = input(
                "\nEnter your question about the code (or 'exit' to quit): ")
            if user_input.lower() == "exit":
                break
            print("\nFinding relevant code snippets and generating answer...")
            reviews = retriever.invoke(user_input)
            result = chain.invoke({"reviews": reviews, "question": user_input})

            print("\n--- Answer ---")
            print(result)


if __name__ == "__main__":
    main()
