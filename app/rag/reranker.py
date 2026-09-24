from dataclasses import replace

from app.rag.retriever import RetrievedChunk


class KnowledgeReranker:
    def rerank(
        self,
        query: str,
        chunks: list[RetrievedChunk],
        top_k: int = 3,
    ) -> list[RetrievedChunk]:
        if not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than 0."
            )

        if not chunks:
            return []

        query_terms = self._normalize_text(query)

        scored_chunks: list[
            tuple[float, RetrievedChunk]
        ] = []

        for chunk in chunks:
            chunk_terms = self._normalize_text(
                chunk.content
            )

            keyword_score = (
                self._calculate_keyword_score(
                    query_terms=query_terms,
                    chunk_terms=chunk_terms,
                )
            )

            final_score = (
                (0.7 * chunk.retrieval_score)
                + (0.3 * keyword_score)
            )

            reranked_chunk = replace(
                chunk,
                rerank_score=final_score,
            )

            scored_chunks.append(
                (
                    final_score,
                    reranked_chunk,
                )
            )

        scored_chunks.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            chunk
            for _, chunk in scored_chunks[:top_k]
        ]

    @staticmethod
    def _normalize_text(
        text: str,
    ) -> set[str]:
        return {
            word.strip(
                ".,!?;:()[]{}\"'"
            ).lower()
            for word in text.split()
            if word.strip(
                ".,!?;:()[]{}\"'"
            )
        }

    @staticmethod
    def _calculate_keyword_score(
        query_terms: set[str],
        chunk_terms: set[str],
    ) -> float:
        if not query_terms:
            return 0.0

        matched_terms = (
            query_terms.intersection(
                chunk_terms
            )
        )

        return (
            len(matched_terms)
            / len(query_terms)
        )