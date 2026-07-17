export interface EngineeringData {
  project_id: number;
  project_name: string;
  progress_percentage: number;
  total_tasks: number;
  done_tasks: number;
  blocked_tasks: { id: number; title: string; priority: string }[];
  blocked_task_count: number;
  is_inactive: boolean;
}

export interface RiskData {
  delay_risk: number;
  burnout_risk: number;
  completion_forecast: string;
  features_used: {
    completion_rate: number;
    blocked_ratio: number;
    velocity: number;
    days_to_deadline: number | null;
    avg_workload_ratio: number;
  };
}

export interface PlanningData {
  ranked_tasks: {
    id: number;
    title: string;
    status: string;
    priority: string;
    recommended_action: string;
  }[];
  suggested_sprint_goal: string;
  feasibility: string;
  timeline_adjustment?: {
    original_deadline: string | null;
    suggested_deadline: string | null;
    estimated_days_remaining: number | null;
    adjustment_message: string;
    is_at_risk: boolean;
  };
}

export interface OrchestratorResult {
  project_id: number;
  engineering_data: EngineeringData;
  risk_data: RiskData;
  planning_data: PlanningData;
  qa_data: { total_open_prs: number; high_priority_count: number };
  documentation_data: { answer: string; sources: string[] };
  report_output: { report: string };
  agent_trace: string[];
}