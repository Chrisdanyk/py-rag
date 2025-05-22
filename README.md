# Local AI Agent with Python, Ollama, LangChain and SingleStore

A local RAG (Retrieval-Augmented Generation) system that uses Ollama for LLMs, LangChain for orchestration, and SingleStore for vector storage. Built with Python, this project demonstrates how to create a Q&A system that runs entirely on your local machine, perfect for experimenting with AI without cloud dependencies.

This project demonstrates how to build a local Retrieval-Augmented Generation (RAG) AI agent using Python. The agent runs entirely on your machine and leverages:

* **Ollama** for open-source LLMs and embeddings
* **LangChain** for orchestration
* **SingleStore** as the vector store

By the end we'll have a working Q&A system powered by the local data and models.

## Prerequisites

Ensure the following are installed and configured:

* Docker (running)
* Python 3.9+
* Ollama installed and working

## Step 1: Set up Ollama

1. Visit [ollama.com](https://ollama.com) and download the installer for your OS
2. Follow the on-screen instructions
3. Download the required models by running:
   ```bash
   ollama serve
   ollama pull llama3
   ollama pull mxbai-embed-large
   ```

## Step 2: Set up Python Environment

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Step 3: Prepare Your Code Repository

The project can work with any code repository or directory containing code files. Supported file extensions include:
- Python (.py)
- JavaScript (.js, .jsx)
- TypeScript (.ts, .tsx)
- Java (.java)
- C/C++ (.c, .cpp, .h, .hpp)
- C# (.cs)
- Go (.go)
- Rust (.rs)

## Step 4: Run SingleStore Locally

The Python script will automatically start a SingleStore instance using Docker. Just make sure Docker is running.

## Step 5: Run the Application

Start the application from the command line:
```bash
python3 main.py
```

When prompted, enter the path to your code repository or directory.

## Example Usage

Once running, you can ask questions about the code. For example:
```
Enter your question about the code (or 'exit' to quit): How is the database connection handled?
```

The system will:
1. Find relevant code snippets using vector similarity search
2. Use the LLaMA model to generate an answer based on those snippets

## Project Structure

```
.
├── README.md
├── requirements.txt
├── main.py
└── LICENSE
```

## Dependencies

The project uses the following main dependencies:
- langchain
- langchain-ollama
- langchain-singlestore
- singlestoredb
- docker

## Customization

Feel free to experiment with:
* Different LLMs or embedding models via Ollama
* Other code repositories or directories
* Custom prompt templates
* Adjusting the number of retrieved code snippets (currently set to 3)
* Adding support for more file types

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

This project is based on the tutorial "Build a Local AI Agent with Python, Ollama, LangChain and SingleStore" by Volodymyr Tkachuk, Engineering Manager at SingleStore. Original tutorial can be found at: [SingleStore Blog](https://www.singlestore.com/blog/build-a-local-ai-agent-python-ollama-langchain-singlestore/)

The code has been adapted to use pip and requirements.txt instead of Poetry for dependency management, and modified to work with code repositories instead of pizza reviews.