# supply-chain-intelligence-platform

# Agentic Supply Chain Intelligence & Operations Platform

The **supply-chain-intelligence-platform** is a production-oriented AI platform designed to investigate supply-chain problems, retrieve trusted operational knowledge, analyze relationships between supply-chain entities, generate recommendations, and support operational workflows.

The platform is being developed incrementally, starting with a reliable data and API foundation before introducing RAG, knowledge graphs, multi-agent workflows, forecasting, conversational interfaces, evaluation, observability, and production hardening.

---

# Project Goal

The goal is to build an AI copilot that can answer operational questions such as:

> **"Why is order ORD-10482 delayed?"**

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

The intended final architecture is:

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
              ┌─────────────────┼─────────────────┐
              │                 │                 │
              ▼                 ▼                 ▼
         Data Agent         RAG Agent        Graph Agent
              │                 │                 │
              ▼                 ▼                 ▼
         PostgreSQL          Qdrant             Neo4j
              │                 │                 │
              └─────────────────┼─────────────────┘
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

> **"Why is order ORD-10482 delayed?"**

The system does not simply ask an LLM to guess the answer.

Instead, it investigates the problem using multiple trusted sources:

1. PostgreSQL checks order, inventory, supplier, and shipment data.
2. The RAG system retrieves relevant supplier policies and SOPs.
3. Neo4j analyzes relationships between orders, products, suppliers, shipments, and warehouses.
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

| Milestone                                                       | Status      |
| --------------------------------------------------------------- | ----------- |
| Milestone 1 — Data & Backend Foundation                         | ✅ Completed |
| Milestone 2 — RAG Knowledge System                              | ✅ Completed |
| Milestone 3 — Knowledge Graph                                   | ✅ Completed |
| Milestone 4 — LangGraph Multi-Agent Architecture                | 🔜 Next     |
| Milestone 5 — Tools & Workflow Integration                      | Planned     |
| Milestone 6 — Recommendation & Forecasting                      | Planned     |
| Milestone 7 — Evaluation & Observability                        | Planned     |
| Milestone 8 — Conversational Interfaces & Production Deployment | Planned     |

---

# Milestone 1 — Supply Chain Data & Backend Foundation

**Status: Completed**

Milestone 1 established the backend and operational data foundation required by the future AI-agent system.

## Implemented

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

The current operational dataset contains synthetic supply-chain data.

## Suppliers

**50 supplier records**

Fields include:

* Supplier code
* Supplier name
* Location
* Reliability score

## Inventory

**150 inventory records**

Fields include:

* Product SKU
* Warehouse
* Current stock
* Reorder point

## Orders

**1,000 order records**

Fields include:

* Order number
* Customer
* Product SKU
* Quantity
* Order status

## Shipments

**1,000 shipment records**

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
Product
  ↓
Inventory
```

Current scenario:

```text
Order
────────────────────
Order Number: ORD-10482
Status: delayed
Quantity: 445
Product: SKU-0077

Shipment
────────────────────
Shipment Number: SHIP-20482
Status: delayed
Expected Delivery: 2026-09-16

Supplier
────────────────────
Supplier Code: SUP-017
Name: Supplier 017 Industries
Reliability Score: 62.5
Location: Pune

Inventory
────────────────────
Product: SKU-0077
Warehouse: Mumbai
Current Stock: 35
Reorder Point: 250
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

# Milestone 1 Architecture

The initial backend follows:

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

The service layer keeps business/data-access logic separate from API route handling.

---

# Milestone 2 — RAG Knowledge System

**Status: Completed**

Milestone 2 introduced the Retrieval-Augmented Generation knowledge layer.

The objective was to allow future AI agents to retrieve trusted supply-chain knowledge from controlled internal documents instead of depending only on an LLM's general knowledge.

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
* Add retrieval evaluation foundations
* Add RAG observability foundations
* Add automated tests

---

# Knowledge Base

