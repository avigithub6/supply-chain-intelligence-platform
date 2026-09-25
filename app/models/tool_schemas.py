from typing import Literal

from pydantic import BaseModel, Field, field_validator

from app.models.schemas import (
    InventoryResponse,
    OrderResponse,
    ShipmentResponse,
    SupplierResponse,
)


class GetOrderToolInput(BaseModel):
    """
    Input schema for the Get Order tool.
    """

    order_number: str = Field(
        min_length=1,
        description="Unique order number, for example ORD-10482.",
    )

    @field_validator("order_number", mode="before")
    @classmethod
    def normalize_order_number(cls, value: str) -> str:
        if not isinstance(value, str):
            raise ValueError("Order number must be a string.")

        return value.strip().upper()


class OrderToolOutput(BaseModel):
    """
    Standard output returned by the Get Order tool.
    """

    success: bool
    order: OrderResponse | None = None
    error: str | None = None


class GetInventoryToolInput(BaseModel):
    """
    Input schema for the Get Inventory tool.
    """

    product_sku: str = Field(
        min_length=1,
        description="Product SKU, for example SKU-0077.",
    )

    @field_validator("product_sku", mode="before")
    @classmethod
    def normalize_product_sku(cls, value: str) -> str:
        if not isinstance(value, str):
            raise ValueError("Product SKU must be a string.")

        return value.strip().upper()


class InventoryToolOutput(BaseModel):
    """
    Standard output returned by the Get Inventory tool.
    """

    success: bool
    inventory: InventoryResponse | None = None
    error: str | None = None


class GetSupplierToolInput(BaseModel):
    """
    Input schema for the Get Supplier tool.
    """

    supplier_code: str = Field(
        min_length=1,
        description="Supplier code, for example SUP-017.",
    )

    @field_validator("supplier_code", mode="before")
    @classmethod
    def normalize_supplier_code(cls, value: str) -> str:
        if not isinstance(value, str):
            raise ValueError("Supplier code must be a string.")

        return value.strip().upper()


class SupplierToolOutput(BaseModel):
    """
    Standard output returned by the Get Supplier tool.
    """

    success: bool
    supplier: SupplierResponse | None = None
    error: str | None = None


class GetShipmentToolInput(BaseModel):
    """
    Input schema for the Get Shipment tool.
    """

    shipment_number: str = Field(
        min_length=1,
        description="Shipment number, for example SHIP-20482.",
    )

    @field_validator("shipment_number", mode="before")
    @classmethod
    def normalize_shipment_number(cls, value: str) -> str:
        if not isinstance(value, str):
            raise ValueError("Shipment number must be a string.")

        return value.strip().upper()


class ShipmentToolOutput(BaseModel):
    """
    Standard output returned by the Get Shipment tool.
    """

    success: bool
    shipment: ShipmentResponse | None = None
    error: str | None = None


# ============================================================
# Workflow Action
# ============================================================

class WorkflowActionRequest(BaseModel):
    """
    Input schema for requesting an operational workflow action.
    """

    action: Literal[
        "escalate_supplier",
        "escalate_delayed_shipment",
        "initiate_replenishment",
    ]

    order_number: str = Field(
        min_length=1,
        description="Order associated with the workflow action.",
    )

    reason: str = Field(
        min_length=1,
        description="Business reason for requesting the action.",
    )

    requested_by: str = Field(
        min_length=1,
        description="Agent or system requesting the action.",
    )

    @field_validator("order_number", mode="before")
    @classmethod
    def normalize_order_number(cls, value: str) -> str:
        if not isinstance(value, str):
            raise ValueError("Order number must be a string.")

        return value.strip().upper()

    @field_validator("reason", "requested_by", mode="before")
    @classmethod
    def normalize_text(cls, value: str) -> str:
        if not isinstance(value, str):
            raise ValueError("Value must be a string.")

        value = value.strip()

        if not value:
            raise ValueError("Value cannot be empty.")

        return value


class WorkflowActionResponse(BaseModel):
    """
    Result returned when a workflow action is requested.
    """

    success: bool
    action: str
    order_number: str
    status: Literal[
        "pending_approval",
        "rejected",
        "executed",
    ]
    reason: str
    requested_by: str
    message: str
    error: str | None = None


# ============================================================
# Human Approval
# ============================================================

class HumanApprovalRequest(BaseModel):
    """
    Input schema used by a human reviewer
    to approve or reject a pending workflow action.
    """

    action: Literal[
        "escalate_supplier",
        "escalate_delayed_shipment",
        "initiate_replenishment",
    ]

    order_number: str = Field(
        min_length=1,
        description="Order associated with the action.",
    )

    decision: Literal[
        "approved",
        "rejected",
    ]

    reviewer: str = Field(
        min_length=1,
        description="Human reviewer making the decision.",
    )

    comment: str = Field(
        default="",
        description="Optional reviewer comment.",
    )

    @field_validator("order_number", mode="before")
    @classmethod
    def normalize_order_number(
        cls,
        value: str,
    ) -> str:
        if not isinstance(value, str):
            raise ValueError(
                "Order number must be a string."
            )

        return value.strip().upper()

    @field_validator(
        "reviewer",
        "comment",
        mode="before",
    )
    @classmethod
    def normalize_text(
        cls,
        value: str,
    ) -> str:
        if not isinstance(value, str):
            raise ValueError(
                "Value must be a string."
            )

        return value.strip()


class HumanApprovalResponse(BaseModel):
    """
    Result returned after a human approval decision.
    """

    success: bool

    action: str

    order_number: str

    decision: Literal[
        "approved",
        "rejected",
    ]

    reviewer: str

    comment: str

    message: str

    error: str | None = None


# ============================================================
# Workflow Action Execution
# ============================================================

class ExecuteWorkflowActionRequest(BaseModel):
    """
    Input schema for executing an already-approved
    workflow action.
    """

    action: Literal[
        "escalate_supplier",
        "escalate_delayed_shipment",
        "initiate_replenishment",
    ]

    order_number: str = Field(
        min_length=1,
        description="Order associated with the action.",
    )

    reason: str = Field(
        min_length=1,
        description="Business reason for executing the action.",
    )

    executed_by: str = Field(
        min_length=1,
        description="Human reviewer authorizing execution.",
    )

    @field_validator("order_number", mode="before")
    @classmethod
    def normalize_order_number(cls, value: str) -> str:
        if not isinstance(value, str):
            raise ValueError("Order number must be a string.")

        return value.strip().upper()

    @field_validator(
        "reason",
        "executed_by",
        mode="before",
    )
    @classmethod
    def normalize_execution_text(
        cls,
        value: str,
    ) -> str:
        if not isinstance(value, str):
            raise ValueError("Value must be a string.")

        value = value.strip()

        if not value:
            raise ValueError("Value cannot be empty.")

        return value


class ExecuteWorkflowActionResponse(BaseModel):
    """
    Result returned after an approved workflow action
    has been executed.
    """

    success: bool

    action: str

    order_number: str

    status: Literal[
        "executed",
        "failed",
    ]

    executed_by: str

    reason: str

    message: str

    error: str | None = None