
# novel-v11-factory

## 🚀 Quick Start (Local Development Guide)

This guide helps you set up the local development environment and run the basic components of the project.

### 1. Initial Setup

First, set up your Python environment and API keys.

# 1. Install required Python packages
pip install -r requirements.txt

# 2. Prepare the environment file. (If .env.example exists, copy it)
# cp .env.example .env

# 3. Open the .env file and add your secret keys.
# It must contain at least:
# OPENAI_API_KEY="sk-..."
# NEO4J_PASSWORD="V11..."


### 4. Syncing Data to Neo4j
To sync the data from `story_bible_v11.json` to the Neo4j database, run:
   python scripts/graph_sync_v11.py --project Pilot

2. Running the Neo4j Database

This project uses Neo4j as its knowledge graph database, which runs inside a Docker container.

Prerequisite: Ensure Docker Desktop is installed and running on your local machine.

Generated bash
# Start the Neo4j service in the background
docker compose up -d neo4j

After running the command, wait for about 1-2 minutes for the database to initialize.

You can access the Neo4j Browser at http://localhost:7747.
(Note: The port is 7747 because we changed it from the default 7474.)

Log in with:

Username: neo4j

Password: The one you set in your `.env` file for `NEO4J_PASSWORD`.

3. Running the Pilot Novel Generation

This command runs the simplified MVP script to generate a few episodes.

Generated bash
# Generate 3 episodes for the "Pilot" project
python scripts/run_novel.py --total 3

Check the generated files in the projects/Pilot/episodes/ directory.

## 🟢 Build FAISS Index

Build a FAISS index from story bible v11 for semantic search and RAG:

```bash
# Build FAISS index for the Pilot project
python scripts/build_faiss_index_v11.py --project Pilot --source-bible projects/Pilot/story_bible_v11.json

# Use a different embedding model (optional)
python scripts/build_faiss_index_v11.py --project Pilot --source-bible projects/Pilot/story_bible_v11.json --model sentence-transformers/paraphrase-MiniLM-L3-v2
```

This creates:
- `memory/faiss_index/Pilot/index.faiss` - The FAISS vector index
- `memory/faiss_index/Pilot/meta.pkl` - Metadata for each indexed text

✅ Project Milestones
Week 1: Foundation & 3-Episode MVP

GitHub repo & Codespace setup is working.

Basic folder structure (engine/, scripts/, etc.) is created.

requirements.txt is prepared.

Basic CI workflow passes (shows a green check).

run_novel.py MVP successfully generates 3 pilot episodes.

Week 2: Memory System Integration (In Progress)

(Day 8) Neo4j container is running successfully via Docker Compose.

(Day 9-14) Integrate Knowledge Graph (KG) and RAG into the pipeline.

Generated code
---