The RAG system currently uses a controlled knowledge base containing supply-chain operational documentation.

```text
knowledge_base/
│
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

The knowledge base contains six documents covering:

* Supplier SLAs
* Supplier delay management
* Delayed-order procedures
* Inventory replenishment
* Customer delay handling
* Supplier escalation policies

These documents provide controlled sources that can later be consumed by the RAG Agent.

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

Each document is represented using structured metadata:

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
Chunk size:     500 words
Chunk overlap:   50 words
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
* Reusable model initialization

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

Stored payload:

```text
content
source
category
file_name
chunk_index
```

Deterministic point IDs are used so the same document chunk can be indexed consistently.

---

# Qdrant Docker Service

The project includes Qdrant in `docker-compose.yml`.

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

Environment configuration:

```env
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION_NAME=supplychain_knowledge
```

---

# Semantic Retrieval

The retriever performs:

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

Complete pipeline:

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

The reranker stores:

```text
rerank_score
```

for each returned chunk.

The reranking layer is intentionally independent so it can later be replaced with a more advanced cross-encoder or learned reranker.

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

A FastAPI endpoint was added:

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

This allows future agents to consume the same search service rather than directly accessing Qdrant.

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

Examples:

```text
Empty query            → 422
retrieval_limit = 0    → 422
top_k = 0              → 422
retrieval_limit > 20   → 422
```

---

# RAG Error Handling

The RAG API separates validation errors from unexpected infrastructure failures.

Validation failures are handled separately from unexpected retrieval/infrastructure failures.

Infrastructure failures are converted into controlled API responses rather than exposing internal implementation details to clients.

---

# RAG Observability Foundation

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
Success / failure
Error type
```

Execution flow:

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

The request ID can also be returned through:

```text
X-Request-ID
```

HTTP response header.

More advanced distributed tracing, metrics collection, dashboards, alerting, and production monitoring are planned for later milestones.

---

# RAG Evaluation Foundation

A retrieval evaluation foundation has been added.

The evaluation layer is designed to support metrics such as:

```text
Recall@K
Precision@K
MRR
```

The evaluation layer is separated from the retrieval implementation so retrieval quality can be measured independently.

Future evaluation will expand into:

* RAG answer quality
* Groundedness
* Agent decisions
* Tool execution
* Recommendation quality
* End-to-end workflow quality

---

# Milestone 3 — Knowledge Graph

**Status: Completed**

Milestone 3 introduced **Neo4j** as the relationship-based intelligence layer of the platform.

The goal was to represent relationships between supply-chain entities that are difficult to model using vector search alone.

The completed architecture is:

```text
PostgreSQL
    ↓
Graph Ingestion Service
    ↓
Neo4j
    ↓
Relationship-Based Investigation
```

---

# Why a Knowledge Graph?

Vector search answers questions based primarily on semantic similarity.

A graph database provides a different capability:

```text
Who is connected to what?
```

For supply-chain investigations, this is useful for relationships such as:

```text
Order
  ↓
Shipment
  ↓
Supplier

Order
  ↓
Product
  ↓
Warehouse
```

This makes Neo4j complementary to PostgreSQL and Qdrant rather than a replacement for them.

---

# Neo4j Graph Model

The implemented graph contains five node types.

## Supplier

Primary identifier:

```text
supplier_code
```

## Product

Primary identifier:

```text
product_sku
```

## Warehouse

Primary identifier:

```text
name
```

## Order

Primary identifier:

```text
order_number
```

## Shipment

Primary identifier:

```text
shipment_number
```

---

# Graph Relationships

The implemented relationships are:

```text
Supplier ──SUPPLIES──────> Product

Product ───STORED_AT─────> Warehouse

Order ─────CONTAINS──────> Product

Order ─────HAS_SHIPMENT──> Shipment

Shipment ──PROVIDED_BY────> Supplier
```

