from pathlib import Path 

directories = [
    "api",
    "chunking",
    "config/logging",
    "config/prompts",
    "config/retrieval",
    "config/models",
    "docs",
    "data/raw",
    "data/processed",
    "data/embeddings",
    "data/cache",
    "embeddings",
    "evaluation",
    "frontend",
    "ingestion",
    "llm",
    "logs",
    "notebooks",
    "preprocessing",
    "retrieval",
    "scripts",
    "services",
    "tests/sample_documents",
    "utils",
    "vector_db"
]

files = [
    "main.py",
    ".env.example",
    "Dockerfile",
    "docker-compose.yml",

    "api/__init__.py",
    "api/routes.py",
    "api/schemas.py",
    "api/dependencies.py",

    "chunking/__init__.py",
    "chunking/chunker.py",
    "chunking/strategies.py",

    "config/__init__.py",
    "config/settings.py",

    "config/logging/__init__.py",
    "config/prompts/__init__.py",
    "config/retrieval/__init__.py",
    "config/models/__init__.py",

    "config/logging/logging_config.py",

    "config/prompts/rag_prompt.py",
    "config/prompts/system_prompt.py",

    "config/retrieval/chunking_config.py",
    "config/retrieval/retrieval_config.py",

    "config/models/embedding_config.py",
    "config/models/llm_config.py",

    "docs/architecture.md",

    "embeddings/__init__.py",
    "embeddings/embedder.py",
    "embeddings/cache.py",

    "evaluation/__init__.py",
    "evaluation/ragas_eval.py",
    "evaluation/benchmark.py",
    "evaluation/metrics.py",

    "frontend/__init__.py",
    "frontend/gradio_app.py",
    "frontend/components.py",

    "ingestion/__init__.py",
    "ingestion/loader.py",
    "ingestion/pipeline.py",

    "llm/__init__.py",
    "llm/generator.py",
    "llm/response_parser.py",

    "preprocessing/__init__.py",
    "preprocessing/ocr.py",
    "preprocessing/tables.py",
    "preprocessing/image_caption.py",
    "preprocessing/metadata.py",
    "preprocessing/cleaner.py",

    "retrieval/__init__.py",
    "retrieval/retriever.py",
    "retrieval/hybrid.py",
    "retrieval/reranker.py",
    "retrieval/query_expansion.py",
    "retrieval/filters.py",

    "scripts/ingest.py",
    "scripts/rebuild_index.py",

    "services/__init__.py",
    "services/chat_service.py",
    "services/ingestion_service.py",
    "services/retrieval_service.py",
    "services/indexing_service.py",

    "tests/test_loader.py",
    "tests/test_chunker.py",
    "tests/test_embedder.py",
    "tests/test_vector_store.py",
    "tests/test_retriever.py",
    "tests/test_api.py",

    "utils/__init__.py",
    "utils/helpers.py",
    "utils/file_utils.py",
    "utils/constants.py",
    "utils/timers.py",

    "vector_db/__init__.py",
    "vector_db/vector_store.py",
    "vector_db/index_manager.py",

    "logs/.gitkeep"
]

ROOT = Path.cwd()

print("=" * 50)
print("Bootstrapping Papermind...")
print("=" * 50)

for directory in directories:
    path = ROOT / directory
    path.mkdir(parents=True, exist_ok=True)

for file in files:
    path = ROOT / file
    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        path.touch()
        print(f"Created: {file}")
    else:
        print(f"Exists : {file}")

print("\nproject structure ready!")