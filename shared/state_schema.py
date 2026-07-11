from typing import TypedDict, Optional, List, Dict, Any


class ProjectState(TypedDict, total=False):
    project_id: int
    request_type: str

    # Filled by Engineering Agent
    engineering_data: Optional[Dict[str, Any]]

    # Filled by other agents later (Week 2-3)
    risk_data: Optional[Dict[str, Any]]
    qa_data: Optional[Dict[str, Any]]
    planning_data: Optional[Dict[str, Any]]
    documentation_data: Optional[Dict[str, Any]]
    report_output: Optional[str]

    # Trace log
    agent_trace: List[str]