# supply-chain-intelligence-platform

## Agentic Supply Chain Intelligence & Operations Platform

The **supply-chain-intelligence-platform** is a production-oriented AI platform designed to investigate supply-chain problems, retrieve trusted operational knowledge, analyze relationships between supply-chain entities, generate recommendations, and support operational workflows.

The platform is being developed incrementally, starting with a reliable data and API foundation before introducing RAG, knowledge graphs, multi-agent workflows, forecasting, conversational interfaces, evaluation, observability, and production hardening.

---

# Project Goal

The goal is to build an AI copilot that can answer operational questions such as:

> "Why is order ORD-10482 delayed?"

Instead of relying only on an LLM, the system combines:

* Structured operational data
* Retrieval-Augmented Generation (RAG)
* Embeddings and vector search
* Knowledge graphs
* Multi-agent workflows
* Deterministic business rules
* Statistical and machine-learning models
* Tool calling
* Structured outputs
* Human approval
* Evaluation and observability

The intended architecture is:

```text
                         User
                           │
                           ▼
                Conversational Interface
                           │
                           ▼
                    FastAPI Gateway
                           │
                           ▼
                  LangGraph Supervisor
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
        Data Agent     RAG Agent     Graph Agent
             │             │             │
             ▼             ▼             ▼
        PostgreSQL       Qdrant        Neo4j
             │             │             │
             └─────────────┼─────────────┘
                           │
                           ▼
                 Recommendation Agent
                           │
                           ▼
                    Human Approval
                           │
                           ▼
                     Workflow Tools
                           │
                           ▼
                         Action
```

---

# What Does This Platform Actually Do?

Imagine a supply-chain manager asks:

> "Why is order ORD-10482 delayed?"

The system does not simply ask an LLM to guess the answer.

Instead, it investigates the problem using multiple trusted sources:

1. PostgreSQL checks the order and shipment data.
2. The RAG system retrieves relevant supplier policies and SOPs.
3. The future knowledge graph analyzes relationships between the order, supplier, shipment, product, and warehouse.
4. Business rules identify operational conditions.
5. ML models can provide predictions where required.
6. AI agents coordinate the investigation.
7. The system produces a structured recommendation.
8. High-impact operational actions can require human approval.
9. The investigation and execution can be evaluated and monitored.

In simple terms:

```text
Data
  ↓
Investigation
  ↓
Evidence
  ↓
Recommendation
  ↓
Human Approval
  ↓
Action
```

---

# Current Progress

## Milestone 1 — Supply Chain Data & Backend Foundation

**Status: Completed**

Milestone 1 establishes the backend and data foundation required by the future AI-agent system.

### Implemented

* FastAPI application
* Uvicorn development server
* Pydantic response schemas
* Pydantic Settings configuration
* Environment-based configuration
* Application logging
* SQLAlchemy ORM
* PostgreSQL database
* Database session management
* Database initialization
* Synthetic supply-chain dataset generation
* CSV dataset generation
* PostgreSQL data seeding
* Order APIs
* Inventory APIs
* Supplier APIs
* Shipment APIs
* Pagination
* Filtering
* 404 error handling
* Service layer
* Automated API tests

---

# Supply Chain Data Model

The current operational dataset contains:

## Suppliers

50 synthetic supplier records.

Fields include:

* Supplier code
* Supplier name
* Location
* Reliability score

## Inventory

150 synthetic inventory records.

Fields include:

* Product SKU
* Warehouse
* Current stock
* Reorder point

## Orders

1,000 synthetic order records.

Fields include:

* Order number
* Customer
* Product SKU
* Quantity
* Order status

## Shipments

1,000 synthetic shipment records.

Fields include:

* Shipment number
* Order number
* Supplier code
* Shipment status
* Expected delivery date

The dataset is synthetic and intended for development, testing, demonstrations, and AI-agent evaluation.

---

# Deterministic Investigation Scenario

A known investigation scenario has been created around:

```text
ORD-10482
```

The scenario connects multiple operational entities:

```text
Order
  ↓
Shipment
  ↓
Supplier

Order
  ↓
Product SKU
  ↓
Inventory
```

Current scenario:

