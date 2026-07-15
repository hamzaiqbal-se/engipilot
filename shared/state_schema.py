from typing import TypedDict, Optional, List, Dict, Any


class ProjectState(TypedDict, total=False):
    project_id: int
    request_type: str

    # Filled by Engineering Agent
    engineering_data: Optional[Dict[str, Any]]

    # Filled by Risk Agent
    risk_data: Optional[Dict[str, Any]]

    # Filled by other agents (Week 2-3)
    qa_data: Optional[Dict[str, Any]]
    planning_data: Optional[Dict[str, Any]]
    documentation_data: Optional[Dict[str, Any]]
    report_output: Optional[str]

    # Trace log — tracks which agents ran, in what order
    agent_trace: List[str]

    # Filled by Automation Agent
    automation_data: Optional[Dict[str, Any]]