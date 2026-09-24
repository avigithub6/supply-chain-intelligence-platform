import logging

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status,
)

from app.models.schemas import (
    KnowledgeSearchChunkResponse,
    KnowledgeSearchRequest,
    KnowledgeSearchResponse,
)
from app.observability.tracing import RAGExecutionTracker
from app.rag.dependencies import (
    get_knowledge_search_service,
)
from app.rag.search_service import (
    KnowledgeSearchService,
)


logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/rag",
    tags=["RAG"],
)


@router.post(
    "/search",
    response_model=KnowledgeSearchResponse,
    status_code=status.HTTP_200_OK,
)
def search_knowledge(
    request: KnowledgeSearchRequest,
    response: Response,
    search_service: KnowledgeSearchService = Depends(
        get_knowledge_search_service
    ),
) -> KnowledgeSearchResponse:

    tracker = RAGExecutionTracker()

    try:
        result = search_service.search(
            query=request.query,
            retrieval_limit=request.retrieval_limit,
            top_k=request.top_k,
        )

        metrics = tracker.finish(
            retrieval_count=len(result.chunks)
        )

        response.headers["X-Request-ID"] = (
            metrics.request_id
        )

    except ValueError as error:
        metrics = tracker.fail(error)

        response.headers["X-Request-ID"] = (
            metrics.request_id
        )

        logger.warning(
            "RAG validation error | "
            "request_id=%s | error=%s",
            metrics.request_id,
            str(error),
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    except Exception as error:
        metrics = tracker.fail(error)

        response.headers["X-Request-ID"] = (
            metrics.request_id
        )

        logger.exception(
            "RAG search failed | "
            "request_id=%s",
            metrics.request_id,
        )

        raise HTTPException(
            status_code=(
                status.HTTP_503_SERVICE_UNAVAILABLE
            ),
            detail=(
                "Knowledge search service is "
                "temporarily unavailable."
            ),
        ) from error

    chunks = [
        KnowledgeSearchChunkResponse(
            content=chunk.content,
            source=chunk.source,
            category=chunk.category,
            file_name=chunk.file_name,
            chunk_index=chunk.chunk_index,
            retrieval_score=chunk.retrieval_score,
            rerank_score=chunk.rerank_score,
        )
        for chunk in result.chunks
    ]

    return KnowledgeSearchResponse(
        query=result.query,
        chunks=chunks,
    )