The `STORED_AT` relationship also stores inventory-specific properties:

```text
current_stock
reorder_point
```

The graph therefore combines entity relationships with relevant operational attributes.

---

# Why Customer Is Not a Graph Node

The current PostgreSQL dataset contains:

```text
customer_name
```

but does not contain a stable customer identifier.

Therefore, customer information remains a property on the `Order` node rather than being represented as a separate entity.

This avoids creating unstable graph identities.

---

# Neo4j Configuration

Neo4j runs locally through Docker.

```yaml
neo4j:
  image: neo4j:5
  container_name: supplychain-neo4j
  ports:
    - "7474:7474"
    - "7687:7687"
  environment:
    NEO4J_AUTH: neo4j/<configured-password>
  volumes:
    - neo4j_data:/data
    - neo4j_logs:/logs
    - neo4j_plugins:/plugins
```

Environment configuration:

```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=<configured-password>
```

The actual password is stored only in `.env` and should never be committed to Git.

---

# Neo4j Client

The project contains a dedicated Neo4j client abstraction:

```text
app/graph/neo4j_client.py
```

The client provides:

* Neo4j driver initialization
* Connectivity verification
* Parameterized Cypher execution
* Driver lifecycle management

This keeps database infrastructure separate from graph business logic.

---

# Graph Schema

The graph schema contains uniqueness constraints for:

```text
Supplier.supplier_code
Product.product_sku
Warehouse.name
Order.order_number
Shipment.shipment_number
```

These constraints provide stable identifiers and protect graph integrity.

The schema is initialized using:

```bash
python -m app.graph.schema
```

---

# Graph Data Ingestion

The project includes a PostgreSQL-to-Neo4j ingestion service.

```text
PostgreSQL
     ↓
SQLAlchemy
     ↓
GraphIngestionService
     ↓
Parameterized Cypher
     ↓
Neo4j
```

The ingestion process:

1. Loads suppliers from PostgreSQL.
2. Loads inventory records.
3. Loads orders.
4. Loads shipments.
5. Builds unique product records.
6. Builds unique warehouse records.
7. Creates graph nodes.
8. Creates order-product relationships.
9. Creates order-shipment relationships.
10. Creates shipment-supplier relationships.
11. Creates product-warehouse relationships.
12. Derives supplier-product relationships from actual shipment/order paths.

---

# Batch Graph Ingestion

The ingestion service uses parameterized Cypher queries with:

```text
UNWIND
```

and:

```text
MERGE
```

This allows large datasets to be inserted in batches while maintaining idempotent behavior.

Default batch size:

```text
500 records
```

The ingestion can be executed with:

```bash
python -m app.graph.ingestion
```

---

# Milestone 3 Graph Statistics

The completed graph contains:

## Nodes

```text
Order       1000
Product      150
Shipment    1000
Supplier      50
Warehouse      6
```

## Relationships

```text
CONTAINS          1000
HAS_SHIPMENT      1000
PROVIDED_BY       1000
STORED_AT          150
SUPPLIES           937
```

The `SUPPLIES` relationship count is 937 because it represents unique Supplier → Product relationships. Multiple shipments can connect the same supplier and product, while `MERGE` prevents duplicate relationships.

---

# Verified Graph Investigation

The deterministic scenario `ORD-10482` was successfully verified in Neo4j.

Graph path:

```text
Order ORD-10482
       │
       ├──CONTAINS──> Product SKU-0077
       │                    │
       │                    └──STORED_AT──> Warehouse Mumbai
       │
       └──HAS_SHIPMENT──> Shipment SHIP-20482
                                │
                                └──PROVIDED_BY──> Supplier SUP-017
```

Verified data:

```text
Order
────────────────────────
ORD-10482
Status: delayed
Quantity: 445
Product: SKU-0077

Shipment
────────────────────────
SHIP-20482
Status: delayed
Expected Delivery: 2026-09-16

Supplier
────────────────────────
SUP-017
Supplier 017 Industries
Reliability: 62.5
Location: Pune

Warehouse
────────────────────────
Mumbai

Inventory
────────────────────────
Current Stock: 35
Reorder Point: 250
```