```text
Order:

ORD-10482
Status: delayed
Quantity: 445
Product: SKU-0077

Shipment:

SHIP-20482
Status: delayed
Expected delivery: 2026-09-16

Supplier:

SUP-017
Reliability score: 62.5
Location: Pune

Inventory:

SKU-0077
Warehouse: Mumbai
Current stock: 35
Reorder point: 250
```

This deterministic scenario will later be used to evaluate whether the AI system can correctly investigate a supply-chain issue using multiple data sources.

---

# API Endpoints

## Health

```text
GET /health
```

## Orders

```text
GET /orders
GET /orders/{order_number}
GET /orders?status=delayed
GET /orders?skip=0&limit=20
```

## Inventory

```text
GET /inventory
GET /inventory/{product_sku}
GET /inventory?low_stock=true
GET /inventory?warehouse=Mumbai
```

## Suppliers

```text
GET /suppliers
GET /suppliers/{supplier_code}
```

## Shipments

```text
GET /shipments
GET /shipments/{shipment_number}
GET /shipments?status=delayed
```

## RAG

```text
POST /rag/search
```

---

# Architecture

Milestone 1 currently follows:

```text
Client / Swagger
       ↓
FastAPI API Layer
       ↓
Service Layer
       ↓
SQLAlchemy
       ↓
PostgreSQL
```

The RAG architecture introduced in Milestone 2 follows:

```text
Client
  ↓
FastAPI RAG API
  ↓
Knowledge Search Service
  ↓
Retriever
  ↓
Qdrant
  ↓
Reranker
  ↓
Knowledge Results
```

This separation allows future agents and tools to reuse the service layer instead of duplicating database or retrieval logic.

---

# Project Structure

```text
supply-chain-intelligence-platform/

│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── logging.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── health.py
│   │   ├── orders.py
│   │   ├── inventory.py
│   │   ├── suppliers.py
│   │   ├── shipments.py
│   │   └── rag.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   ├── session.py
│   │   ├── init_db.py
│   │   └── seed_data.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── schemas.py
│   │   └── database_models.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── order_service.py
│   │   ├── inventory_service.py
│   │   ├── supplier_service.py
│   │   └── shipment_service.py
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── supervisor.py
│   │   ├── data_agent.py
│   │   ├── rag_agent.py
│   │   ├── graph_agent.py
│   │   └── recommendation_agent.py
│   │
│   ├── graph/
│   │   ├── __init__.py
│   │   ├── neo4j_client.py
│   │   └── queries.py
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── ingestion.py
│   │   ├── chunking.py
│   │   ├── embeddings.py
│   │   ├── qdrant_client.py
│   │   ├── qdrant_store.py
│   │   ├── retriever.py
│   │   ├── reranker.py
│   │   ├── search_service.py
│   │   ├── dependencies.py
│   │   └── pipeline.py
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── order_tools.py
│   │   ├── inventory_tools.py
│   │   ├── supplier_tools.py
│   │   └── workflow_tools.py
│   │
│   ├── workflows/
│   │   ├── __init__.py
│   │   └── supply_chain_graph.py
│   │
│   ├── evaluation/
│   │   ├── __init__.py
│   │   ├── evaluation_metrics.py
│   │   ├── rag_eval.py
│   │   └── agent_eval.py
│   │
│   └── observability/
│       ├── __init__.py
│       ├── tracing.py
│       ├── llm_traces.py
│       ├── agent_execution.py
│       ├── tool_calls.py
│       ├── latency.py
│       ├── errors.py
│       └── request_ids.py
│
├── data/
│   ├── orders.csv
│   ├── inventory.csv
│   ├── suppliers.csv
│   └── shipments.csv
│
├── knowledge_base/
│   ├── supplier_sla/
│   ├── sop/
│   └── policies/
│
├── tests/
│   ├── api/
│   ├── agents/
│   ├── rag/
│   ├── tools/
│   ├── graph/
│   ├── workflows/
│   ├── services/
│   └── observability/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# Testing

Milestone 1 includes automated API tests using pytest.

The test suite covers:

* Order retrieval
* Missing order handling
* Delayed-order filtering
* Inventory retrieval
* Missing inventory handling
* Low-stock filtering
* Supplier retrieval
* Missing supplier handling
* Shipment retrieval
* Missing shipment handling
* Health endpoint

Milestone 2 significantly expanded the test suite to cover the RAG pipeline and observability.

Run the complete test suite with:

```bash
pytest -v
```

Current test result:

```text
88 passed
```

---

# Technology Stack

## Current

* Python
* FastAPI
* Uvicorn
* Pydantic
* Pydantic Settings
* SQLAlchemy
* PostgreSQL
* psycopg2
* Sentence Transformers
* all-MiniLM-L6-v2
* Qdrant
* Docker
* pytest
* RAG
* Semantic Retrieval
* Deterministic Reranking
* Request ID Tracking
* Latency Tracking
* Error Tracking

## Planned

* Neo4j
* LangChain
* LangGraph
* LLM Integration
* Multi-Agent Workflow
* Forecasting / Machine Learning
* Tool Calling
* Structured Outputs
* Human Approval
* Web Conversational Interface
* WhatsApp Integration
* CI/CD
* Production Deployment

---

# Milestone Roadmap

## Milestone 1 — Data & Backend Foundation

**Status: Completed**

```text
FastAPI
PostgreSQL
SQLAlchemy
Data Generation
Data APIs
Service Layer
Testing
```

## Milestone 2 — RAG Knowledge System

**Status: Completed**

Implemented:

* Document ingestion
* Document chunking
* Sentence Transformer embeddings
* Qdrant vector database
* Semantic retrieval
* Deterministic reranking
* RAG search service
* FastAPI RAG API
* Request IDs
* Latency tracking
* Error tracking
* RAG evaluation foundation
* Automated testing

**Test Result: 88 passed**

## Milestone 3 — Knowledge Graph

**Status: Planned**

```text
Orders
Suppliers
Products
Warehouses
Shipments
       ↓
     Neo4j
       ↓
