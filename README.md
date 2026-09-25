# supply-chain-intelligence-platform

## Agentic Supply Chain Intelligence & Operations Platform

A production-oriented AI platform for investigating supply-chain problems using **PostgreSQL, RAG, Qdrant, Neo4j, LangGraph, deterministic business rules, structured tools, and Human-in-the-Loop workflow execution**.

The platform is designed around a simple principle:

> **LLMs should not be the source of truth for operational decisions.**

Instead, the system combines:

* PostgreSQL for structured operational data
* Qdrant for controlled knowledge retrieval
* Neo4j for relationship-based investigation
* Deterministic business rules for operational recommendations
* LangGraph for multi-agent orchestration
* Structured tools for operational access
* Human approval for high-impact workflow actions
* Controlled execution boundaries for operational actions

---

# Project Goal

The goal of this project is to build a production-style **Agentic Supply Chain Intelligence Platform** capable of answering operational questions such as:

```text
Why is order ORD-10482 delayed?
```

Instead of relying only on an LLM, the platform investigates the problem across multiple data sources.

For example:

```text
Order
  ↓
Shipment
  ↓
Supplier
  ↓
Supplier Reliability

Order
  ↓
Product
  ↓
Warehouse
  ↓
Inventory

Knowledge Base
  ↓
Supplier SLA / SOP / Policies
```

The system then combines the evidence and produces an operational recommendation.

For actions that can affect real operations, the system introduces a human approval checkpoint before execution.

---

# What Does This Platform Actually Do?

The platform is designed to answer supply-chain operational questions by combining multiple intelligence sources.

For an order such as:

```text
ORD-10482
```

the system can investigate:

### 1. Operational Data

From PostgreSQL:

```text
Order status
Shipment status
Product
Quantity
Supplier
Expected delivery
Inventory
```

### 2. Knowledge

From Qdrant:

```text
Supplier SLA
Supplier delay policy
Delayed order SOP
Inventory replenishment SOP
Customer delay policy
Supplier escalation policy
```

### 3. Relationships

From Neo4j:

```text
Order
 ├── Product
 │      └── Warehouse
 │
 └── Shipment
        └── Supplier
```

### 4. Recommendations

Deterministic business rules identify operational risks such as:

```text
Delayed shipment

Low supplier reliability

Low inventory

Supplier escalation requirement
```

### 5. Workflow Actions

The system can prepare controlled actions such as:

```text
Escalate Supplier

Escalate Delayed Shipment

Initiate Replenishment
```

### 6. Human Approval

Sensitive actions require human approval before execution.

```text
Recommendation
      ↓
Workflow Action
      ↓
Human Approval
      ↓
Execution
```

---

# Current Progress

| Milestone                                                       | Status      |
| --------------------------------------------------------------- | ----------- |
| Milestone 1 — Data & Backend Foundation                         | ✅ Completed |
| Milestone 2 — RAG Knowledge System                              | ✅ Completed |
| Milestone 3 — Knowledge Graph                                   | ✅ Completed |
| Milestone 4 — LangGraph Multi-Agent Architecture                | ✅ Completed |
| Milestone 5 — Tools & Workflow Integration                      | ✅ Completed |
| Milestone 6 — Recommendation & Forecasting                      | 🔜 Next     |
| Milestone 7 — Evaluation & Observability                        | Planned     |
| Milestone 8 — Conversational Interfaces & Production Deployment | Planned     |

---

# Milestone 1 — Data & Backend Foundation

**Status: Completed**

Milestone 1 established the backend foundation of the platform.

Implemented:

* FastAPI application
* PostgreSQL database
* SQLAlchemy ORM
* Pydantic schemas
* Pydantic Settings
* Environment configuration
* Application logging
* Database initialization
* Synthetic supply-chain dataset
* Database seeding
* Service layer
* REST APIs
* Pagination
* Filtering
* Error handling
* API tests

---

# Backend Architecture

```text
FastAPI
   ↓
API Routers
   ↓
Service Layer
   ↓
SQLAlchemy
   ↓
PostgreSQL
```

The service layer keeps business and database logic separate from API routes.

---

# Database

PostgreSQL database:

```text
supplychain
```

Main tables:

```text
orders
inventory
shipments
suppliers
```

---

# Synthetic Dataset

The project contains realistic synthetic supply-chain data.

Generated datasets include:

```text
Suppliers
Inventory
Orders
Shipments
```

