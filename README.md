# Classroom Project RAG POC

A complete Retrieval-Augmented Generation (RAG) system for querying a Provider Manual, built with **LangChain**, **Streamlit**, **PostgreSQL**, and **ChromaDB**.

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- OpenAI API Key

### 1. Configuration
Copy the example environment file:
```bash
cp env.example .env
```
Edit `.env` and set your `OPENAI_API_KEY`:
```ini
OPENAI_API_KEY=sk-your-key-here
# Optional: Adjust embedding model or DB creds if needed
```

### 2. Run with Docker (Recommended)
Build and start the services:
```bash
docker-compose up --build
```
> This will start:
> - **Postgres**: For chat history
> - **ChromaDB**: For vector storage
> - **Streamlit App**: The user interface

The application will be available at [http://localhost:8501](http://localhost:8501).

---

## 📂 Data Ingestion

The system automatically checks for data ingestion on startup. 

### Manual Ingestion
If you need to re-ingest data or add new files while the container is running:

1. Place your PDF file in `data/provider_manual.pdf`.
2. Run the ingestion script inside the container:
   ```bash
   docker-compose exec app python scripts/run_ingestion.py
   ```

---

## 🧪 Testing

The repository includes a comprehensive test suite covering unit logic, integration flows, and quality evaluations.

### Running Tests
Run the tests inside the container to ensure connectivity to the database services:

```bash
docker-compose exec app pytest
```

### Test Structure
| Type | Path | Purpose |
|------|------|---------|
| **Unit** | `tests/unit/` | Tests individual components (LLM wrapper, Embedding wrapper) using mocks. |
| **Integration** | `tests/integration/` | Tests complete pipelines (Ingestion, Query) ensuring components wire together correctly. |
| **Evaluation** | `tests/eval/` | Quality checks for retrieving relevant context and generating faithful answers. |

---

## 🏗 Architecture

### Tech Stack
- **Framework**: [LangChain](https://www.langchain.com/) (Orchestration)
- **Frontend**: [Streamlit](https://streamlit.io/)
- **LLM**: OpenAI GPT-4o
- **Embeddings**: SentenceTransformers (`all-MiniLM-L6-v2`) running via HuggingFace
- **Vector Store**: [ChromaDB](https://www.trychroma.com/) (Client-Server mode)
- **Database**: PostgreSQL (Session & Chat History)
- **Infrastructure**: Docker Compose

### Project Structure
```
├── app/                  # Streamlit frontend & state management
├── db/                   # Database models & SQL schema
├── pipelines/            # LangChain pipelines (Ingestion, Query)
├── utils/                # Core utilities (LLM, Embeddings, Config)
├── tests/                # Unit, Integration, and Eval tests
├── docker/               # Dockerfile & Entrypoint scripts
├── data/                 # Raw PDF data
└── scripts/              # Standalone execution scripts
```