Relationship-Based Investigation
```

## Milestone 4 — LangGraph Multi-Agent System

**Status: Planned**

```text
Supervisor
    ↓
Data Agent
RAG Agent
Graph Agent
Recommendation Agent
```

## Milestone 5 — Intelligence & Conversational Workflow

**Status: Planned**

* Forecasting
* Recommendation engine
* Structured outputs
* Tool calling
* Human approval
* Web chat
* WhatsApp workflow

## Milestone 6 — Production Hardening, Evaluation & Deployment

**Status: Planned**

* End-to-end AI evaluation
* RAG evaluation
* Agent evaluation
* LLM tracing
* Agent execution tracing
* Tool-call monitoring
* Structured logging
* Metrics and alerting
* Security hardening
* Authentication and authorization
* Rate limiting
* Database migrations
* Health and readiness checks
* Docker production setup
* CI/CD
* Deployment
* Documentation

---

# Engineering Principles

The platform is designed around several principles.

## Use deterministic logic when deterministic logic is enough

Not every supply-chain decision needs an LLM.

Business rules should be preferred when a problem can be solved reliably using deterministic logic.

## Use ML when prediction is required

Forecasting and predictive problems can use statistical or machine-learning models.

## Use RAG for trusted knowledge

Policies, SOPs, supplier SLAs, and operational documentation should be retrieved from controlled sources.

## Use agents for multi-step investigation

Agents will coordinate tools and data sources when a question requires multiple reasoning steps.

## Keep humans in control of high-impact actions

Operational actions can require explicit human approval before execution.

## Evaluate continuously

The system will progressively measure:

* Retrieval quality
* Answer quality
* Groundedness
* Agent behavior
* Tool execution
* Recommendation quality
* Workflow quality
* Latency
* Errors

---

# Development

Create a virtual environment:

```bash
python -m venv .venv
```

## Windows

```powershell
.venv\Scripts\Activate.ps1
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Initialize Database

```bash
python -m app.database.init_db
```

## Generate and Seed Synthetic Data

```bash
python -m app.database.seed_data
```

## Start Qdrant

```bash
docker compose up -d qdrant
```

## Build the Knowledge Index

```bash
python -m app.rag.pipeline
```

## Run the API

```bash
uvicorn app.main:app --reload
```

## Open Swagger