This establishes a deterministic multi-entity investigation path that can later be consumed by the Graph Agent.

---

# Current Multi-Source Intelligence Architecture

After Milestone 3, the platform contains three complementary intelligence/data layers:

```text
                    Supply Chain Platform
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
     PostgreSQL           Qdrant            Neo4j
   Structured Data    Semantic Knowledge   Relationships
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
                            ▼
                     Future AI Agents
```

Each system has a different responsibility:

| System     | Primary Purpose                  |
| ---------- | -------------------------------- |
| PostgreSQL | Structured operational data      |
| Qdrant     | Semantic knowledge retrieval     |
| Neo4j      | Relationship-based investigation |

This separation prevents the LLM from becoming the source of truth.

---

# Complete Investigation Architecture

The future investigation of:

```text
Why is order ORD-10482 delayed?
```

can combine:

```text
                 User Question
                      │
                      ▼
              LangGraph Supervisor
                      │
       ┌──────────────┼──────────────┐
       ▼              ▼              ▼
   Data Agent      RAG Agent      Graph Agent
       │              │              │
       ▼              ▼              ▼
 PostgreSQL         Qdrant          Neo4j
       │              │              │
       └──────────────┼──────────────┘
                      │
                      ▼
             Recommendation Agent
                      │
                      ▼
                Human Approval
                      │
                      ▼
                Workflow Tools
```

---

# Testing

The project uses `pytest` for automated testing.

The complete test suite currently contains:

```text
88 passed
```

Run:

```bash
pytest -v
```

The test suite covers the backend, RAG components, graph functionality, validation, and supporting infrastructure implemented up to the current milestones.

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
* Neo4j
* Cypher
* Docker
* pytest
* RAG
* Semantic Retrieval
* Deterministic Reranking
* Knowledge Graphs
* Request ID Tracking
* Latency Tracking
* Error Tracking

## Upcoming

* LangChain
* LangGraph
* LLM Integration
* Multi-Agent Workflow
* Tool Calling
* Structured Outputs
* Recommendation Engine
* Forecasting / Machine Learning
* Human Approval
* Web Conversational Interface
* WhatsApp Integration
* Advanced AI Evaluation
* Advanced Observability
* CI/CD
* Production Deployment

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
│   │   └── rag_api.py
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
│   │   ├── queries.py
│   │   ├── schema.py
│   │   └── ingestion.py
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
│   ├── __init__.py
│   │
│   ├── api/
│   ├── agents/
│   ├── rag/
│   ├── tools/
│   ├── graph/
│   ├── workflows/
│   └── services/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# Milestone Roadmap

## Milestone 1 — Data & Backend Foundation

**Status: Completed**

Implemented:

```text
FastAPI
PostgreSQL
SQLAlchemy
Pydantic
Configuration
Synthetic Data
Data APIs
Service Layer
Testing
```

---

## Milestone 2 — RAG Knowledge System

**Status: Completed**

Implemented:

```text
Knowledge Base
Document Ingestion
Chunking
Embeddings
Qdrant
Semantic Retrieval
Deterministic Reranking
RAG Search Service
RAG API
Request IDs
Latency Tracking
Error Tracking
Evaluation Foundation
Automated Testing
```

---

## Milestone 3 — Knowledge Graph

**Status: Completed**

Implemented:

```text
Neo4j
Graph Schema
Uniqueness Constraints
Cypher Queries
Batch Graph Ingestion
PostgreSQL → Neo4j Synchronization
Supplier Relationships
Product Relationships
Order Relationships
Shipment Relationships
Warehouse Relationships
Graph Investigation
Graph Validation
```

Verified:

```text
Orders:      1000
Products:     150
Shipments:   1000
Suppliers:     50
Warehouses:     6
```

---

## Milestone 4 — LangGraph Multi-Agent Architecture

**Status: Next**

Planned architecture:

```text
                    Supervisor
                        │
       ┌────────────────┼────────────────┐
       │                │                │
       ▼                ▼                ▼
  Data Agent        RAG Agent       Graph Agent
       │                │                │
 PostgreSQL          Qdrant          Neo4j
       │                │                │
       └────────────────┼────────────────┘
                        │
                        ▼
              Recommendation Agent
```

Planned work:

* LangGraph state design
* Supervisor node
* Data Agent
* RAG Agent
* Graph Agent
* Recommendation Agent
* Agent routing
* Shared investigation state
* Structured agent outputs
* Conditional workflow edges
* Agent error handling
* Agent testing

---

# Milestone 5 — Tools & Workflow Integration

**Status: Planned**

Planned capabilities:

* Order tools
* Inventory tools
* Supplier tools
* Shipment tools
* Workflow tools
* Function/tool calling
* Structured tool inputs
* Structured tool outputs
* Operational action execution
* Human approval checkpoints
* Safe workflow execution

Example:

```text
Recommendation
      ↓
Human Approval
      ↓
Workflow Tool
      ↓
Operational Action
```

---

# Milestone 6 — Recommendation & Forecasting

**Status: Planned**

This milestone will introduce intelligence beyond retrieval.

Planned capabilities:

* Demand forecasting
* Inventory forecasting
* Delay prediction
* Supplier risk analysis
* Recommendation engine
* Statistical models
* Machine-learning models
* Rule-based decision logic
* Structured recommendation outputs

The platform will deliberately choose between:

```text
Deterministic Rules
        OR
Statistical / ML Model
        OR
Generative AI
```

depending on the problem.

---

# Milestone 7 — Evaluation & Observability

**Status: Planned**

Planned capabilities:

## RAG Evaluation

* Recall@K
* Precision@K
* MRR
* Groundedness
* Context relevance

## Agent Evaluation

* Agent routing
* Tool selection
* State transitions
* Decision quality
* Failure handling

## End-to-End Evaluation

* Investigation accuracy
* Recommendation quality
* Workflow correctness
* Safety
* Latency

## Observability

* LLM traces
* Agent execution traces
* Tool-call monitoring
* Request IDs
* Latency metrics
* Error tracking
* Structured logs
* Metrics
* Alerting

---

# Milestone 8 — Conversational Interfaces & Production Deployment

**Status: Planned**

Planned capabilities:

* Web conversational interface
* WhatsApp integration
* Authentication
* Authorization
* Rate limiting
* Security hardening
* Database migrations
* Secrets management
* Production Docker setup
* CI/CD
* Deployment
* Monitoring
* Health checks
* Readiness checks
* Backup and recovery
* Documentation

---

# Engineering Principles

## Use Deterministic Logic When Deterministic Logic Is Enough

Not every supply-chain decision needs an LLM.

Business rules should be preferred when a problem can be solved reliably using deterministic logic.

---

## Use ML When Prediction Is Required

Forecasting and predictive problems can use statistical or machine-learning models.

---

## Use RAG for Trusted Knowledge

Policies, SOPs, supplier SLAs, and operational documentation should be retrieved from controlled sources.

---

## Use Knowledge Graphs for Relationships

Neo4j is used when the question depends on relationships between entities.

For example:

```text
Order
  ↓
Shipment
  ↓
Supplier
  ↓
Product
  ↓
Warehouse
```

---

## Use Agents for Multi-Step Investigation

Agents will coordinate tools and data sources when a question requires multiple reasoning steps.

---

## Keep Humans in Control of High-Impact Actions

Operational actions can require explicit human approval before execution.

The system should distinguish between:

```text
Investigation
    ↓
Recommendation
    ↓
Approval
    ↓
Execution
```

