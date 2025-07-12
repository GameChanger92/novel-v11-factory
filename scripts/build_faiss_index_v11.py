#!/usr/bin/env python3
"""
FAISS Index Builder v11 - "FAISS Lite" spec §4.2
Creates FAISS index from story_bible_v11.json character descriptions and episode summaries.
"""

import argparse
import json
import pickle
import sys
from pathlib import Path
import faiss  # type: ignore
from sentence_transformers import SentenceTransformer


def main() -> None:
    parser = argparse.ArgumentParser(description='Build FAISS index from story bible v11')
    parser.add_argument('--project', required=True, help='Project name')
    parser.add_argument('--source-bible', required=True, help='Path to story_bible_v11.json')
    parser.add_argument('--model', default='all-MiniLM-L6-v2', help='SentenceTransformer model')
    args = parser.parse_args()

    with open(args.source_bible, 'r', encoding='utf8') as f:
        data = json.load(f)

    texts, metadata = [], []

    for char in data.get('characters', []):
        if 'description' in char:
            texts.append(char['description'])
            metadata.append({
                'source': 'char_desc',
                'graph_id': char.get('graph_id', 'unknown'),
                'snippet': char['description'][:60]
            })

    for ep in data.get('episode_log', []):
        if 'summary' in ep:
            texts.append(ep['summary'])
            metadata.append({
                'source': 'ep_summary',
                'graph_id': f"ep_{ep.get('episode_id', 'unknown'):03d}",
                'snippet': ep['summary'][:60]
            })

    if not texts:
        sys.exit("⛔ No texts found to index")

    model = SentenceTransformer(args.model)
    vectors = model.encode(texts, batch_size=32).astype('float32')
    faiss.normalize_L2(vectors)
    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)

    output_dir = Path(f"memory/faiss_index/{args.project}")
    output_dir.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(output_dir / "index.faiss"))
    pickle.dump(metadata, open(output_dir / "meta.pkl", 'wb'))

    print(f"✅ FAISS index saved: {args.project} (vectors={len(texts)}, dim={vectors.shape[1]})")


if __name__ == "__main__":
    main()