```text
http://127.0.0.1:8000/docs
```

## Run Tests

```bash
pytest -v
```

---

# Milestone 2 — RAG Knowledge System

**Status: Completed**

Milestone 2 introduces the Retrieval-Augmented Generation (RAG) knowledge layer of the SupplyChain AI Copilot.

The goal of this milestone is to allow future AI agents to retrieve trusted supply-chain knowledge from controlled internal documents instead of depending only on an LLM's general knowledge.

The completed RAG pipeline is:

```text
Knowledge Base Documents
        ↓
Document Ingestion
        ↓
Text Chunking
        ↓
Sentence Transformer Embeddings
        ↓
Qdrant Vector Database
        ↓
Semantic Retrieval
        ↓
Keyword-Based Reranking
        ↓
Knowledge Search Service
        ↓
FastAPI RAG API
```

---

# Milestone 2 Goals

The main objectives were:

* Build a controlled supply-chain knowledge base
* Load and validate knowledge documents
* Split documents into searchable chunks
* Generate vector embeddings
* Store embeddings in Qdrant
* Implement semantic retrieval
* Implement deterministic reranking
* Expose RAG functionality through FastAPI
* Add validation and error handling
* Add RAG evaluation metrics
* Add observability for RAG execution
* Add automated tests

---

# Knowledge Base

The RAG system currently uses a controlled knowledge base containing supply-chain operational documentation.

```text
knowledge_base/

├── supplier_sla/
│   ├── supplier_sla_policy.txt
│   └── supplier_delay_policy.txt
│
├── sop/
│   ├── delayed_order_sop.txt
│   └── inventory_replenishment_sop.txt
│
└── policies/
    ├── customer_delay_policy.txt
    └── supplier_escalation_policy.txt
```

The knowledge base currently contains six documents covering:

* Supplier SLAs
* Supplier delay management
* Delayed-order procedures
* Inventory replenishment
* Customer delay handling
* Supplier escalation policies

These documents provide controlled sources that can later be used by the RAG Agent.

---

# Document Ingestion

The ingestion layer automatically discovers `.txt` files inside the knowledge base.

Implemented functionality:

* Recursive document discovery
* UTF-8 file reading
* Empty-document filtering
* Relative source path generation
* Category extraction
* File metadata preservation

Each document is represented internally using structured metadata:

```text
KnowledgeDocument

content
source
category
file_name
```

This metadata is preserved throughout the RAG pipeline so retrieved information can be traced back to its original document.

---

# Document Chunking

Large documents are divided into smaller searchable chunks.

The chunking system supports:

* Configurable chunk size
* Configurable chunk overlap
* Chunk indexing
* Source metadata preservation
* Input validation

Current default configuration:

```text
Chunk size:    500 words
Chunk overlap: 50 words
```

The overlap helps preserve context between neighboring chunks.

Each generated chunk contains:

```text
content
source
category
file_name
chunk_index
```

---

# Embeddings

The project uses Sentence Transformers to convert text into numerical vector representations.

Current embedding model:

```text
all-MiniLM-L6-v2
```

Embedding dimension:

```text
384
```

The embedding service supports:

* Single-text embedding
* Batch chunk embedding
* Normalized embeddings
* Cached model initialization

The embedding model is cached so the application does not repeatedly load the model for every request.

---

# Qdrant Vector Database

Qdrant is used as the vector database for semantic retrieval.

Qdrant runs locally through Docker.

```text
Application
     ↓
Qdrant Client
     ↓
Qdrant
     ↓
supplychain_knowledge collection
```

Current vector configuration:

```text
Vector size: 384
Distance:    Cosine
```

The stored payload contains:

```text
content
source
category
file_name
chunk_index
```

Deterministic UUID-based point IDs are used so the same document chunk can be indexed consistently.

---

# Qdrant Docker Service

The project includes a Qdrant service in `docker-compose.yml`.

```yaml
qdrant:
  image: qdrant/qdrant:latest
  container_name: supplychain-qdrant
  ports:
    - "6333:6333"
    - "6334:6334"
  volumes:
    - qdrant_storage:/qdrant/storage
```

Start Qdrant with:

```bash
docker compose up -d qdrant
```

Qdrant is configured through environment variables:

