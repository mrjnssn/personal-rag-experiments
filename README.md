# Traceable knowledge engine

A local-first, user-controlled system for ingesting, indexing, retrieving and analysing personal and external information with verifiable, source-traceable outputs.


## Goals

This traceable knowledge engine aims to provide a transparent and user-controlled system for working with personal knowledge and external information.

The main goals are to:
- keep generated answers verifiable by allowing users to trace information back to its original source
- make source inspiection a core part of the user experience rather than an optional debugging feature
- keep personal data local by default
- support both local and external AI models without locking the system to a specific provider
- give users explicit control over actions that affect external systems
- combine personal knowledge with external sources such as the web, news, RSS feeds, and read-only newsletters
- support multiple retrieval strategies, including semantic and lexibal search
- provide a modular architecture in which models, storage, retrieval methods, data sources, and interfaces can be replaced independently
- enable applications such as question answering, research, recommendations, news briefings, and cross-source knowledge discovery


## Design principles

### Privacy first
Personal data should remain local by default. External services should only receive data when explicitly configured and when their use is clear to the user. Local and open-source alternatives should be preferred where possible.

### Verifiability
Generated answers should remain traceable to their underlying sources. Users should be able to inspect the evidence behind an answer and navigate back to the relevant location in the original source whenever possible. Source attribution should be designed as a core system capability, not added only at the presentation layer.

### User control
While the system may automatically read, index, retrieve and analyse information, actions that affect external systems should require explicit user apprival

### Model agnostic
AI models and providers should be interchangeable. Users should be able to choose between local and external models based on their own requirements for privacy, performance, cost and quality.

### Local first
Core functionality should be able to run locally. Local models and open-source components are preferred defaults, while external providers remain optional.

### Transparancy
The system should make its processing steps understandable and inspectable. Users should be able to understand which data sources, retrieval methods, models and external services were involved in producing a result.


## Architecture

This personal knowledge engine is designed as a modular, local-first system. Individual components should be replaceable without requiring major changes to the rest of the application. 

### High-level architecture
```
Data sources
|--- Personal documents
|--- Notes
|--- Books / reading data
|--- Web pages
|--- RSS / news
|--- Read-only email sources
|
Ingestion
|--- Load and parse content
|--- Normalise text
|--- Extract metadata
|--- Detect new, changed, and deleted content
|
Indexing
|--- Chunking
|--- Local embeddings
|--- Vector index
|--- Lexical index
|
Retrieval
|--- Semantic search
|--- BM25 / lexical search
|--- Hybrid result fusion
|--- Optional reranking
|
Application layer
|--- Question answering
|--- Research and synthesis
|--- Recommendations
|--- News briefings
|--- Knowledge discovery
|
Local LLM
|--- Context-based generation (RAG)
|--- Source attribution
|--- Structured output
|
User interface
|--- Search / chat
|--- File upload
|--- Source inspection
|--- Data and index management
```

### Data boundaries

Personal data should remain on the local machine by default.

Local componants handle:
- personal documents and notes
- embeddings
- vector and lexical indexes
- retrieval
- LLM inference
- conversation and application state

External access is used only when required for explicitly configured sources:
- web search
- web pages
- RSS feeds
- news sources
- read-only newsletter or email ingestion

External data may be retrieved and processed locally, but personal data should never be sent to external services unless explicitly configured to do so by the user. 

## Current status

The project currently implements a working RAG pipeline for local text documents.

The current system can:

- Load `.txt` documents from a local directory
- Split documents into paragraph-aware chunks
- Generate embeddings using the OpenAI API
- Store embeddings, text, and metadata in a persistent Chroma vector database
- Retrieve relevant chunks using cosine vector search
- Generate answers based on retrieved context
- Track source filenames, chunk IDs, file content updates (hashes) and embedding model
- Incrementally update the index when documents are added, changed, or removed
- Avoid regenerating embeddings for unchanged documents
- Evaluate retrieval quality using a small test set

The current retrieval evaluation passes 6/6 test questions.

N.B. OpenAI is currently used for both embeddings and text generation. This is a temporary implementation choice; the architecture is intended to support interchangeable local and external model providers.

## Roadmap

### v0.1 - Basic RAG (x)
- load text documents
- split documents into simple chunks
- generate embeddings
- store embeddings in JSON
- impliment cosine similarity search
- generate answers using retrieved context
- add a basic retrievel evaluation set

### v0.2 - Chroma Vector Store (x)
- replace JSON storage with Chroma
- use cosine vector search
- add persistent storage
- implement incremental indexing
- detect new, changed and deleted documents

### v0.3 - Hybrid search / retrieval
- add lexical search using BM25
- combine lexical and semantic search
- experiment with result fusion and ranking
- improve source attribution
- expand the retrieval evaluation set
- compare vector, BM25, and hybrid retrieval

### v0.4 = Data ingestion
- support additional document formats
- add web page ingestion
- add RSS/news ingestion
- preserve useful source metadata
- explore read-only email/newsletter ingestion

### v0.5 - User interface
- add a simple file upload interface
- add conversational search
- display retrieved sources and metadata
- make indexing and data management visible to the user

### v0.6 - Local & private models
- replace cloud embeddings with a local embedding model
- run an open-source LLM locally
- ensure personal documents can be indexed and queried without leaving the machine
- keep model-specific logic isolated from the RAG pipeline
- make provider selection configurable
- keep external providers optional

### Future
- personalised book and content recommendations
- AI / tech news briefings
- research dossiers
- cross-source knowledge discovery
- personal notes and idea resurfacing
- reranking
