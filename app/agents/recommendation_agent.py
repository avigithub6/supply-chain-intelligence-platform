from app.agents.state import AgentState


def recommendation_agent_node(state: AgentState) -> AgentState:
    """
    Analyze Data, RAG, and Graph results and generate
    a deterministic supply-chain recommendation.
    """

    data_result = state.get("data_result")
    rag_result = state.get("rag_result") or []
    graph_result = state.get("graph_result")

    recommendations: list[str] = []
    evidence: list[str] = []
    risk_factors: list[str] = []

    # ---------------------------------------------------------
    # 1. Validate that we have investigation results
    # ---------------------------------------------------------

    if not data_result and not graph_result and not rag_result:
        return {
            **state,
            "recommendation": None,
            "errors": [
                *state.get("errors", []),
                "Recommendation Agent: no investigation results available.",
            ],
        }

    # ---------------------------------------------------------
    # 2. Analyze order and shipment information
    # ---------------------------------------------------------

    order_data = {}

    if data_result:
        order_data = data_result.get("order") or {}

    if graph_result:
        order_data = {
            **order_data,
            **{
                key: value
                for key, value in {
                    "order_number": graph_result.get("order_number"),
                    "customer_name": graph_result.get("customer_name"),
                    "product_sku": graph_result.get("product_sku"),
                    "quantity": graph_result.get("quantity"),
                    "status": graph_result.get("order_status"),
                }.items()
                if value is not None
            },
        }

    order_number = order_data.get("order_number")
    product_sku = order_data.get("product_sku")
    order_quantity = order_data.get("quantity")
    order_status = order_data.get("status")

    if order_number:
        evidence.append(f"Order: {order_number}")

    if product_sku:
        evidence.append(f"Product: {product_sku}")

    if order_quantity is not None:
        evidence.append(f"Order quantity: {order_quantity}")

    if order_status:
        evidence.append(f"Order status: {order_status}")

    # ---------------------------------------------------------
    # 3. Analyze shipment
    # ---------------------------------------------------------

    shipment = None

    if data_result:
        shipment = data_result.get("shipment")

    shipment_status = None
    shipment_number = None
    supplier_code = None

    if shipment:
        shipment_status = shipment.get("status")
        shipment_number = shipment.get("shipment_number")
        supplier_code = shipment.get("supplier_code")

    if graph_result:
        shipment_status = (
            graph_result.get("shipment_status")
            or shipment_status
        )
        shipment_number = (
            graph_result.get("shipment_number")
            or shipment_number
        )
        supplier_code = (
            graph_result.get("supplier_code")
            or supplier_code
        )

    if shipment_number:
        evidence.append(f"Shipment: {shipment_number}")

    if shipment_status:
        evidence.append(f"Shipment status: {shipment_status}")

    if shipment_status == "delayed" or order_status == "delayed":
        risk_factors.append("Order or shipment is delayed.")
        recommendations.append(
            "Escalate the delayed shipment for operational review."
        )

    # ---------------------------------------------------------
    # 4. Analyze supplier
    # ---------------------------------------------------------

    supplier_reliability = None
    supplier_name = None

    if graph_result:
        supplier_reliability = graph_result.get(
            "supplier_reliability"
        )
        supplier_name = graph_result.get("supplier_name")

    if supplier_code:
        evidence.append(f"Supplier: {supplier_code}")

    if supplier_name:
        evidence.append(f"Supplier name: {supplier_name}")

    if supplier_reliability is not None:
        evidence.append(
            f"Supplier reliability: {supplier_reliability}"
        )

        if supplier_reliability < 70:
            risk_factors.append(
                "Supplier reliability is below the 70% threshold."
            )
            recommendations.append(
                f"Escalate supplier {supplier_code or 'identified supplier'} "
                "and review supplier performance."
            )

    # ---------------------------------------------------------
    # 5. Analyze inventory
    # ---------------------------------------------------------

    current_stock = None
    reorder_point = None

    if graph_result:
        current_stock = graph_result.get("current_stock")
        reorder_point = graph_result.get("reorder_point")

    if current_stock is not None:
        evidence.append(f"Current inventory: {current_stock}")

    if reorder_point is not None:
        evidence.append(f"Reorder point: {reorder_point}")

    if (
        current_stock is not None
        and reorder_point is not None
        and current_stock < reorder_point
    ):
        risk_factors.append(
            "Current inventory is below the reorder point."
        )

        recommendations.append(
            f"Initiate replenishment for {product_sku or 'the affected product'}."
        )

    # ---------------------------------------------------------
    # 6. Analyze retrieved business knowledge
    # ---------------------------------------------------------

    knowledge_sources: list[str] = []

    for chunk in rag_result:
        source = chunk.get("source")
        file_name = chunk.get("file_name")

        if file_name:
            knowledge_sources.append(file_name)
        elif source:
            knowledge_sources.append(source)

    # Remove duplicates while preserving order.
    knowledge_sources = list(dict.fromkeys(knowledge_sources))

    if knowledge_sources:
        evidence.append(
            "Knowledge sources: "
            + ", ".join(knowledge_sources)
        )

    # ---------------------------------------------------------
    # 7. Determine risk level
    # ---------------------------------------------------------

    risk_level = "low"

    if len(risk_factors) >= 3:
        risk_level = "high"
    elif len(risk_factors) >= 1:
        risk_level = "medium"

    # ---------------------------------------------------------
    # 8. Fallback recommendation
    # ---------------------------------------------------------

    if not recommendations:
        recommendations.append(
            "No immediate operational action was identified. "
            "Continue monitoring the order."
        )

    # ---------------------------------------------------------
    # 9. Build structured recommendation
    # ---------------------------------------------------------

    recommendation = {
        "order_number": order_number,
        "product_sku": product_sku,
        "risk_level": risk_level,
        "risk_factors": risk_factors,
        "evidence": evidence,
        "recommendations": recommendations,
        "knowledge_sources": knowledge_sources,
    }

    return {
        **state,
        "recommendation": recommendation,
        "completed_agents": [
            *state.get("completed_agents", []),
            "recommendation_agent",
        ],
    }