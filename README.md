# Local AI Agent with Python, Ollama, LangChain and SingleStore

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

## Step 3: Prepare Your Data

The project uses a CSV file (`pizza_reviews.csv`) containing pizza reviews. The file should have the following columns:
- Title
- Date
- Rating
- Review

## Step 4: Run SingleStore Locally

The Python script will automatically start a SingleStore instance using Docker. Just make sure Docker is running.

## Step 5: Run the Application

Start the application from the command line:
```bash
python3 main.py
```

## Example Usage

Once running, you can ask questions about the pizza reviews. For example:
```
Enter your question about pizza (or 'exit' to quit): What do people think about the crust?
```

The system will:
1. Find relevant reviews using vector similarity search
2. Use the LLaMA model to generate an answer based on those reviews

## Project Structure

```
.
├── README.md
├── requirements.txt
├── main.py
└── pizza_reviews.csv
```

## Dependencies

The project uses the following main dependencies:
- langchain
- langchain-ollama
- langchain-singlestore
- singlestoredb
- pandas
- docker

## Customization

Feel free to experiment with:
* Different LLMs or embedding models via Ollama
* Other datasets
* Custom prompt templates
* Adjusting the number of retrieved reviews (currently set to 2)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

This project is based on the tutorial "Build a Local AI Agent with Python, Ollama, LangChain and SingleStore" by Volodymyr Tkachuk, Engineering Manager at SingleStore. Original tutorial can be found at: [SingleStore Blog](https://www.singlestore.com/blog/build-a-local-ai-agent-python-ollama-langchain-singlestore/).