Current seeded dataset:

```text
Suppliers  → 50
Inventory  → 150
Orders     → 1000
Shipments  → 1000
```

CSV datasets are stored inside:

```text
data/
```

---

# Deterministic Investigation Scenario

One important test scenario is:

```text
Order:
ORD-10482

Customer:
Customer 0482

Product:
SKU-0077

Quantity:
445

Order Status:
delayed
```

Shipment:

```text
SHIP-20482

Supplier:
SUP-017

Status:
delayed

Expected Delivery:
2026-09-16
```

Supplier:

```text
Supplier:
SUP-017

Reliability:
62.5

Location:
Pune
```

Inventory:

```text
SKU:
SKU-0077

Warehouse:
Mumbai

Current Stock:
35

Reorder Point:
250
```

This scenario is used throughout the project to validate the intelligence workflow.

---

# API Endpoints

Implemented APIs include:

```text
/orders
/inventory
/suppliers
/shipments
/health
```

The APIs support:

* Pagination
* Filtering
* Resource lookup
* Validation
* 404 handling

Swagger documentation is available through:

```text
http://127.0.0.1:8000/docs
```

---

# Milestone 2 — RAG Knowledge System

**Status: Completed**

Milestone 2 introduced a controlled Retrieval-Augmented Generation foundation.

The system uses:

```text
Knowledge Base
     ↓
Document Ingestion
     ↓
Chunking
     ↓
Embeddings
     ↓
Qdrant
     ↓
Semantic Retrieval
     ↓
Keyword Reranking
     ↓
Relevant Knowledge
```

---

# Knowledge Base

The controlled knowledge base contains:

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

The knowledge base contains six supply-chain documents covering:

* Supplier SLA
* Supplier delays
* Delayed orders
* Inventory replenishment
* Customer delays
* Supplier escalation

---

# Document Ingestion

The ingestion pipeline:

```text
TXT Documents
      ↓
Document Loading
      ↓
Recursive Chunking
      ↓
Metadata
      ↓
Embeddings
      ↓
Qdrant
```

Current chunking configuration:

```text
Chunk Size:
500 words

Chunk Overlap:
50 words
```

---

# Embeddings

The project uses:

```text
all-MiniLM-L6-v2
```

Embedding dimension:

```text
384
```

---

# Qdrant

Qdrant stores the document embeddings.

Collection:

```text
supplychain_knowledge
```

Distance metric:

```text
Cosine
```

---

# Retrieval

The retrieval process uses:

```text
Semantic Retrieval
        ↓
Keyword Reranking
        ↓
Final Results
```

Reranking combines:

```text
70% semantic score
30% keyword score
```

Each result contains a deterministic:

```text
rerank_score
```

---

# RAG API

Implemented endpoint:

```text
POST /rag/search
```

The API supports:

```text
retrieval_limit: 1–20

top_k: 1–10
```

The RAG layer also includes:

* Request IDs
* Latency tracking
* Error tracking
* `X-Request-ID`
* Retrieval evaluation foundation

Evaluation metrics include:

```text
Recall@K
Precision@K
MRR
```

---

# Milestone 3 — Knowledge Graph

**Status: Completed**

Milestone 3 introduced Neo4j to represent supply-chain relationships.

The graph complements PostgreSQL and RAG by answering relationship-oriented questions.

---

# Knowledge Graph Architecture

```text
PostgreSQL
    ↓
Graph Ingestion
    ↓
Neo4j
```

Main graph entities:

```text
Supplier
Product
Warehouse
Order
Shipment
```

---

# Graph Relationships

```text
Supplier ──SUPPLIES──> Product

Product ──STORED_AT──> Warehouse

Order ──CONTAINS──> Product

Order ──HAS_SHIPMENT──> Shipment

Shipment ──PROVIDED_BY──> Supplier
```

---

# Neo4j Dataset

Current graph contains:

```text
Order Nodes       → 1000
Product Nodes     → 150
Shipment Nodes    → 1000
Supplier Nodes    → 50
Warehouse Nodes   → 6
```

Relationships:

```text
CONTAINS          → 1000
HAS_SHIPMENT      → 1000
PROVIDED_BY       → 1000
STORED_AT         → 150
SUPPLIES          → 937
```

---

# Example Graph Investigation

For:

```text
ORD-10482
```

the graph relationship is:

