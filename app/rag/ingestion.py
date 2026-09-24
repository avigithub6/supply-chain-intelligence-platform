from dataclasses import dataclass
from pathlib import Path


@dataclass
class KnowledgeDocument:
    content: str
    source: str
    category: str
    file_name: str


def load_knowledge_documents(
    knowledge_base_path: str = "knowledge_base",
) -> list[KnowledgeDocument]:
    base_path = Path(knowledge_base_path)

    if not base_path.exists():
        raise FileNotFoundError(
            f"Knowledge base directory not found: {base_path}"
        )

    documents: list[KnowledgeDocument] = []

    for file_path in sorted(base_path.rglob("*.txt")):
        content = file_path.read_text(
            encoding="utf-8"
        ).strip()

        if not content:
            continue

        relative_path = file_path.relative_to(base_path)

        category = relative_path.parts[0]

        document = KnowledgeDocument(
            content=content,
            source=relative_path.as_posix(),
            category=category,
            file_name=file_path.name,
        )

        documents.append(document)

    return documents