import axios from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { "Content-Type": "application/json" },
});

export const getProjects = async () => {
  const res = await api.get(`/projects/`);
  return res.data;
};

export const getOrchestratorRun = async (projectId: number) => {
  const res = await api.get(`/orchestrator/run/${projectId}`);
  return res.data;
};

export const askDocumentation = async (query: string) => {
  const res = await api.get(`/agents/documentation/query`, { params: { query } });
  return res.data;
};

export const getRetrospective = async (projectId: number) => {
  const res = await api.get(`/agents/retrospective/${projectId}`);
  return res.data;
};

export const createProject = async (data: {
  name: string;
  technology: string;
  status?: string;
  deadline?: string;
  github_repo?: string;
}) => {
  const res = await api.post(`/projects/`, data);
  return res.data;
};

export const createSprint = async (data: {
  project_id: number;
  sprint_number: number;
  goal?: string;
}) => {
  const res = await api.post(`/sprints/`, data);
  return res.data;
};

export const createTask = async (data: {
  sprint_id: number;
  title: string;
  status?: string;
  priority?: string;
}) => {
  const res = await api.post(`/tasks/`, data);
  return res.data;
};