```text
Order ORD-10482
      │
      ├── CONTAINS ──> Product SKU-0077
      │                     │
      │                     └── STORED_AT ──> Warehouse Mumbai
      │
      └── HAS_SHIPMENT ──> Shipment SHIP-20482
                                │
                                └── PROVIDED_BY ──> Supplier SUP-017
```

This provides relationship-based context for the agent workflow.

---

# Milestone 3 Outcome

The platform now has three independent intelligence sources:

```text
PostgreSQL
    +
Qdrant
    +
Neo4j
```

These sources provide:

```text
Structured Data
Knowledge
Relationships
```

---

# Current Multi-Source Intelligence Architecture

```text
                 Supply Chain Query
                        │
        ┌───────────────┼───────────────┐
        ↓               ↓               ↓
   PostgreSQL         Qdrant          Neo4j
        │               │               │
 Structured Data     Knowledge      Relationships
        │               │               │
        └───────────────┼───────────────┘
                        ↓
              Multi-Source Evidence
```

---

# Milestone 4 — LangGraph Multi-Agent Architecture

**Status: Completed**

Milestone 4 introduced the LangGraph multi-agent orchestration layer.

The objective was to connect the existing PostgreSQL, Qdrant, and Neo4j intelligence layers through a shared agent workflow.

Implemented:

* LangGraph workflow
* Shared `AgentState`
* Supervisor Agent
* Data Agent
* RAG Agent
* Graph Agent
* Recommendation Agent
* Conditional routing
* Structured agent results
* Agent execution tracking
* Agent error handling
* End-to-end investigation workflow
* Automated agent tests

---

# Shared Agent State

Agents communicate through a shared:

```text
AgentState
```

The state contains information such as:

```text
user_query

order_number

required_agents

data_result

rag_result

graph_result

recommendation

final_answer

completed_agents

errors
```

This allows individual agents to contribute investigation results without directly coupling agents together.

---

# Supervisor Agent

The Supervisor Agent analyzes the user query and determines which agents are required.

For an order-specific question:

```text
Why is order ORD-10482 delayed?
```

the supervisor identifies:

```text
Data Agent

Graph Agent

RAG Agent
```

The workflow then routes the investigation through the required agents.

For a general knowledge question without an order number, the workflow can route to the RAG Agent.

---

# Data Agent

The Data Agent retrieves factual operational information from PostgreSQL using the existing service layer.

It retrieves:

* Order details
* Order status
* Product SKU
* Quantity
* Shipment information
* Supplier information
* Expected delivery date

The Data Agent does not directly implement database access logic.

It reuses the existing service layer.

---

# RAG Agent

The RAG Agent connects the LangGraph workflow with the existing RAG knowledge system.

Flow:

```text
User Query
    ↓
Knowledge Search Service
    ↓
Qdrant
    ↓
Semantic Retrieval
    ↓
Deterministic Reranking
    ↓
RAG Agent
```

The agent can retrieve:

* Supplier SLA
* Supplier delay policies
* Delayed order SOP
* Inventory replenishment SOP
* Customer delay policies
* Supplier escalation policies

---

# Graph Agent

The Graph Agent connects the LangGraph workflow with Neo4j.

It investigates relationships such as:

```text
Order
  ↓
Shipment
  ↓
Supplier
```

and:

```text
Order
  ↓
Product
  ↓
Warehouse
```

Neo4j temporal values are converted into JSON-safe values before being stored in the shared agent state.

This ensures compatibility with LangGraph checkpoint serialization.

---

# Recommendation Agent

The Recommendation Agent combines the available operational evidence and applies deterministic business rules.

Example:

```text
Delayed Shipment
       +
Low Supplier Reliability
       +
Low Inventory
       ↓
Operational Recommendation
```

Example recommendations include:

```text
Escalate the delayed shipment for operational review.

Escalate supplier SUP-017 and review supplier performance.

Initiate replenishment for SKU-0077.
```

Risk levels are determined using deterministic rules:

```text
Low
Medium
High
```

The recommendation layer does not allow an LLM to arbitrarily invent operational actions.

---

# Milestone 4 Workflow

The completed workflow is:

```text
User Query
    ↓
Supervisor
    ↓
Data Agent
    ↓
Graph Agent
    ↓
RAG Agent
    ↓
Recommendation Agent
```

Conditional routing determines which agent executes next.

---

# Complete Investigation Architecture

The platform now combines:

