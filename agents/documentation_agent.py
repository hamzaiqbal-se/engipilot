from shared.gemini_client import generate_text
from shared.vector_store import search_documents, add_document
import logging

logger = logging.getLogger("engipilot")


def index_project_documents():
    """
    Indexes core project documentation into ChromaDB.
    In a real setup, this would read actual files (README, case study docs, etc.)
    For now, we index key architectural facts about EngiPilot itself.
    """
    documents = {
        "doc_architecture": "EngiPilot uses a multi-agent architecture orchestrated by LangGraph. Each agent specializes in one engineering management task: Engineering Agent tracks progress, Risk Agent predicts delays, Planning Agent prioritizes tasks, QA Agent scores PR review urgency, and Documentation Agent answers questions using RAG.",
        "doc_risk_agent": "The Risk Agent uses two XGBoost regression models trained on synthetic data to predict delay risk and burnout risk. Models were tuned using RandomizedSearchCV and validated with 5-fold cross-validation to avoid overfitting.",
        "doc_tech_stack": "EngiPilot's tech stack includes FastAPI for the backend, PostgreSQL for structured data, Redis for caching, ChromaDB for vector storage, and Docker Compose for local infrastructure. Database migrations are managed with Alembic.",
        "doc_planning_agent": "The Planning Agent ranks pending tasks by priority and status, and adjusts its sprint feasibility recommendation based on the Risk Agent's delay_risk score. High delay risk triggers a recommendation to reduce sprint scope and focus on unblocking tasks.",
    }

    for doc_id, text in documents.items():
        add_document(doc_id, text, metadata={"source": "engipilot_docs"})

    logger.info(f"Indexed {len(documents)} project documents into vector store")
    return {"indexed_count": len(documents)}


def run_documentation_agent(query: str) -> dict:
    """
    Documentation Agent:
    - Retrieves relevant documents from ChromaDB based on the query
    - Uses Gemini to generate a coherent answer grounded in those documents
    Returns a dict matching the 'documentation_data' schema field.
    """

    try:
        results = search_documents(query, n_results=3)
    except Exception as e:
        logger.info(f"Documentation Agent: Gemini generation failed — {e}")
        return {"query": query, "answer": f"Sorry, I couldn't generate an answer right now.", "sources": []}

    retrieved_docs = results.get("documents", [[]])[0]
    retrieved_ids = results.get("ids", [[]])[0]

    if not retrieved_docs:
        return {
            "query": query,
            "answer": "No relevant documentation found for this query.",
            "sources": [],
        }

    context = "\n\n".join(retrieved_docs)

    prompt = f"""You are a technical documentation assistant for a software project called EngiPilot.
Answer the user's question using ONLY the context provided below. Be concise (2-4 sentences).
If the context doesn't contain enough information, say so clearly.

Context:
{context}

Question: {query}

Answer:"""

    try:
        answer = generate_text(prompt)
    except Exception as e:
        logger.info(f"Documentation Agent: Gemini generation failed — {e}")
        return {"error": f"LLM generation failed: {str(e)}"}

    result = {
        "query": query,
        "answer": answer,
        "sources": retrieved_ids,
    }

    logger.info(f"Documentation Agent answered query='{query}' using sources={retrieved_ids}")
    return result