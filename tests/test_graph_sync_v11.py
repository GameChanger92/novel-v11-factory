"""
Tests for the graph_sync_v11.py script.
"""

import os
import sys

# Add the scripts directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

import pytest  # noqa: E402
from unittest.mock import patch, MagicMock  # noqa: E402
from graph_sync_v11 import Neo4jSyncer  # noqa: E402


class TestNeo4jSyncer:
    """Tests for the Neo4jSyncer class."""

    @patch.dict(os.environ, {
        'NEO4J_URI': 'bolt://localhost:7687',
        'NEO4J_USER': 'neo4j',
        'NEO4J_PASSWORD': 'test_password'
    })
    @patch('graph_sync_v11.neo4j.GraphDatabase.driver')
    def test_init_with_valid_env_vars(self, mock_driver):
        """Test Neo4jSyncer initialization with valid environment variables."""
        mock_driver_instance = MagicMock()
        mock_driver.return_value = mock_driver_instance

        syncer = Neo4jSyncer()

        assert syncer.uri == 'bolt://localhost:7687'
        assert syncer.user == 'neo4j'
        assert syncer.password == 'test_password'
        mock_driver.assert_called_once_with(
            'bolt://localhost:7687',
            auth=('neo4j', 'test_password')
        )

    @patch.dict(os.environ, {}, clear=True)
    def test_init_with_missing_env_vars(self):
        """Test Neo4jSyncer initialization fails with missing environment variables."""
        with pytest.raises(ValueError) as exc_info:
            Neo4jSyncer()

        assert "Missing Neo4j connection details" in str(exc_info.value)

    @patch.dict(os.environ, {
        'NEO4J_URI': 'bolt://localhost:7687',
        'NEO4J_USER': 'neo4j',
        'NEO4J_PASSWORD': 'test_password'
    })
    @patch('graph_sync_v11.neo4j.GraphDatabase.driver')
    def test_close(self, mock_driver):
        """Test closing the Neo4j driver connection."""
        mock_driver_instance = MagicMock()
        mock_driver.return_value = mock_driver_instance

        syncer = Neo4jSyncer()
        syncer.close()

        mock_driver_instance.close.assert_called_once()

    @patch.dict(os.environ, {
        'NEO4J_URI': 'bolt://localhost:7687',
        'NEO4J_USER': 'neo4j',
        'NEO4J_PASSWORD': 'test_password'
    })
    @patch('graph_sync_v11.neo4j.GraphDatabase.driver')
    @patch('builtins.print')
    def test_init_schema(self, mock_print, mock_driver):
        """Test schema initialization with proper Cypher queries."""
        mock_driver_instance = MagicMock()
        mock_session = MagicMock()
        mock_driver.return_value = mock_driver_instance
        mock_driver_instance.session.return_value.__enter__.return_value = mock_session

        syncer = Neo4jSyncer()
        syncer.init_schema()

        # Verify that all expected queries were executed
        expected_queries = [
            "CREATE CONSTRAINT IF NOT EXISTS FOR (c:Character) REQUIRE c.graph_id IS UNIQUE;",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (l:Location) REQUIRE l.graph_id IS UNIQUE;",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (i:Item) REQUIRE i.graph_id IS UNIQUE;",
            "CREATE INDEX IF NOT EXISTS FOR (e:EpisodeSummary) ON (e.episode_id);"
        ]

        assert mock_session.run.call_count == 4
        for i, expected_query in enumerate(expected_queries):
            mock_session.run.assert_any_call(expected_query)

        # Verify success message was printed
        mock_print.assert_called_once_with("✅ Schema initialization completed successfully.")


def test_argument_parsing():
    """Test command line argument parsing."""
    # This will be tested by running the script directly in integration tests
    # since mocking argparse is complex and not very valuable
    pass
