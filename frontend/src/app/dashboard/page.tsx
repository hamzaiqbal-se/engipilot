"use client";

import { useEffect, useState } from "react";
import Sidebar from "@/components/Sidebar";
import HealthCard from "@/components/HealthCard";
import SprintReportCard from "@/components/SprintReportCard";
import RiskReportCard from "@/components/RiskReportCard";
import { getProjects, getOrchestratorRun } from "@/lib/api";
import { OrchestratorResult } from "@/lib/types";

export default function Dashboard() {
  const [projects, setProjects] = useState<{ id: number; name: string }[]>([]);
  const [selectedProject, setSelectedProject] = useState<number | null>(null);
  const [data, setData] = useState<OrchestratorResult | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    getProjects().then((res) => {
      setProjects(res);
      if (res.length > 0) setSelectedProject(res[0].id);
    });
  }, []);

  useEffect(() => {
    if (selectedProject === null) return;
    setLoading(true);
    getOrchestratorRun(selectedProject)
      .then((res) => setData(res))
      .finally(() => setLoading(false));
  }, [selectedProject]);

  return (
    <div className="flex flex-col md:flex-row min-h-screen">
      <Sidebar active="Sprint Report" onSelect={() => {}} />

      <main className="flex-1 p-4 md:p-8 overflow-x-hidden">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
          <h2 className="text-xl md:text-2xl font-bold text-white">Manager Dashboard</h2>
          <select
            value={selectedProject ?? ""}
            onChange={(e) => setSelectedProject(Number(e.target.value))}
            className="bg-[var(--surface-solid)] border border-[var(--border)] text-white text-sm rounded-lg px-3 py-2 w-full sm:w-auto"
          >
            {projects.map((p) => (
              <option key={p.id} value={p.id}>{p.name}</option>
            ))}
          </select>
        </div>

        {loading && <p className="text-slate-500">Loading agent data...</p>}

        {data && !loading && (
          <div className="space-y-4 md:space-y-6">
            <HealthCard
              status={data.risk_data.completion_forecast}
              projectName={data.engineering_data.project_name}
            />
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 md:gap-6">
              <SprintReportCard engineering={data.engineering_data} planning={data.planning_data} />
              <RiskReportCard risk={data.risk_data} />
            </div>
          </div>
        )}
      </main>
    </div>
  );
}