```text
                     User Query
                         ↓
                    Supervisor
                         ↓
                  ┌──────┴──────┐
                  ↓             ↓
             Data Agent     RAG Agent
                  ↓
             Graph Agent
                  ↓
          Recommendation Agent
```

---

# Milestone 5 — Tools & Workflow Integration

**Status: Completed**

Milestone 5 extended the multi-agent architecture with structured tools, workflow actions, human approval, and controlled execution.

The milestone was implemented incrementally:

```text
5.1 Tool Foundation
       ↓
5.2 Core Read-only Tools
       ↓
5.3 Workflow / Action Tools
       ↓
5.4 Human Approval Foundation
       ↓
5.5 Workflow Action Agent
       ↓
5.6 Controlled Action Execution
       ↓
5.7 Persistent Human-in-the-Loop
```

---

# Milestone 5.1 — Tool Foundation

**Status: Completed**

Implemented:

* Structured tool schemas
* Pydantic tool inputs
* Pydantic tool outputs
* Order lookup tool
* Input validation
* Database session management
* Service-layer integration
* Tool tests

Architecture:

```text
Agent
  ↓
Structured Tool
  ↓
Service Layer
  ↓
PostgreSQL
```

The tool layer prevents agents from directly accessing database implementation details.

---

# Milestone 5.2 — Core Read-only Tools

**Status: Completed**

Added deterministic read-only tools for:

```text
Orders

Inventory

Suppliers

Shipments
```

The tools reuse the existing PostgreSQL service layer.

Architecture:

```text
Agent
   ↓
Structured Tool
   ↓
Service Layer
   ↓
PostgreSQL
```

This provides a controlled interface between the agent layer and operational data.

---

# Milestone 5.3 — Workflow / Action Tools

**Status: Completed**

Added controlled workflow actions:

```text
escalate_supplier

escalate_delayed_shipment

initiate_replenishment
```

Each workflow action contains:

```text
action

order_number

reason

requested_by
```

Actions initially enter:

```text
pending_approval
```

No real external operational side effect is automatically performed at this stage.

---

# Milestone 5.4 — Human Approval Foundation

**Status: Completed**

Added structured human approval handling.

Supported approval states:

```text
not_required

pending

approved

rejected
```

Approval information contains:

```text
action

order_number

decision

reviewer

comment
```

This creates a controlled separation:

```text
Recommendation
      ↓
Approval Decision
      ↓
Execution
```

---

# Milestone 5.5 — Workflow Action Agent

**Status: Completed**

Added:

```text
Workflow Action Agent
```

The agent converts a recommendation into a structured pending workflow action.

Example:

```text
Recommendation Agent
        ↓
"Escalate supplier SUP-017"
        ↓
Workflow Action Agent
        ↓
escalate_supplier
        ↓
Pending Approval
```

The Workflow Action Agent does not execute the action.

It prepares the action for human review.

---

# Milestone 5.6 — Controlled Action Execution

**Status: Completed**

Added:

```text
Execution Agent
```

and:

```text
Workflow Execution Tool
```

Execution behavior:

```text
No Action
    ↓
No Execution
```

```text
Pending Approval
    ↓
Wait
```

```text
Rejected
    ↓
Skip
```

```text
Approved
    ↓
Execution Agent
    ↓
Workflow Execution Tool
```

The Execution Agent checks the approval state before execution.

Approved actions can proceed to the execution tool.

Rejected actions are skipped.

Pending actions remain waiting for approval.

The current execution tool represents a controlled execution boundary and does not yet perform real external side effects.

Future integrations can connect this layer to:

```text
ERP Systems

Supplier Portals

Email Systems

Inventory Systems

Ticketing Platforms
```

---

# Milestone 5.7 — Persistent Human-in-the-Loop

**Status: Completed**

Milestone 5.7 introduced resumable Human-in-the-Loop execution using LangGraph.

Implemented:

* `InMemorySaver` checkpointing
* Thread-based workflow execution
* LangGraph `interrupt()`
* `Command(resume=...)`
* Human approval checkpoint
* Reviewer tracking
* Approval comments
* Approved execution path
* Rejected execution path
* Pending approval handling
* Controlled execution after approval

The workflow can pause at the human approval checkpoint and resume using the same workflow thread.

Example:

```python
Command(
    resume={
        "decision": "approved",
        "reviewer": "operations_manager",
        "comment": "Approved delayed shipment escalation.",
    }
)
```

Human-in-the-Loop flow:

