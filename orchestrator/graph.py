from langgraph.graph import StateGraph, END
from sqlalchemy.orm import Session
from shared.state_schema import ProjectState
from agents.engineering_agent import run_engineering_agent
from agents.risk_agent import run_risk_agent
from agents.planning_agent import run_planning_agent
from agents.qa_agent import run_qa_agent
from agents.documentation_agent import run_documentation_agent
from agents.reporting_agent import run_reporting_agent
import logging

logger = logging.getLogger("engipilot")


# --- Real agent nodes: Engineering, Risk, and Planning are now fully implemented ---
# --- Remaining stubs for QA, Documentation, and Reporting agents will be added as they're built ---

def engineering_node(state: ProjectState, db: Session) -> ProjectState:
    result = run_engineering_agent(state["project_id"], db)
    state["engineering_data"] = result
    state.setdefault("agent_trace", []).append("engineering_agent")
    logger.info(f"Orchestrator: engineering_node completed for project_id={state['project_id']}")
    return state


def risk_node(state: ProjectState, db: Session) -> ProjectState:
    result = run_risk_agent(state["project_id"], db)
    state["risk_data"] = result
    state.setdefault("agent_trace", []).append("risk_agent")
    logger.info(f"Orchestrator: risk_node completed for project_id={state['project_id']}")
    return state


def planning_node(state: ProjectState, db: Session) -> ProjectState:
    risk_data = state.get("risk_data")
    result = run_planning_agent(state["project_id"], db, risk_data=risk_data)
    state["planning_data"] = result
    state.setdefault("agent_trace", []).append("planning_agent")
    logger.info(f"Orchestrator: planning_node completed for project_id={state['project_id']}")
    return state


def build_orchestrator_graph(db: Session):
    """
    Builds and compiles the LangGraph orchestrator.
    Currently wires: Engineering -> Risk -> Planning
    """
    graph = StateGraph(ProjectState)

    graph.add_node("engineering", lambda state: engineering_node(state, db))
    graph.add_node("risk", lambda state: risk_node(state, db))
    graph.add_node("planning", lambda state: planning_node(state, db))
    graph.add_node("qa", lambda state: qa_node(state, db))
    graph.add_node("documentation", lambda state: documentation_node(state, db))
    graph.add_node("reporting", lambda state: reporting_node(state, db))

    graph.set_entry_point("engineering")
    graph.add_edge("engineering", "risk")
    graph.add_edge("risk", "planning")
    graph.add_edge("planning", "qa")
    graph.add_edge("qa", "documentation")
    graph.add_edge("documentation", "reporting")
    graph.add_edge("reporting", END)

    return graph.compile()


def run_orchestrator(project_id: int, db: Session) -> ProjectState:
    """Entry point: runs the full agent chain for a given project."""
    compiled_graph = build_orchestrator_graph(db)

    initial_state: ProjectState = {
        "project_id": project_id,
        "request_type": "full_analysis",
        "agent_trace": [],
    }

    final_state = compiled_graph.invoke(initial_state)
    logger.info(f"Orchestrator run complete for project_id={project_id}. Trace: {final_state.get('agent_trace')}")
    return final_state

def qa_node(state: ProjectState, db: Session) -> ProjectState:
    result = run_qa_agent()
    state["qa_data"] = result
    state.setdefault("agent_trace", []).append("qa_agent")
    logger.info(f"Orchestrator: qa_node completed for project_id={state['project_id']}")
    return state

def documentation_node(state: ProjectState, db: Session) -> ProjectState:
    query = "What is the architecture and tech stack of this project?"
    result = run_documentation_agent(query)
    state["documentation_data"] = result
    state.setdefault("agent_trace", []).append("documentation_agent")
    logger.info(f"Orchestrator: documentation_node completed for project_id={state['project_id']}")
    return state

def reporting_node(state: ProjectState, db: Session) -> ProjectState:
    result = run_reporting_agent(state)
    state["report_output"] = result
    state.setdefault("agent_trace", []).append("reporting_agent")
    logger.info(f"Orchestrator: reporting_node completed for project_id={state['project_id']}")
    return state