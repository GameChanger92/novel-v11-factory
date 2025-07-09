"""
Graph synchronization script for Neo4j schema initialization.
Compatible with GameChanger V11.
"""

import argparse
import os
import sys

import dotenv
import neo4j

dotenv.load_dotenv()


class Neo4jSyncer:
    """
    Neo4j database syncer for schema initialization and management.
    """

    def __init__(self):
        """Initialize the Neo4j driver with connection details from environment."""
        self.uri = os.getenv("NEO4J_URI")
        self.user = os.getenv("NEO4J_USER")
        self.password = os.getenv("NEO4J_PASSWORD")

        if not all([self.uri, self.user, self.password]):
            raise ValueError(
                "Missing Neo4j connection details. Please set NEO4J_URI, "
                "NEO4J_USER, and NEO4J_PASSWORD in your .env file."
            )

        self.driver = neo4j.GraphDatabase.driver(
            self.uri, auth=(self.user, self.password)
        )

    def close(self):
        """Close the Neo4j driver connection."""
        if self.driver:
            self.driver.close()

    def init_schema(self):
        """
        Initialize the Neo4j schema by creating constraints and indexes.
        Uses IF NOT EXISTS to prevent errors on re-runs.
        """
        schema_queries = [
            "CREATE CONSTRAINT IF NOT EXISTS FOR (c:Character) REQUIRE c.graph_id IS UNIQUE;",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (l:Location) REQUIRE l.graph_id IS UNIQUE;",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (i:Item) REQUIRE i.graph_id IS UNIQUE;",
            "CREATE INDEX IF NOT EXISTS FOR (e:EpisodeSummary) ON (e.episode_id);"
        ]
        with self.driver.session() as session:
            for query in schema_queries:
                session.run(query)

        print("✅ Schema initialization completed successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Neo4j graph synchronization script for GameChanger V11"
    )
    parser.add_argument(
        "--project",
        type=str,
        required=True,
        help="Project name (required)"
    )
    parser.add_argument(
        "--init-schema",
        action="store_true",
        help="Initialize Neo4j schema with constraints and indexes"
    )

    args = parser.parse_args()

    if args.init_schema:
        syncer = None
        try:
            syncer = Neo4jSyncer()
            syncer.init_schema()
        except Exception as e:
            print(f"❌ Error initializing schema: {e}", file=sys.stderr)
            sys.exit(1)
        finally:
            if syncer:
                syncer.close()