```text
Recommendation Agent
        ↓
Workflow Action Agent
        ↓
Pending Action
        ↓
LangGraph interrupt()
        ↓
Human Review
      ↙   ↘
Approved  Rejected
    ↓        ↓
Execution   Skip
    ↓
Workflow Execution Tool
    ↓
Action
```

The current implementation uses:

```text
InMemorySaver
```

for checkpointing.

Production-grade persistent checkpoint storage can be introduced during later production-hardening work.

---

# Milestone 5 Workflow

The complete Milestone 5 workflow is:

```text
Recommendation Agent
        ↓
Workflow Action Agent
        ↓
Human Approval
      ↙       ↘
Rejected     Approved
   ↓             ↓
 Skip       Execution Agent
                ↓
        Workflow Execution Tool
                ↓
              Action
```

---

# Complete Agentic Workflow

The complete current platform architecture is:

```text
                         User Query
                              ↓
                     LangGraph Supervisor
                              ↓
              ┌───────────────┴───────────────┐
              ↓               ↓               ↓
         Data Agent       Graph Agent      RAG Agent
              ↓               ↓               ↓
         PostgreSQL         Neo4j           Qdrant
              └───────────────┬───────────────┘
                              ↓
                   Recommendation Agent
                              ↓
                   Workflow Action Agent
                              ↓
                       Human Approval
                         ↙       ↘
                   Rejected      Approved
                      ↓              ↓
                    Skip       Execution Agent
                                    ↓
                          Workflow Execution Tool
                                    ↓
                                  Action
```

---

# Milestone 5 Outcome

Milestone 5 transformed the platform from:

```text
Investigation
      ↓
Recommendation
```

into:

```text
Investigation
      ↓
Recommendation
      ↓
Workflow Action
      ↓
Human Approval
      ↓
Controlled Execution
```

The platform now has the foundation for safe agentic operational workflows where AI can investigate supply-chain problems and prepare operational actions while keeping humans in control of high-impact execution.

---

# Testing

The project includes unit and integration-style tests covering:

* API behavior
* Services
* RAG
* Retrieval
* Graph integration
* Agents
* Tools
* Workflow actions
* Human approval
* Execution
* LangGraph workflow
* Error handling
* Validation

Current test result:

```text
162 passed, 2 warnings
```

The warnings are non-blocking compatibility/deprecation warnings from dependencies.

---

# Technology Stack

## Current

### Backend

```text
Python
FastAPI
Pydantic
Pydantic Settings
SQLAlchemy
PostgreSQL
```

### AI / Agentic Layer

```text
LangGraph
LangChain Core
Multi-Agent Workflow
Shared Agent State
Conditional Agent Routing
Structured Tool Inputs
Structured Tool Outputs
Workflow Actions
Human-in-the-Loop
LangGraph Interrupts
LangGraph Checkpointing
```

### RAG

```text
SentenceTransformers
all-MiniLM-L6-v2
Qdrant
Semantic Retrieval
Keyword Reranking
```

### Knowledge Graph

```text
Neo4j
Cypher
Graph-based Investigation
```

### Infrastructure

```text
Docker
Docker Compose
Uvicorn
```

### Testing

```text
Pytest
FastAPI TestClient
```

---

# Upcoming Technology

The following technologies/features are planned for future milestones:

```text
LLM-based Agent Reasoning
Demand Forecasting
Inventory Forecasting
Supplier Risk Prediction
Delivery Delay Prediction
Evaluation Framework Expansion
LLM Tracing
Observability
Persistent Production Checkpointing
WhatsApp Interface
Conversational UI
Production Deployment
```

---

# Project Structure

