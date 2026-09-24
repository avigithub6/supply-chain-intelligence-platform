from app.graph.neo4j_client import neo4j_client
from app.graph.queries import CREATE_GRAPH_CONSTRAINTS


def initialize_graph_schema() -> None:
    """Create required Neo4j constraints."""

    for query in CREATE_GRAPH_CONSTRAINTS:
        neo4j_client.execute_query(query)


if __name__ == "__main__":
    initialize_graph_schema()
    print("Neo4j graph schema initialized successfully.")