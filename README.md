# RAG System for Provider Manual

A Retrieval-Augmented Generation (RAG) system that processes a healthcare provider manual PDF and provides an interactive chat interface for answering questions about the document.

## Features

- PDF document ingestion and text chunking
- Vector embeddings for semantic search
- Streamlit-based chat interface
- Source citations with page references
- Local ChromaDB vector storage
- OpenAI GPT-4 integration

## Prerequisites

- Python 3.11+
- OpenAI API key
- Docker (optional)
- Postgres (https://www.postgresql.org/download/)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/WhiteboxHub/classroom-project-rag-poc
   cd classroom-project-rag-poc
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables(create .env file in the root directory):
   ```bash
# ===============================
# App Mode
# ===============================
USE_LOCAL_DB=true

# ===============================
# LLM Provider (Free Mode)
# ===============================
LLM_PROVIDER=openai

# ===============================
# OpenAI Configuration
# ===============================
OPENAI_API_KEY=your-api-key
OPENAI_MODEL_NAME=gpt-4o

# ===============================
# Alternative LLM Provider (Groq)
# Uncomment to use
# ===============================
# LLM_PROVIDER=groq
# GROQ_API_KEY=your-groq-api-key
# GROQ_MODEL_NAME=meta-llama/llama-4-scout-17b-16e-instruct

# ===============================
# Embeddings (Free & Local)
# ===============================
EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2

# ===============================
# ChromaDB (Local Persistent)
# ===============================
CHROMADB_HOST=localhost
CHROMADB_PORT=8000
COLLECTION_NAME=rag_collection

# ===============================
# Chunking Configuration
# ===============================
CHUNK_SIZE=800
CHUNK_OVERLAP=150

# ===============================
# Logging
# ===============================
LOG_LEVEL=INFO

# ===============================
# Database (Local PostgreSQL)
# ===============================
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=rag_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# ===============================
# AWS (Optional – Not Used Currently)
# ===============================
# AWS_ACCESS_KEY_ID=
# AWS_SECRET_ACCESS_KEY=
# AWS_REGION=us-east-1
   ```

## Usage

### Local Development

1. Initialize the database:
   ```bash
   python -c "from db.models import init_db; init_db()"
   ```

2. Run document ingestion:
   ```bash
   python scripts/run_ingestion.py
   ```

3. Start the application:
   ```bash
   python -m streamlit run app/streamlit_app.py
   ```

4. Open your browser to `http://localhost:8501`

### Docker

1. Build and run with Docker Compose:
   ```bash
   docker compose up --build
   ```

2. Access the application at `http://localhost:8501`

## Project Structure

- `app/` - Streamlit application
- `pipelines/` - Data processing pipelines
- `utils/` - Utility modules
- `db/` - Database models and schemas
- `scripts/` - Setup and utility scripts
- `tests/` - Unit and integration tests
- `data/` - Document storage
- `prompts/` - System prompts

## Configuration

Edit the `.env` file to configure:
- OpenAI API key
- Database settings
- Chunking parameters
- Embedding model

## Testing

Run tests with:
```bash
pytest tests/
```

## Technologies

- LangChain
- ChromaDB
- SentenceTransformers
- OpenAI GPT-4
- Streamlit
- SQLAlchemy
