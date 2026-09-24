from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class SupplierResponse(BaseModel):
    id: int
    supplier_code: str
    name: str
    location: str
    reliability_score: float

    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    id: int
    order_number: str
    customer_name: str
    product_sku: str
    quantity: int
    status: str

    model_config = ConfigDict(from_attributes=True)


class InventoryResponse(BaseModel):
    id: int
    product_sku: str
    warehouse: str
    current_stock: int
    reorder_point: int

    model_config = ConfigDict(from_attributes=True)


class ShipmentResponse(BaseModel):
    id: int
    shipment_number: str
    order_number: str
    supplier_code: str
    status: str
    expected_delivery: date

    model_config = ConfigDict(from_attributes=True)


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str

class KnowledgeSearchRequest(BaseModel):
    query: str = Field(
        min_length=1,
        description="Natural-language supply-chain knowledge query.",
    )

    retrieval_limit: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Maximum number of chunks retrieved from Qdrant.",
    )

    top_k: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Number of chunks returned after reranking.",
    )


class KnowledgeSearchChunkResponse(BaseModel):
    content: str
    source: str
    category: str
    file_name: str
    chunk_index: int
    retrieval_score: float
    rerank_score: float | None


class KnowledgeSearchResponse(BaseModel):
    query: str
    chunks: list[KnowledgeSearchChunkResponse]