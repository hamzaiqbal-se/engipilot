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