```text
supply-chain-intelligence-platform/
│
├── app/
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── state.py
│   │   ├── supervisor.py
│   │   ├── data_agent.py
│   │   ├── rag_agent.py
│   │   ├── graph_agent.py
│   │   ├── recommendation_agent.py
│   │   ├── workflow_agent.py
│   │   ├── approval_agent.py
│   │   └── execution_agent.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── chat.py
│   │   ├── health.py
│   │   ├── inventory.py
│   │   ├── orders.py
│   │   ├── shipments.py
│   │   ├── suppliers.py
│   │   └── rag.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── logging.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── session.py
│   │   ├── init_db.py
│   │   └── seed_data.py
│   │
│   ├── evaluation/
│   │   └── evaluation_metrics.py
│   │
│   ├── graph/
│   │   ├── __init__.py
│   │   ├── neo4j_client.py
│   │   ├── queries.py
│   │   └── ingestion.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── schemas.py
│   │   └── tool_schemas.py
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── ingestion.py
│   │   ├── embeddings.py
│   │   ├── retriever.py
│   │   ├── reranker.py
│   │   ├── search_service.py
│   │   └── pipeline.py
│   │
│   ├── services/
│   │   ├── order_service.py
│   │   ├── inventory_service.py
│   │   ├── supplier_service.py
│   │   └── shipment_service.py
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── order_tools.py
│   │   ├── inventory_tools.py
│   │   ├── supplier_tools.py
│   │   ├── shipment_tools.py
│   │   ├── workflow_tools.py
│   │   └── execution_tools.py
│   │
│   ├── workflows/
│   │   └── supply_chain_graph.py
│   │
│   └── main.py
│
├── data/
│   ├── inventory.csv
│   ├── orders.csv
│   ├── shipments.csv
│   └── suppliers.csv
│
├── knowledge_base/
│   ├── supplier_sla/
│   │   ├── supplier_sla_policy.txt
│   │   └── supplier_delay_policy.txt
│   │
│   ├── sop/
│   │   ├── delayed_order_sop.txt
│   │   └── inventory_replenishment_sop.txt
│   │
│   └── policies/
│       ├── customer_delay_policy.txt
│       └── supplier_escalation_policy.txt
│
├── tests/
│   ├── agents/
│   ├── api/
│   ├── rag/
│   ├── tools/
│   ├── graph/
│   └── services/
│
├── docker-compose.yml
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

# Milestone Roadmap

## Milestone 1 — Data & Backend Foundation

**Status: Completed**

```text
FastAPI
PostgreSQL
SQLAlchemy
REST APIs
Synthetic Data
Testing
```

---

## Milestone 2 — RAG Knowledge System

**Status: Completed**

```text
Knowledge Base
Document Ingestion
Embeddings
Qdrant
Semantic Retrieval
Reranking
RAG API
Retrieval Evaluation
```

---

## Milestone 3 — Knowledge Graph

**Status: Completed**

```text
Neo4j
Graph Modeling
Relationships
Graph Ingestion
Graph Queries
```

---

## Milestone 4 — LangGraph Multi-Agent Architecture

**Status: Completed**

```text
Shared Agent State
Supervisor Agent
Data Agent
RAG Agent
Graph Agent
Recommendation Agent
Conditional Routing
Agent Error Handling
Agent Testing
```

---

## Milestone 5 — Tools & Workflow Integration

**Status: Completed**

```text
Tool Foundation
Read-only Operational Tools
Workflow Action Tools
Human Approval
Workflow Action Agent
Execution Agent
Controlled Execution
LangGraph interrupt()
Command(resume=...)
Checkpointing
Human-in-the-Loop
```

---

## Milestone 6 — Recommendation & Forecasting

**Status: Next**

Planned capabilities:

```text
Demand Forecasting

Inventory Risk Prediction

Supplier Risk Scoring

Delivery Delay Prediction

Forecast-based Recommendations

What-if Analysis
```

---

## Milestone 7 — Evaluation & Observability

**Status: Planned**

Planned capabilities:

```text
LLM Evaluation

Agent Evaluation

RAG Evaluation

Tool-call Evaluation

LLM Tracing

Agent Execution Tracing

Latency Monitoring

Error Tracking

Request IDs

Production Metrics
```

---

## Milestone 8 — Conversational Interfaces & Production Deployment

**Status: Planned**

Planned capabilities:

```text
Conversational UI

WhatsApp Interface

Authentication

Role-based Access

Persistent Checkpointing

Production Infrastructure

Cloud Deployment

Monitoring

Security Hardening
```

---

# Engineering Principles

## 1. LLM Is Not the Source of Truth

Operational facts should come from:

```text
PostgreSQL
Qdrant
Neo4j
```

not from LLM hallucination.

---

## 2. Deterministic Tasks Use Deterministic Logic

For example:

```text
If shipment is delayed
→ identify delayed shipment
```

Business rules should not depend on an LLM when deterministic logic is sufficient.

---

## 3. RAG for Controlled Knowledge

Policies, SOPs, and supplier rules should be retrieved from the controlled knowledge base.

---

## 4. Graph for Relationships

Neo4j is used when the question requires relationship traversal.

Example:

```text
Order
 → Shipment
 → Supplier
