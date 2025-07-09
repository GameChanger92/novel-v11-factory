"""
Test for FAISS index builder v11
"""

import json
import pickle
from unittest.mock import Mock, patch

import numpy as np

from scripts.build_faiss_index_v11 import main


def test_faiss_builder_creates_index_files(tmp_path):
    """Test that FAISS index builder creates index.faiss and meta.pkl files."""

    # Create test story bible data
    test_data = {
        "characters": [
            {
                "graph_id": "char_001",
                "name": "TestChar1",
                "description": "A test character with some description for embedding"
            },
            {
                "graph_id": "char_002",
                "name": "TestChar2",
                "description": "Another test character with different content"
            }
        ],
        "episode_log": [
            {
                "episode_id": 1,
                "summary": "First episode summary for testing purposes"
            },
            {
                "episode_id": 2,
                "summary": "Second episode with different content to test"
            }
        ]
    }

    # Create test bible file
    bible_file = tmp_path / "test_bible.json"
    with open(bible_file, 'w', encoding='utf8') as f:
        json.dump(test_data, f)

    # Mock SentenceTransformer to avoid network calls
    mock_vectors = np.random.rand(4, 384).astype('float32')  # 4 texts, 384 dim

    with patch('scripts.build_faiss_index_v11.SentenceTransformer') as mock_model:
        mock_instance = Mock()
        mock_instance.encode.return_value = mock_vectors
        mock_model.return_value = mock_instance

        # Mock sys.argv to simulate CLI arguments
        test_args = [
            'build_faiss_index_v11.py',
            '--project', 'test_project',
            '--source-bible', str(bible_file),
            '--model', 'test-model'
        ]

        with patch('sys.argv', test_args):
            # Change to tmp_path for output
            with patch('scripts.build_faiss_index_v11.Path') as mock_path:
                # Create output directory in tmp_path
                output_dir = tmp_path / "memory" / "faiss_index" / "test_project"
                output_dir.mkdir(parents=True, exist_ok=True)

                # Make Path return our tmp directory
                mock_path.return_value = output_dir

                # Mock faiss functions
                with patch('scripts.build_faiss_index_v11.faiss.normalize_L2') as mock_normalize, \
                     patch('scripts.build_faiss_index_v11.faiss.IndexFlatIP') as mock_index_class, \
                     patch('scripts.build_faiss_index_v11.faiss.write_index') as mock_write_index:

                    mock_index = Mock()
                    mock_index_class.return_value = mock_index

                    # Run the main function
                    main()

                    # Verify function calls
                    mock_model.assert_called_once_with('test-model')
                    mock_instance.encode.assert_called_once()
                    mock_normalize.assert_called_once()
                    mock_index_class.assert_called_once_with(384)
                    mock_index.add.assert_called_once()
                    mock_write_index.assert_called_once()

                    # Verify metadata file was created (we can check this exists)
                    meta_file = output_dir / "meta.pkl"
                    assert meta_file.exists()

                    # Verify metadata content
                    with open(meta_file, 'rb') as f:
                        metadata = pickle.load(f)

                    assert len(metadata) == 4  # 2 characters + 2 episodes

                    # Check character metadata
                    char_metas = [m for m in metadata if m['source'] == 'char_desc']
                    assert len(char_metas) == 2
                    assert char_metas[0]['graph_id'] == 'char_001'
                    assert char_metas[0]['snippet'] == 'A test character with some description for embedding'

                    # Check episode metadata
                    ep_metas = [m for m in metadata if m['source'] == 'ep_summary']
                    assert len(ep_metas) == 2
                    assert ep_metas[0]['graph_id'] == 'ep_001'
                    assert ep_metas[0]['snippet'] == 'First episode summary for testing purposes'
