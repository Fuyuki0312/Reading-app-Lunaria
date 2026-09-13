from app.config import Config

import chromadb


config = Config()

client = chromadb.PersistentClient(
    path=str(config.CHROMA_DB_PATH)
)

collection = client.get_or_create_collection(
    name="books",
    configuration={
        "hnsw": {
            "space": "cosine"
        }
    }
)