---

## Evaluate Continuously

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

# Development Setup

## 1. Create Virtual Environment

```bash
python -m venv .venv
```

## 2. Activate Environment

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Configuration

Create a `.env` file based on `.env.example`.

Example structure:

```env
APP_NAME=supply-chain-intelligence-platform
APP_VERSION=1.0.0
ENVIRONMENT=development

DATABASE_URL=postgresql+psycopg2://postgres:<password>@localhost:5432/supplychain

QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION_NAME=supplychain_knowledge

NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=<password>

LOG_LEVEL=INFO
```

Never commit `.env` or database credentials to Git.

---

# Initialize PostgreSQL

```bash
python -m app.database.init_db
```

---

# Generate and Seed Synthetic Data

```bash
python -m app.database.seed_data
```

This creates:

```text
Suppliers: 50
Inventory: 150
Orders: 1000
Shipments: 1000
```

and generates CSV files under:

```text
data/
```

---

# Start Qdrant

```bash
docker compose up -d qdrant
```

---

# Build RAG Knowledge Index

```bash
python -m app.rag.pipeline
```

---

# Start Neo4j

```bash
docker compose up -d neo4j
```

---

# Initialize Neo4j Graph Schema

```bash
python -m app.graph.schema
```

---

# Ingest PostgreSQL Data into Neo4j

```bash
python -m app.graph.ingestion
```

Expected graph ingestion summary:

```text
Suppliers: 50
Products: 150
Warehouses: 6
Orders: 1000
Shipments: 1000
Order -> Product relationships: 1000
Order -> Shipment relationships: 1000
Shipment -> Supplier relationships: 1000
Product -> Warehouse relationships: 150
```

---

# Run the API

```bash
uvicorn app.main:app --reload
```

---

# Open Swagger

```text
http://127.0.0.1:8000/docs
```

---

# Neo4j Browser

Neo4j Browser is available locally at:

```text
http://localhost:7474
```

Bolt connection:

```text
bolt://localhost:7687
```

---

# Run Tests

```bash
pytest -v
```

Current result:

```text
88 passed
```

---

# Complete Platform Flow

The platform currently contains three completed intelligence layers:

```text
                    Supply Chain Platform
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
     PostgreSQL            Qdrant             Neo4j
   Structured Data     Semantic Knowledge   Knowledge Graph
          │                  │                  │
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
                             ▼
                    Future LangGraph
                    Multi-Agent System
                             │
                             ▼
                  Recommendation Engine
                             │
                             ▼
                      Human Approval
                             │
                             ▼
                       Workflow Tools
```

---

# Example Future Investigation

Question:

```text
Why is order ORD-10482 delayed?
```

Potential investigation:

```text
                    ORD-10482
                        │
          ┌─────────────┼─────────────┐
          │             │             │
          ▼             ▼             ▼
     Order Data     Shipment      Product
     PostgreSQL     SHIP-20482    SKU-0077
          │             │             │
          │             ▼             ▼
          │         Supplier       Inventory
          │          SUP-017        Mumbai
          │             │
          │             ▼
          │        Supplier SLA
          │             │
          └─────────────┼─────────────┘
                        ▼
                  Evidence
                        │
                        ▼
                 Recommendation
                        │
                        ▼
                  Human Approval
                        │
                        ▼
                     Action
```

This architecture allows the system to combine:

```text
Structured Data
       +
Semantic Knowledge
       +
Graph Relationships
       +
Business Rules
       +
Machine Learning
       +
LLM Reasoning
```

---

# Production-Oriented Design

The project is currently **production-oriented / production-style in development**, rather than production-ready.

Implemented engineering principles include:

* Separation of concerns
* Configuration management
* Environment-based settings
* Service-layer architecture
* Database abstraction
* Input validation
* Error handling
* Automated testing
* Deterministic business logic
* RAG retrieval
* Vector database
* Knowledge graph
* Batch data ingestion
* Idempotent graph synchronization
* Request tracking
* Latency measurement
* Error tracking
* Modular AI components