```env
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION_NAME=supplychain_knowledge
```

---

# Semantic Retrieval

The retriever performs the following workflow:

```text
User Query
    ↓
Query Embedding
    ↓
Qdrant Vector Search
    ↓
Top N Relevant Chunks
```

The retrieval layer returns structured objects containing:

```text
content
source
category
file_name
chunk_index
retrieval_score
```

The original Qdrant similarity score is preserved as:

```text
retrieval_score
```

This makes retrieval results easier to evaluate and monitor.

---

# Reranking

A deterministic keyword-based reranker was implemented after semantic retrieval.

The complete retrieval pipeline is:

```text
Query
  ↓
Embedding
  ↓
Qdrant Semantic Search
  ↓
Initial Retrieved Chunks
  ↓
Keyword Reranking
  ↓
Top-K Results
```

The final reranking score combines:

```text
70% semantic retrieval score
+
30% keyword matching score
```

This provides an additional relevance signal on top of vector similarity.

The reranker also stores:

```text
rerank_score
```

for every returned chunk.

This design intentionally keeps the reranking layer independent so it can later be replaced with a more advanced cross-encoder or learned reranker.

---

# Knowledge Search Service

A dedicated search service coordinates retrieval and reranking.

```text
KnowledgeSearchService
        ↓
KnowledgeRetriever
        ↓
Qdrant
        ↓
Retrieved Chunks
        ↓
KnowledgeReranker
        ↓
Final Knowledge Results
```

The service validates:

* Query input
* Retrieval limit
* Top-K value

This keeps the RAG API layer thin and makes the retrieval pipeline reusable by future agents.

---

# RAG API

A production-oriented FastAPI endpoint was added:

```text
POST /rag/search
```

Example request:

```json
{
  "query": "What should we do when a supplier shipment is delayed?",
  "retrieval_limit": 5,
  "top_k": 3
}
```

The response contains:

```text
query
chunks
```

Each returned chunk contains:

```text
content
source
category
file_name
chunk_index
retrieval_score
rerank_score
```

This allows future agents to use the same service instead of directly accessing Qdrant.

---

# RAG API Validation

The API validates user input using Pydantic.

Current limits:

```text
retrieval_limit:
1 → 20

top_k:
1 → 10
```

Invalid requests are rejected before reaching the retrieval system.

Examples:

```text
Empty query          → 422
retrieval_limit=0    → 422
top_k=0              → 422
retrieval_limit > 20 → 422
```

---

# Error Handling

The RAG API separates validation errors from unexpected infrastructure failures.

Validation errors return:

```text
HTTP 400
```

Unexpected search or infrastructure failures return:

```text
HTTP 503
```

This prevents internal implementation details from being exposed to API clients.

---

# RAG Observability

Basic production-oriented observability was added to the RAG execution flow.

Each RAG request receives a unique:

```text
Request ID
```

The system tracks:

```text
Request ID
Total latency
Retrieved chunk count
Success/failure
Error type
```

Example execution flow:

```text
RAG Request
    ↓
Generate Request ID
    ↓
Start Latency Timer
    ↓
Execute Retrieval
    ↓
Execute Reranking
    ↓
Record Metrics
    ↓
Structured Log
```

Example log information:

```text
RAG execution completed

request_id=<unique-id>
latency_ms=<value>
retrieval_count=<value>
success=True
```

Failed executions record:

```text
request_id
latency
error type
error message
```

The request ID is also returned through:

```text
X-Request-ID
```

HTTP response header.

This is an observability foundation. More advanced distributed tracing, metrics collection, dashboards, alerting, and production monitoring are planned for later milestones.

---

# RAG Evaluation

A retrieval evaluation foundation has been added to the project.

The evaluation layer is designed to support metrics such as:

```text
Recall@K
Precision@K
MRR
```

The evaluation layer is intentionally separated from the retrieval implementation so retrieval quality can be measured independently.

Future milestones will expand evaluation to:

* RAG answer quality
* Groundedness
* Agent decisions
* Tool execution
* Recommendation quality
* End-to-end workflow quality

---

# Milestone 2 Project Structure

The RAG-related project structure is:

```text
app/

├── rag/
│   ├── __init__.py
│   ├── ingestion.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── qdrant_client.py
│   ├── qdrant_store.py
│   ├── retriever.py
│   ├── reranker.py
│   ├── search_service.py
│   ├── dependencies.py
│   └── pipeline.py
│
├── api/
│   └── rag.py
│
├── evaluation/
│   ├── __init__.py
│   ├── evaluation_metrics.py
│   ├── rag_eval.py
│   └── agent_eval.py
│
└── observability/
    ├── __init__.py
    ├── tracing.py
    ├── llm_traces.py
    ├── agent_execution.py
    ├── tool_calls.py
    ├── latency.py
    ├── errors.py
    └── request_ids.py
```

---

# RAG Tests

Milestone 2 significantly expanded the automated test suite.

Tests cover:

## Ingestion

* Knowledge-base discovery
* Document loading
* Metadata extraction
* Empty document handling

## Chunking

* Chunk generation
* Chunk overlap
* Chunk indexing
* Invalid chunk parameters

## Embeddings

* Single-text embeddings
* Batch embeddings
* Empty input validation
* Model abstraction

## Qdrant

* Collection creation
* Collection existence
* Idempotent collection creation
* Chunk upsert
* Metadata storage
* Deterministic point IDs
* Invalid input handling

## Retrieval

* Query embedding
* Vector search
* Retrieved metadata
* Retrieval scores
* Empty query validation

## Reranking

* Keyword matching
* Combined ranking score
* Top-K selection
* Rerank score generation

## Search Service

* Retrieval and reranking integration
* Input validation
* Empty-result handling

## API

* Successful RAG search
* Request validation
* Retrieval limit validation
* Top-K validation
* Request ID response header

## Observability

* Request ID generation
* Latency measurement
* Successful execution tracking
* Failed execution tracking

Run the complete test suite:

```bash
pytest -v
```

Current test result:

```text
88 passed
```

---

# Milestone 2 Technology Stack

The RAG layer currently uses:

```text
Python
FastAPI
Pydantic
Sentence Transformers
all-MiniLM-L6-v2
Qdrant
Docker
pytest
SQLAlchemy
PostgreSQL
```

---

# Complete Milestone 2 Flow

The completed RAG flow is:

```text
Knowledge Base
      ↓
Document Ingestion
      ↓
Document Chunking
      ↓
Sentence Transformer
      ↓
384-D Embeddings
      ↓
Qdrant
      ↓
Semantic Retrieval
      ↓
Keyword Reranking
      ↓
Knowledge Search Service
      ↓
FastAPI /rag/search
      ↓
Request ID + Latency + Metrics
```

---

# How Milestone 2 Supports Future Agents

The RAG system is intentionally implemented as an independent service layer.

Future architecture:

```text
                    LangGraph Supervisor
                            │
                            ▼
                       RAG Agent
                            │
                            ▼
                  Knowledge Search Service
                       /            \
                      ▼              ▼
                  Qdrant         Reranker
                      │
                      ▼
              Trusted Knowledge
```

The future RAG Agent will be able to retrieve:

* Supplier SLA requirements
* Supplier delay procedures
* Inventory replenishment rules
* Customer delay policies
* Supplier escalation policies
* Operational SOPs

This allows the agent to ground its decisions in controlled business documentation.

---

# Example Future Investigation

The final platform should be able to investigate:

```text
Why is order ORD-10482 delayed?
```

The future workflow can combine:

```text
PostgreSQL
    +
Qdrant
    +
Neo4j
    +
ML / Forecasting
    +
Business Rules
    +
LLM Reasoning
```

For example:

```text
Order ORD-10482
        ↓
Shipment SHIP-20482
        ↓
Supplier SUP-017
        ↓
Supplier SLA / Delay Policy
        ↓
Inventory SKU-0077
        ↓
Business Rules
        ↓
Recommendation
```

Milestone 2 provides the trusted-document retrieval component of this future investigation.

---

# Milestone 2 Outcome

Milestone 2 transformed the project from a traditional backend/data platform into a system with a dedicated knowledge-retrieval layer.

The project now has:

