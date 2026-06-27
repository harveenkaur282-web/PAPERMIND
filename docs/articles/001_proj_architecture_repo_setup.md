# Building Papermind #001 (Project Foundations) Phase 0, part 1- Architecture and Repository design

This is not an article, or a tutorial, it's actually my project's first engineering log. I will be continuing this for next 4-5 months, rigorous building first three months and then optimizations. This is not for you, it's mainly so that I can come back to these articles when I have interviews about AI system designing-python related basically. So I'll be building an end-to-end AI application that starts as a standard RAG system and gradually evolves into an agentic research assistant/companion.

I want to document or remember every architectural decision I made, every mistake, every small detail, and every challenge I encountered while doing this project. If well, someone finds it useful, cuz I'm a total beginner by the way- a third year undergrad right now so yeah, it'll be a bonus. Some things/decisions might change along the way, that's the part of the learning process.

So here's DAY 1. No polished demo/article, no perfection, but mistakes, why i did this, and just the foundations cuz I want to understand building an actual retrieval system without all those agentic frameworks for now. Just praying I show up every day. Also this is so that there is an automatic jounal created, like rag about my journals too when I would link this with my github repo, I would be able to ask what did I do during this phase, why did I do it so it's mainly for future me.

## What is PaperMind?

Papermind is an end-to-end AI research assistant that I will be building over the next few months. Instead of starting with a complex multi-agent architecture, I'll begin with a standard Retrieval-Augmented Generation (RAG) system and gradually evolve it into an agentic research companion.

Problem statement- So there are thousands of arXiv papers, blog posts, AI news, documentation, info is everywhere but there is nothing structured, existing LLMs can answer questions about research papers, but my goal isn't simply to consume them. I want to understand how an end-to-end retrieval system is designed and implemented from scratch. I myself wanna keep up with everything AI but I sometimes get so overwhelmed that I get anxiety, no seriously.

So this starts out as standard RAG system where the there will be prebuilt rag corpus of research papers and the user can ask questions about it. Its primary purpose is to **retrieve, ground, and synthesize information from research papers**. It's a domain-specific AI system. So, for now- three versions.

V1: AI research assistant- A standard rag- arXiv papers, question answering, summarizations, citations

**Although the long-term goal is to support AI research papers, blog posts, documentation, AI news, and user-uploaded content, Version 1 focuses only on building a robust retrieval system over a curated collection of arXiv papers.**

V2: Bring your own paper version, user uploads pdfs.

V3: Knowledge Hub version, AI news articles, AI blogs, documentation, user uploaded pdfs, agentic RAG, multi-agent workflows, better retrieval, memory, planning.

## Project Setup Foundations:

## Architecture diagram:

Starting with setting up the infrastructure: repo folders and files. I'll be talking about the structure, configuration, settings, logging, dependency management, backend setup.

This is the simple project structure (for now) :