```

---

## 5. Agents for Multi-step Investigation

Agents coordinate multiple information sources and tools.

---

## 6. Human Approval for High-impact Actions

The system does not allow an agent to directly execute sensitive operational actions without approval.

```text
AI Recommendation
      ↓
Human Approval
      ↓
Execution
```

---

## 7. Controlled Execution Boundary

Operational actions are isolated behind tools.

```text
Agent
  ↓
Workflow Tool
  ↓
Execution Boundary
  ↓
External System
```

This makes future integrations safer and easier to control.

---

# Development Setup

## 1. Clone Repository

```bash
git clone https://github.com/avigithub6/supply-chain-intelligence-platform.git
cd supply-chain-intelligence-platform
```

---

## 2. Create Virtual Environment

Windows:

```powershell
python -m venv .venv
```

Activate:

```powershell
.venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Configuration

Create:

```text
.env
```

Example:

```env
DATABASE_URL=postgresql+psycopg://postgres:your_password@localhost:5432/supplychain

QDRANT_URL=http://localhost:6333

NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_neo4j_password
```

---

# Initialize PostgreSQL

Create the database:

```text
supplychain
```

Then run:

```bash
python -m app.database.init_db
```

---

# Seed Data

Run:

```bash
python -m app.database.seed_data
```

Expected seeded data:

```text
Suppliers: 50

Inventory: 150

Orders: 1000

Shipments: 1000
```

---

# Start Qdrant

Qdrant is configured through Docker Compose.

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

Start:

```bash
docker compose up -d qdrant
```

Run RAG ingestion:

```bash
python -m app.rag.pipeline
```

---

# Start Neo4j

Neo4j is configured through Docker Compose.

```yaml
neo4j:
  image: neo4j:5
  container_name: supplychain-neo4j
  ports:
    - "7474:7474"
    - "7687:7687"
  environment:
    NEO4J_AUTH: neo4j/your_neo4j_password
  volumes:
    - neo4j_data:/data
    - neo4j_logs:/logs
    - neo4j_plugins:/plugins
```

Start:

```bash
docker compose up -d neo4j
```

Neo4j Browser:

```text
http://localhost:7474
```

---

# Run API

Start FastAPI:

```bash
uvicorn app.main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

# Run Tests

Run the complete test suite:

```bash
pytest -v
```

Current result:

```text
162 passed
```

---

# Complete Platform Flow

The complete current platform works as follows:

```text
                         User
                          ↓
                    User Query
                          ↓
                 FastAPI / Agent Layer
                          ↓
                 LangGraph Supervisor
                          ↓
       ┌──────────────────┼──────────────────┐
       ↓                  ↓                  ↓
  Data Agent          Graph Agent         RAG Agent
       ↓                  ↓                  ↓
 PostgreSQL             Neo4j             Qdrant
       └──────────────────┼──────────────────┘
                          ↓
                Recommendation Agent
                          ↓
                Workflow Action Agent
                          ↓
                   Human Approval
                     ↙         ↘
                Rejected       Approved
                   ↓              ↓
                  Skip      Execution Agent
                                  ↓
                        Workflow Execution Tool
                                  ↓
                                Action
```

---

# Example Future Investigation

User:

```text
Why is order ORD-10482 delayed?
```

The platform can investigate:

### Order

```text
ORD-10482
Status: delayed
Quantity: 445
Product: SKU-0077
```

### Shipment

```text
SHIP-20482
Status: delayed
Expected delivery: 2026-09-16
```

### Supplier

```text
SUP-017
Reliability: 62.5
Location: Pune
```

### Inventory

```text
SKU-0077
Current Stock: 35
Reorder Point: 250
Warehouse: Mumbai
```

### Knowledge

The RAG layer can retrieve relevant:

```text
Supplier SLA
Supplier Delay Policy
Delayed Order SOP
Inventory Replenishment SOP
Supplier Escalation Policy
```

### Recommendation

The deterministic recommendation layer can identify:

```text
Delayed shipment requires operational review.

Supplier SUP-017 has low reliability.

Inventory for SKU-0077 is below the reorder point.
```

### Workflow

The recommendation can become:

```text
Workflow Action
       ↓
Pending Approval
```

A human can then approve or reject the proposed operational action.

---

# Production-Oriented Design

The project is intentionally structured around production-oriented engineering principles.

### Separation of Responsibilities

```text
API Layer
    ↓