Production-hardening work is intentionally reserved for later milestones.

---

# Planned Production Hardening

Future production work includes:

* Authentication
* Authorization
* Security controls
* Rate limiting
* Database migrations
* Secrets management
* Production logging
* Distributed tracing
* Metrics and alerting
* Reliability controls
* CI/CD
* Container hardening
* Deployment
* Monitoring
* Backup and recovery
* End-to-end AI evaluation
* Model monitoring
* Operational alerting

---

# Current Project Status

```text
Milestone 1 — Data & Backend Foundation

████████████████████ 100%


Milestone 2 — RAG Knowledge System

████████████████████ 100%


Milestone 3 — Knowledge Graph

████████████████████ 100%


Milestone 4 — LangGraph Multi-Agent Architecture

░░░░░░░░░░░░░░░░░░░░   0%


Milestone 5 — Tools & Workflow Integration

░░░░░░░░░░░░░░░░░░░░   0%


Milestone 6 — Recommendation & Forecasting

░░░░░░░░░░░░░░░░░░░░   0%


Milestone 7 — Evaluation & Observability

░░░░░░░░░░░░░░░░░░░░   0%


Milestone 8 — Conversational Interfaces & Production Deployment

░░░░░░░░░░░░░░░░░░░░   0%
```

---

# Milestone 3 Outcome

Milestone 3 transformed the platform from having only structured and semantic knowledge into a system that also understands **relationships between supply-chain entities**.

The platform now has:

```text
✓ FastAPI backend

✓ PostgreSQL operational data

✓ Service layer

✓ Controlled knowledge base

✓ Document ingestion

✓ Document chunking

✓ Sentence Transformer embeddings

✓ Qdrant vector database

✓ Semantic retrieval

✓ Deterministic reranking

✓ RAG API

✓ Request ID tracking

✓ Latency tracking

✓ Error tracking

✓ RAG evaluation foundation

✓ Neo4j knowledge graph

✓ Graph schema

✓ Graph constraints

✓ Cypher queries

✓ PostgreSQL → Neo4j ingestion

✓ Relationship-based investigation

✓ 88 passing tests
```

The project is now ready to move from **relationship-based intelligence** to **multi-agent orchestration**.

---

# Next Milestone

## Milestone 4 — LangGraph Multi-Agent Architecture

The next milestone will introduce **LangGraph** and build the initial multi-agent architecture.

Planned structure:

```text
                       User Query
                           │
                           ▼
                    LangGraph Supervisor
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
      Data Agent        RAG Agent       Graph Agent
          │                │                │
          ▼                ▼                ▼
     PostgreSQL          Qdrant           Neo4j
          │                │                │
          └────────────────┼────────────────┘
                           │
                           ▼
                  Recommendation Agent
```

The milestone will focus on:

* LangGraph
* Shared agent state
* Supervisor routing
* Data Agent
* RAG Agent
* Graph Agent
* Recommendation Agent
* Conditional workflow edges
* Structured outputs
* Agent error handling
* Agent testing
* End-to-end investigation flow

The first major target will be an agentic investigation of:

```text
"Why is order ORD-10482 delayed?"
```

---

# Engineering Vision

The long-term goal is not to build an LLM wrapper.

The goal is to build an **agentic supply-chain intelligence platform** where:

```text
Structured Data
       +
Knowledge Retrieval
       +
Knowledge Graph
       +
Business Rules
       +
Machine Learning
       +
LLM Reasoning
       +
Tool Execution
       +
Human Approval
       +
Evaluation
       +
Observability
```

work together as a controlled operational intelligence system.

---

# Author

**Avinash Gupta**

Building an agentic AI system for supply-chain intelligence, retrieval, reasoning, recommendations, and operational workflows.
