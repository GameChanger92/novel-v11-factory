"""
Graph synchronization script for Neo4j schema initialization.
Compatible with GameChanger V11.
"""

import argparse
import json
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

    def sync_bible_to_graph(self, bible_data: dict) -> None:
        """
        Sync Bible data to Neo4j graph, merging characters, locations, and items.
        """
        counts = {"characters": 0, "locations": 0, "items": 0}

        with self.driver.session() as session:
            # Sync characters
            if "characters" in bible_data:
                for char_data in bible_data["characters"].values():
                    if "graph_id" in char_data:
                        query = """
                        MERGE (c:Character {graph_id: $char.graph_id})
                        ON CREATE SET c += $char, c.created_at = timestamp()
                        ON MATCH SET c += $char, c.updated_at = timestamp()
                        """
                        session.run(query, char=char_data)
                        counts["characters"] += 1

            # Sync locations
            if "locations" in bible_data:
                for loc_data in bible_data["locations"].values():
                    if "graph_id" in loc_data:
                        query = """
                        MERGE (l:Location {graph_id: $loc.graph_id})
                        ON CREATE SET l += $loc, l.created_at = timestamp()
                        ON MATCH SET l += $loc, l.updated_at = timestamp()
                        """
                        session.run(query, loc=loc_data)
                        counts["locations"] += 1

            # Sync items
            if "items" in bible_data:
                for item_data in bible_data["items"].values():
                    if "graph_id" in item_data:
                        query = """
                        MERGE (i:Item {graph_id: $item.graph_id})
                        ON CREATE SET i += $item, i.created_at = timestamp()
                        ON MATCH SET i += $item, i.updated_at = timestamp()
                        """
                        session.run(query, item=item_data)
                        counts["items"] += 1

        success_msg = (
            f"✅ Bible sync completed. characters={counts['characters']}, "
            f"locations={counts['locations']}, items={counts['items']}"
        )
        print(success_msg)

    def _load_story_bible(self, project_name: str) -> dict:
        """
        Load story bible from projects/{project}/story_bible_v11.json
        """
        bible_path = f"projects/{project_name}/story_bible_v11.json"
        if not os.path.exists(bible_path):
            sys.exit("⛔ Bible not found")

        with open(bible_path, 'r', encoding='utf-8') as f:
            return json.load(f)


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

    syncer = None
    try:
        syncer = Neo4jSyncer()

        if args.init_schema:
            syncer.init_schema()
        else:
            # Load Bible and sync to graph
            bible_data = syncer._load_story_bible(args.project)
            syncer.sync_bible_to_graph(bible_data)
    except Exception as e:
        if args.init_schema:
            print(f"❌ Error initializing schema: {e}", file=sys.stderr)
        else:
            print(f"❌ Error syncing Bible: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if syncer:
            syncer.close()
