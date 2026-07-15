import axios from "axios";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const getOrchestratorRun = async (projectId: number) => {
  const response = await api.get(`/orchestrator/run/${projectId}`);
  return response.data;
};

export const getProjects = async () => {
  const response = await api.get(`/projects/`);
  return response.data;
};