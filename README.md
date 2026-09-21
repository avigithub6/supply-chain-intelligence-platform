# chain-intelligence-platform

## Agentic Supply Chain Intelligence & Operations Platform

chain-intelligence-platform is a production-oriented AI platform designed to investigate supply-chain problems, retrieve trusted operational knowledge, analyze relationships between supply-chain entities, generate recommendations, and support operational workflows.

The platform is being developed incrementally, starting with a reliable data and API foundation before introducing RAG, knowledge graphs, multi-agent workflows, forecasting, conversational interfaces, evaluation, and observability.

---

## Project Goal

The goal is to build an AI copilot that can answer operational questions such as:

> "Why is order ORD-10482 delayed?"

Instead of relying only on an LLM, the system will combine:

* Structured operational data
* Retrieval-Augmented Generation (RAG)
* Embeddings and vector search
* Knowledge graphs
* Multi-agent workflows
* Deterministic business rules
* Statistical/ML models
* Tool calling
* Structured outputs
* Human approval
* Evaluation and observability

The intended architecture is:

```text
User
  ↓
Conversational Interface
  ↓
FastAPI Gateway
  ↓
LangGraph Supervisor
  ↓
 ┌──────────────┬──────────────┬──────────────┐
 ↓              ↓              ↓
Data Agent    RAG Agent     Graph Agent
 ↓              ↓              ↓
PostgreSQL    Qdrant        Neo4j
  \             |             /
   \            |            /
    └──── Recommendation Agent
                    ↓
             Human Approval
                    ↓
              Workflow Tools
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

### Suppliers

50 synthetic supplier records.

Fields include:

* Supplier code
* Supplier name
* Location
* Reliability score

### Inventory

150 synthetic inventory records.

Fields include:

* Product SKU
* Warehouse
* Current stock
* Reorder point

### Orders

1,000 synthetic order records.

Fields include:

* Order number
* Customer
* Product SKU
* Quantity
* Order status

### Shipments

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

This separation allows future agents and tools to reuse the service layer instead of duplicating database logic.

---

# Project Structure

```text
supply-chain-intelligence-platform/
│
├── app/
│   ├── main.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── logging.py
│   │
│   ├── api/
│   │   ├── health.py
│   │   ├── orders.py
│   │   ├── inventory.py
│   │   ├── suppliers.py
│   │   └── shipments.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   ├── session.py
│   │   ├── init_db.py
│   │   └── seed_data.py
│   │
│   ├── models/
│   │   ├── schemas.py
│   │   └── database_models.py
│   │
│   ├── services/
│   │   ├── order_service.py
│   │   ├── inventory_service.py
│   │   ├── supplier_service.py
│   │   └── shipment_service.py
│   │
│   ├── agents/
│   ├── graph/
│   ├── rag/
│   ├── tools/
│   ├── workflows/
│   ├── evaluation/
│   └── observability/
│
├── data/
├── knowledge_base/
├── tests/
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

Run tests with:

```bash
pytest -v
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
* pytest

## Planned

* LangChain
* LangGraph
* Qdrant
* Neo4j
* Embedding models
* Reranking
* LLMs
* Forecasting/ML
* Tool calling
* Structured outputs
* Evaluation frameworks
* Observability
* Docker
* CI/CD
* Web conversational interface
* WhatsApp integration

---

# Milestone Roadmap

## Milestone 1 — Data & Backend Foundation

Completed.

```text
FastAPI
PostgreSQL
SQLAlchemy
Data generation
Data APIs
Testing
```

## Milestone 2 — RAG Knowledge System

Planned.

```text
Document ingestion
      ↓
Chunking
      ↓
Embeddings
      ↓
Qdrant
      ↓
Retrieval
      ↓
Reranking
      ↓
Grounded answers
```

## Milestone 3 — Knowledge Graph

Planned.

```text
Orders
Suppliers
Products
Warehouses
Shipments
      ↓
Neo4j
      ↓
Relationship-based investigation
```

## Milestone 4 — LangGraph Multi-Agent System

Planned.

```text
Supervisor
   ↓
Data Agent
RAG Agent
Graph Agent
Recommendation Agent
```

## Milestone 5 — Intelligence & Conversational Workflow

Planned.

* Forecasting
* Recommendation engine
* Structured outputs
* Tool calling
* Human approval
* Web chat
* WhatsApp workflow

## Milestone 6 — Production, Evaluation & Observability

Planned.

* AI evaluation
* RAG evaluation
* Agent evaluation
* LLM traces
* Agent execution traces
* Tool-call monitoring
* Latency tracking
* Error tracking
* Request IDs
* Automated testing
* Docker
* CI/CD
* Deployment
* Documentation

---

# Engineering Principles

The platform is designed around several principles:

### Use deterministic logic when deterministic logic is enough

Not every supply-chain decision needs an LLM.

### Use ML when prediction is required

Forecasting and predictive problems can use statistical or machine-learning models.

### Use RAG for trusted knowledge

Policies, SOPs, supplier SLAs, and operational documentation should be retrieved from controlled sources.

### Use agents for multi-step investigation

Agents will coordinate tools and data sources when a question requires multiple reasoning steps.

### Keep humans in control of high-impact actions

Operational actions can require explicit human approval before execution.

### Evaluate continuously

The system will eventually measure retrieval quality, answer quality, tool execution, agent behavior, latency, and errors.

---

# Development

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the API:

```bash
uvicorn app.main:app --reload
```

Open Swagger:

```text
http://127.0.0.1:8000/docs
```

Run tests:

```bash
pytest -v
```

Initialize database:

```bash
python -m app.database.init_db
```

Generate and seed synthetic data:

```bash
python -m app.database.seed_data
```

---

# Project Status

```text
Milestone 1  ████████████████████ 100%
Milestone 2  ░░░░░░░░░░░░░░░░░░░░   0%
Milestone 3  ░░░░░░░░░░░░░░░░░░░░   0%
Milestone 4  ░░░░░░░░░░░░░░░░░░░░   0%
Milestone 5  ░░░░░░░░░░░░░░░░░░░░   0%
Milestone 6  ░░░░░░░░░░░░░░░░░░░░   0%
```

---

## Author

Avinash Gupta

Building an agentic AI system for supply-chain intelligence, retrieval, reasoning, recommendations, and operational workflows.
