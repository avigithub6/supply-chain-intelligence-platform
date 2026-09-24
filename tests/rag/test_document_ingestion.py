from app.rag.ingestion import load_knowledge_documents


def test_load_knowledge_documents() -> None:
    documents = load_knowledge_documents()

    assert len(documents) == 6

    file_names = {
        document.file_name
        for document in documents
    }

    assert "supplier_sla_policy.txt" in file_names
    assert "supplier_delay_policy.txt" in file_names
    assert "delayed_order_sop.txt" in file_names
    assert "inventory_replenishment_sop.txt" in file_names
    assert "customer_delay_policy.txt" in file_names
    assert "supplier_escalation_policy.txt" in file_names


def test_document_metadata() -> None:
    documents = load_knowledge_documents()

    supplier_document = next(
        document
        for document in documents
        if document.file_name == "supplier_sla_policy.txt"
    )

    assert supplier_document.category == "supplier_sla"

    assert (
        supplier_document.source
        == "supplier_sla/supplier_sla_policy.txt"
    )

    assert "SUPPLIER SERVICE LEVEL AGREEMENT" in (
        supplier_document.content
    )