Service Layer
    ↓
Data Layer
```

Agentic layer:

```text
Supervisor
    ↓
Specialized Agents
    ↓
Tools
    ↓
Execution Boundary
```

---

# Production Safety Model

The platform separates:

```text
Investigation
```

from:

```text
Action
```

and:

```text
Execution
```

This means an agent can investigate and recommend an action without automatically performing the action.

The intended production flow is:

```text
Read
 ↓
Analyze
 ↓
Recommend
 ↓
Request Approval
 ↓
Approve
 ↓
Execute
```

---

# Planned Production Hardening

Future production hardening will include:

* Persistent LangGraph checkpoint storage
* Authentication
* Authorization
* Role-based access
* Audit logs
* External workflow integrations
* ERP integrations
* Supplier portal integrations
* Email integrations
* Ticketing integrations
* Production observability
* LLM tracing
* Agent tracing
* Retry strategies
* Rate limiting
* Security hardening
* Deployment automation
* Cloud infrastructure

---

# Current Project Status

## Milestone 1

```text
████████████████████ 100%
```

## Milestone 2

```text
████████████████████ 100%
```

## Milestone 3

```text
████████████████████ 100%
```

## Milestone 4

```text
████████████████████ 100%
```

## Milestone 5

```text
████████████████████ 100%
```

## Milestone 6

```text
░░░░░░░░░░░░░░░░░░░░ 0%
```

## Milestone 7

```text
░░░░░░░░░░░░░░░░░░░░ 0%
```

## Milestone 8

```text
░░░░░░░░░░░░░░░░░░░░ 0%
```

---

# Milestone 3 Outcome

Milestone 3 established the relationship intelligence layer using Neo4j.

The platform can now understand relationships between:

```text
Orders
Products
Warehouses
Shipments
Suppliers
```

This became one of the core information sources used by the multi-agent architecture introduced in Milestone 4.

---

# Milestone 5 Outcome

Milestone 5 established the operational workflow layer.

The platform can now move from:

```text
Investigation
```

to:

```text
Recommendation
```

to:

```text
Workflow Action
```

to:

```text
Human Approval
```

to:

```text
Controlled Execution
```

The implementation currently provides a safe execution foundation without performing real external side effects.

---

# Next Milestone

## Milestone 6 — Recommendation & Forecasting

The next major milestone will extend the deterministic recommendation layer with predictive intelligence.

Planned capabilities:

```text
Demand Forecasting
        ↓
Inventory Risk Prediction
        ↓
Supplier Risk Scoring
        ↓
Delivery Delay Prediction
        ↓
Forecast-based Recommendations
        ↓
What-if Analysis
```

The objective is to move the platform from:

```text
Reactive Investigation
```

towards:

```text
Predictive Supply Chain Intelligence
```

---

# Engineering Vision

The long-term vision is to build a production-grade **Agentic Supply Chain Intelligence & Operations Platform** capable of:

```text
Understand
    ↓
Investigate
    ↓
Retrieve
    ↓
Reason
    ↓
Predict
    ↓
Recommend
    ↓
Request Approval
    ↓
Execute
    ↓
Monitor
```

The platform is designed to combine:

```text
Machine Learning
+
Generative AI
+
RAG
+
Knowledge Graphs
+
Multi-Agent Systems
+
Workflow Automation
+
Human-in-the-Loop
```

while maintaining deterministic operational controls wherever required.

---

# Author

**Avinash Gupta**

GitHub:

https://github.com/avigithub6

LinkedIn:

https://linkedin.com/in/theavinashgupta5/

---

# Project Repository

```text
https://github.com/avigithub6/supply-chain-intelligence-platform
```

---

## Current Milestone Summary

```text
Milestone 1  ✅ Completed
Milestone 2  ✅ Completed
Milestone 3  ✅ Completed
Milestone 4  ✅ Completed
Milestone 5  ✅ Completed
Milestone 6  🔜 Next
Milestone 7  ⏳ Planned
Milestone 8  ⏳ Planned
```

**Current achievement:**

```text
Foundation
    ↓
RAG
    ↓
Knowledge Graph
    ↓
Multi-Agent Architecture
    ↓
Tools
    ↓
Workflow Actions
    ↓
Human Approval
    ↓
Controlled Execution
```

The project has now progressed from a traditional backend/data platform into an **agentic, multi-source, human-controlled supply-chain intelligence system**.
