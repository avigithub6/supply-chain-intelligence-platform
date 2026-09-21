from datetime import date

from pydantic import BaseModel, ConfigDict


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