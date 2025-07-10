"""
Graph synchronization script for Neo4j schema initialization.
Compatible with GameChanger V11.
"""

import argparse
import json
import os
import pathlib
import sys

from dotenv import load_dotenv
import neo4j

load_dotenv()


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

        # 타입 체커를 위한 assert (런타임에서는 위에서 이미 체크됨)
        assert self.uri is not None
        assert self.user is not None
        assert self.password is not None

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
                session.run(query)  # type: ignore

        print("✅ Schema initialization completed successfully.")

    def load_story_bible(self, project_name: str) -> dict:
        """
        지정된 프로젝트의 story_bible_v11.json 파일을 로드합니다.
        """
        file_path = pathlib.Path(f"projects/{project_name}/story_bible_v11.json")
        if not os.path.exists(str(file_path)):
            print(f"⛔️ ERROR: Story Bible file not found at: {file_path}", file=sys.stderr)
            sys.exit(1)

        try:
            with open(file_path, "r", encoding="utf8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"⛔️ ERROR: Failed to decode JSON from {file_path}. Error: {e}", file=sys.stderr)
            sys.exit(1)

    def sync_bible_to_graph(self, bible_data: dict):
        """
        Story Bible 데이터를 Neo4j 그래프에 동기화합니다.
        """
        # 동기화할 데이터 섹션 목록
        sections_to_sync = {
            "characters": "Character",
            "locations": "Location",
            "items": "Item"
        }

        stats = {key: 0 for key in sections_to_sync.keys()}

        with self.driver.session() as session:
            for section, label in sections_to_sync.items():
                if section in bible_data and bible_data[section]:
                    for entity in bible_data[section]:
                        # Cypher 쿼리: MERGE를 사용하여 노드 생성 또는 업데이트
                        query = (
                            f"MERGE (n:{label} {{graph_id: $entity.graph_id}}) "
                            "ON CREATE SET n += $entity, n.created_at = timestamp() "
                            "ON MATCH SET n += $entity, n.updated_at = timestamp()"
                        )
                        session.run(query, entity=entity)  # type: ignore
                        stats[section] += 1

        print(f"✅ Bible sync completed. "
              f"characters={stats['characters']}, "
              f"locations={stats['locations']}, "
              f"items={stats['items']}")


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

    neo4j_syncer = None
    try:
        neo4j_syncer = Neo4jSyncer()

        # --init-schema 옵션이 있으면 스키마 초기화 실행
        if args.init_schema:
            neo4j_syncer.init_schema()
        # 옵션이 없으면 기본 동작으로 데이터 동기화 실행
        else:
            print(f"프로젝트 '{args.project}'의 Story Bible을 Neo4j와 동기화합니다...")
            story_bible_data = neo4j_syncer.load_story_bible(args.project)
            neo4j_syncer.sync_bible_to_graph(story_bible_data)

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if neo4j_syncer:
            neo4j_syncer.close()