![](https://cdn.hashnode.com/uploads/covers/6a3fc30c862274b71e9523b9/3cb89a99-c0ef-47a9-b4b1-53d378117e44.png align="center")

This is a rough setup, might change later. One realization I had while designing Papermind was that a RAG system isn't a single pipeline. It's actually two separate systems. The indexing pipeline prepares the knowledge base before users interact with it, while the query pipeline runs every time a user asks a question.

So the offline pipeline is when the knowledge base of a curated collection of AI arXiv research papers we have, this pipeline will be executed once and when I would add new papers, or I want to rebuild index, or update embeddings.

Online pipeline- It runs for everytime when the user asks a question.

Both pipelines are independent but communicate through a shared vector database. The offline pipeline writes knowledge into the vector database, while the online pipeline only reads from it.

### Repository Structure:

![](https://cdn.hashnode.com/uploads/covers/6a3fc30c862274b71e9523b9/415d0b76-bedf-405c-acc4-726cb31552ca.png align="center")

Initially, I imagined a user asking a question, the system retrieving information, and the LLM answering it. However, after designing the project structure with the help of a linkedin article as well as confirming with chatgpt about this so that it suits my problem, I realized that there are actually **two completely independent workflows** that share a common vector database.

The first workflow is for **building the knowledge base**, while the second workflow is for **using that knowledge base to answer user questions**. Once I understood this separation, every folder in the repository suddenly made sense.

Since these pipelines run at completely different times, I decided to explain them separately.

### 1\. Online Query Pipeline (Runs Every Time a User Asks a Question)

This is the pipeline that powers the research assistant. Every user question follows this path.

The journey begins in `frontend/gradio_app.py`, where the user types a question. At this stage, the frontend is only responsible for collecting user input and displaying the final response. It contains no retrieval or LLM logic.

The question is then sent as an HTTP request to the FastAPI backend. The application itself is initialized in `main.py`, which creates the FastAPI application, loads configuration, registers API routes, initializes logging, and starts the server through Uvicorn. Command used: uv run uvicorn main:app --reload

The request reaches `api/routes.py`, where the corresponding endpoint receives the incoming request. Before any processing occurs, the request body is validated (Request validation) using the Pydantic models defined inside `api/schemas.py`.

For ex- like in case the user entered 12345 instead of a string query like "What is transformer?"

These schemas ensure that the request follows the expected format and prevent invalid data from entering the application. Any dependencies required by the routes, such as shared services or authentication in future versions, are managed through `api/dependencies.py`.

An important architectural decision is that the API layer never contains business logic. Instead, the validated query is forwarded to `services/chat_service.py`, which acts as the orchestrator for the entire online workflow.

The responsibility of `chat_service.py` is not to retrieve information or call the LLM directly, but rather to coordinate the different modules. It first sends the user's query to the retrieval module.

Inside `retrieval/retriever.py`, the retrieval process begins. The retriever itself does not generate embeddings. Instead, it calls `embeddings/embedder.py`, which converts the user's question into a dense vector representation using the configured embedding model.

The embedding model to use, its dimensions, batch size, and related settings are stored separately inside `config/models/embedding_config.py`, ensuring that changing models requires configuration updates rather than code modifications.

Once the query embedding has been generated, the retriever communicates with `vector_db/vector_store.py`, which serves as the abstraction layer over the chosen vector database (such as FAISS or ChromaDB). The vector database performs similarity search and returns the most relevant document chunks.

The retriever may optionally perform additional retrieval enhancements depending on the configuration:

1.  `retrieval/hybrid.py` combines dense retrieval with keyword-based retrieval such as BM25.
    
2.  `retrieval/query_expansion.py` expands or rewrites the user's query to improve retrieval quality.
    
3.  `retrieval/filters.py` applies metadata-based filtering, such as restricting results to papers from a particular year, author, or research area.
    
4.  `retrieval/reranker.py` reranks the retrieved chunks using a stronger cross-encoder model to improve relevance before passing them to the LLM.
    

The behaviour of these retrieval strategies is controlled by configuration files inside `config/retrieval/`, including `retrieval_config.py` and `chunking_config.py`.

After retrieval is complete, the retriever returns the top-k document chunks back to `services/chat_service.py`.

At this point, the chat service now possesses two pieces of information:

1.  the original user question
    
2.  the retrieved contextual chunks
    

The chat service forwards both to `llm/generator.py`.

The generator is responsible for constructing the final prompt. Rather than hardcoding prompts directly inside Python files, prompt templates are maintained separately inside `config/prompts/`, including files such as `system_prompt.py` and `rag_prompt.py`. This separation makes prompt engineering independent of application logic.

The LLM model configuration itself is stored inside `config/models/llm_config.py`, allowing the application to switch between local models or API providers without modifying the generation logic.

After constructing the prompt, `generator.py` calls the selected language model and receives the generated response. If any post-processing or structured parsing is required, `llm/response_parser.py` performs that work before returning the final answer.

Finally, `chat_service.py` sends the completed response back to `api/routes.py`, which returns the JSON response to FastAPI. FastAPI sends it back to `frontend/gradio_app.py`, where the answer is displayed to the user.

Throughout this entire process, `config/settings.py` provides environment-based configuration, while `config/logging/logging_config.py` records logs into `logs/app.log`. Utility functions from `utils/helpers.py`, `utils/file_utils.py`, `utils/constants.py`, and `utils/timers.py` may be used wherever common functionality is required without duplicating code.

### 2\. Offline Indexing Pipeline (Runs Only When Building or Updating the Knowledge Base)

Unlike the online pipeline, the offline pipeline is never triggered by a user question. Instead, it prepares the knowledge base before users interact with the system.

The process typically begins by running `scripts/ingest.py`. This script starts the indexing workflow and delegates the work to `services/ingestion_service.py` or `services/indexing_service.py`, which coordinate the indexing process.

Raw research papers are first stored inside `data/raw/`.

The documents are loaded using `ingestion/loader.py`, which is responsible for reading supported document formats such as PDF, DOCX, or TXT. If multiple loading stages are required, `ingestion/pipeline.py` coordinates them.

The extracted content is then passed into the preprocessing stage.

Inside `preprocessing/cleaner.py`, unnecessary formatting, whitespace, and noisy text are removed.

If scanned PDFs are encountered, `preprocessing/ocr.py` performs optical character recognition.

If research papers contain tables, `preprocessing/tables.py` extracts structured table content.

Images within papers can be processed through `preprocessing/image_caption.py`, while `preprocessing/metadata.py` extracts metadata such as title, authors, publication year, categories, or other useful filtering information.

The cleaned document is then forwarded to `chunking/chunker.py`, which divides the document into smaller chunks suitable for retrieval. Different chunking strategies, including recursive, semantic, or fixed-size chunking, are implemented inside `chunking/strategies.py`.

The resulting chunks are passed to `embeddings/embedder.py`, which converts every chunk into a dense vector representation using the configured embedding model. During indexing, the embedder may also utilize `embeddings/cache.py` to avoid recomputing embeddings for unchanged documents.

These chunk embeddings are then stored inside the vector database through `vector_db/vector_store.py`, while `vector_db/index_manager.py` manages index creation, rebuilding, persistence, or loading. The physical vector index becomes the application's searchable knowledge base.

Processed versions of the documents may be stored inside `data/processed/`, while temporary intermediate files can be placed inside `data/cache/`.

Whenever the knowledge base needs to be rebuilt, `scripts/rebuild_index.py` rerun the entire indexing pipeline.

### 3\. Supporting Infrastructure

Several parts of the repository support both pipelines rather than belonging to only one.

The `config/` directory centralizes all configuration, including environment variables, model settings, prompt templates, retrieval parameters, and logging configuration.

The `tests/` directory contains unit tests for individual modules such as document loading, chunking, embedding generation, retrieval, vector storage, and API endpoints. Sample documents used for testing are stored inside `tests/sample_documents/`.

The `evaluation/` directory is responsible for measuring the quality of the RAG system after it has been built. This includes retrieval metrics, benchmarking, and RAGAS-based evaluation to assess answer quality.

The `docs/` directory stores project documentation, architecture notes, and future design decisions.

The `notebooks/` directory serves as a workspace for experiments, prototypes, and exploratory analysis without affecting the production codebase.

Finally, `project_setup.py` bootstraps the project structure during development, while `pyproject.toml`, `uv.lock`, Docker files, environment files, and the README manage dependencies, reproducibility, containerization, and project documentation.

### Questions I still have:

*   How will I automatically collect and maintain a corpus of AI research papers? Should I use the arXiv API, Semantic Scholar, or manually curate papers initially?
    
*   How many papers should Version 1 realistically index? Is 100 enough to demonstrate the system, or should I start with fewer?
    
*   If I index 100 papers, will the embedding model struggle? Does embedding time or memory become a bottleneck?
    
*   Where should I store metadata such as authors, publication dates, categories, and arXiv IDs so that I can later implement metadata filtering?
    
*   Should I embed every paper from scratch whenever I add a new one, or only embed newly added documents and append them to the existing vector database?
    
*   When should I rebuild the entire vector index, and when can I simply update it incrementally?
    

### Conclusion:

This article focused only on the architectural foundation of Papermind. At this stage, the goal was to understand how the different modules communicate before writing the retrieval logic itself. I have started coding files like config/logging/logging\_config.py, env file that contains app name, version, host, port and log level which are verfied using Pydantic settings in config/settings.py, [main.py](http://main.py) has a functional fastapi application working. The learnings and challenges faced regarding this will be told in the next article. Thankyou!

If you'd like to follow along, then this is my repo: [harveenkaur282-web/PAPERMIND: Major project](https://github.com/harveenkaur282-web/PAPERMIND)

**Next Log:** Project Foundations – Part 2 (project\_setup.py, generate\_tree.py, uv, pyproject.toml, Pydantic Settings, configs folder, env, FastAPI, Uvicorn, Loguru, logs folder, initialization of docker files, async programming, git commits practice and the backend setup.)