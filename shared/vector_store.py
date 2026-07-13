import chromadb
from sentence_transformers import SentenceTransformer
import logging

logger = logging.getLogger("engipilot")

_chroma_client = None
_embedding_model = None
_collection = None


def _get_client():
    global _chroma_client
    if _chroma_client is None:
        _chroma_client = chromadb.HttpClient(host="localhost", port=8001)
    return _chroma_client


def _get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedding_model


def get_collection():
    global _collection
    if _collection is None:
        client = _get_client()
        _collection = client.get_or_create_collection(name="engipilot_docs")
    return _collection


def add_document(doc_id: str, text: str, metadata: dict = None):
    """Embeds and stores a document in ChromaDB."""
    model = _get_embedding_model()
    collection = get_collection()

    embedding = model.encode(text).tolist()

    final_metadata = metadata if metadata else {"source": "engipilot"}

    collection.add(
        ids=[doc_id],
        embeddings=[embedding],
        documents=[text],
        metadatas=[final_metadata],
    )
    logger.info(f"Added document to vector store: doc_id={doc_id}")


def search_documents(query: str, n_results: int = 3):
    """Searches for documents similar to the query."""
    model = _get_embedding_model()
    collection = get_collection()

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )
    logger.info(f"Vector search for query='{query}' returned {len(results.get('ids', [[]])[0])} results")
    return results