from neo4j import Driver, GraphDatabase

from app.core.config import settings


class Neo4jClient:
    """Manages the Neo4j database connection and queries."""

    def __init__(self) -> None:
        self._driver: Driver = GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(
                settings.neo4j_username,
                settings.neo4j_password,
            ),
        )

    def verify_connection(self) -> bool:
        """Verify that Neo4j is reachable."""

        self._driver.verify_connectivity()

        return True

    def execute_query(
        self,
        query: str,
        parameters: dict | None = None,
    ) -> list[dict]:
        """Execute a Cypher query and return records."""

        records, _, _ = self._driver.execute_query(
            query,
            parameters_=parameters or {},
        )

        return [
            record.data()
            for record in records
        ]

    def close(self) -> None:
        """Close the Neo4j driver."""

        self._driver.close()


neo4j_client = Neo4jClient()