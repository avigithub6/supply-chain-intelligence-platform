from dataclasses import dataclass

from app.rag.ingestion import KnowledgeDocument


@dataclass
class DocumentChunk:
    content: str
    source: str
    category: str
    file_name: str
    chunk_index: int


def chunk_document(
    document: KnowledgeDocument,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> list[DocumentChunk]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0.")

    if chunk_overlap < 0:
        raise ValueError(
            "chunk_overlap cannot be negative."
        )

    if chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be smaller than chunk_size."
        )

    words = document.content.split()

    if not words:
        return []

    chunks: list[DocumentChunk] = []

    start = 0
    chunk_index = 0

    step = chunk_size - chunk_overlap

    while start < len(words):
        end = min(
            start + chunk_size,
            len(words),
        )

        chunk_words = words[start:end]

        content = " ".join(chunk_words).strip()

        if content:
            chunks.append(
                DocumentChunk(
                    content=content,
                    source=document.source,
                    category=document.category,
                    file_name=document.file_name,
                    chunk_index=chunk_index,
                )
            )

        chunk_index += 1
        start += step

    return chunks


def chunk_documents(
    documents: list[KnowledgeDocument],
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> list[DocumentChunk]:
    chunks: list[DocumentChunk] = []

    for document in documents:
        document_chunks = chunk_document(
            document=document,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        chunks.extend(document_chunks)

    return chunks