```text
✓ Controlled knowledge base

✓ Document ingestion

✓ Chunking

✓ Embeddings

✓ Qdrant vector database

✓ Semantic retrieval

✓ Deterministic reranking

✓ RAG search API

✓ Request IDs

✓ Latency tracking

✓ Error tracking

✓ Retrieval evaluation foundation

✓ Automated tests

✓ 88 passing tests
```

The RAG layer is now ready to be consumed by the future multi-agent architecture.

---

# Milestone Roadmap Update

```text
Milestone 1 — Data & Backend Foundation

████████████████████ 100%


Milestone 2 — RAG Knowledge System

████████████████████ 100%


Milestone 3 — Knowledge Graph

░░░░░░░░░░░░░░░░░░░░   0%


Milestone 4 — LangGraph Multi-Agent System

░░░░░░░░░░░░░░░░░░░░   0%


Milestone 5 — Intelligence & Conversational Workflow

░░░░░░░░░░░░░░░░░░░░   0%


Milestone 6 — Production Hardening, Evaluation & Deployment

░░░░░░░░░░░░░░░░░░░░   0%
```

---

# Next Milestone

## Milestone 3 — Knowledge Graph

The next milestone will introduce **Neo4j** to represent relationships between supply-chain entities.

The graph structure shown below is a planned conceptual model. The final schema will be designed from the actual PostgreSQL models and seeded dataset before implementation.

```text
Supplier
   │
   ├── SUPPLIES ──→ Product
   │                    │
   │                    ├── STORED_AT ──→ Warehouse
   │                    │
   │                    └── CONTAINED_IN ──→ Order
   │
   └── SHIPS ──→ Shipment
                         │
                         └── BELONGS_TO ──→ Order
```

The graph layer will allow the system to perform relationship-based investigations that are difficult to represent using vector search alone.

The next milestone will focus on:

* Neo4j
* Graph schema
* Entity relationships
* Cypher queries
* Graph data synchronization
* Relationship-based investigation
* Graph query services
* Graph testing
* Graph Agent foundation

The exact graph relationships will be derived from the actual supply-chain data model rather than being assumed in advance.

---

# Current Platform Architecture

After Milestone 2, the platform architecture is:

```text
                         User
                           │
                           ▼
                    FastAPI Gateway
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
      Structured APIs                RAG API
             │                           │
             ▼                           ▼
        PostgreSQL                    Qdrant
                                         │
                                         ▼
                                     Reranker
                                         │
                                         ▼
                                  Knowledge Base


              Next: Neo4j Knowledge Graph
                           │
                           ▼
                 LangGraph Multi-Agent
                           │
                           ▼
                  Recommendations
                           │
                           ▼
                    Workflow Tools
```

The platform is now ready to move from **document-based intelligence** toward **relationship-based supply-chain intelligence** in Milestone 3.

---

# Project Status

```text
Milestone 1  ████████████████████ 100%
Milestone 2  ████████████████████ 100%
Milestone 3  ░░░░░░░░░░░░░░░░░░░░   0%
Milestone 4  ░░░░░░░░░░░░░░░░░░░░   0%
Milestone 5  ░░░░░░░░░░░░░░░░░░░░   0%
Milestone 6  ░░░░░░░░░░░░░░░░░░░░   0%
```

---

# Production Readiness

The project is currently **production-oriented and under active development**.

The architecture follows production engineering principles such as:

* Separation of concerns
* Configuration management
* Service-layer architecture
* Automated testing
* Input validation
* Error handling
* Deterministic business logic
* Retrieval evaluation foundations
* Request tracking
* Latency measurement
* Modular AI components

However, production deployment hardening is intentionally reserved for later milestones.

Planned production-hardening areas include:

* Authentication
* Authorization
* Security controls
* Rate limiting
* Database migrations
* Secrets management
* Production logging
* Metrics and alerting
* Distributed tracing
* Reliability controls
* CI/CD
* Container hardening
* Deployment
* Monitoring
* Backup and recovery
* End-to-end AI evaluation

Therefore, the project should currently be considered **production-oriented / production-style in development**, rather than production-ready.

---

# Author

**Avinash Gupta**

Building an agentic AI system for supply-chain intelligence, retrieval, reasoning, recommendations, and operational workflows.
