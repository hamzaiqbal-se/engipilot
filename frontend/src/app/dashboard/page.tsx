"use client";

import { useEffect, useState } from "react";
import Sidebar from "@/components/Sidebar";
import HealthCard from "@/components/HealthCard";
import SprintReportCard from "@/components/SprintReportCard";
import RiskReportCard from "@/components/RiskReportCard";
import ProductivityReportCard from "@/components/ProductivityReportCard";
import TeamPerformanceCard from "@/components/TeamPerformanceCard";
import { getProjects, getOrchestratorRun, getProjectSprints } from "@/lib/api";
import { OrchestratorResult } from "@/lib/types";
import { AnimatePresence, motion } from "framer-motion";
import AskEngiPilot from "@/components/AskEngiPilot";
import AgentPipeline3D from "@/components/AgentPipeline3D";
import CommandPalette from "@/components/CommandPalette";
import RetrospectiveCard from "@/components/RetrospectiveCard";
import NewProjectModal from "@/components/NewProjectModal";
import AddTaskModal from "@/components/AddTaskModal";
import AddSprintModal from "@/components/AddSprintModal";
import ExecutiveDashboard from "@/components/ExecutiveDashboard";

interface SprintOption {
  id: number;
  sprint_number: number;
  goal: string | null;
}

export default function Dashboard() {
  const [projects, setProjects] = useState<{ id: number; name: string }[]>([]);
  const [selectedProject, setSelectedProject] = useState<number | null>(null);
  const [data, setData] = useState<OrchestratorResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeView, setActiveView] = useState("Sprint Report");
  const [sprints, setSprints] = useState<SprintOption[]>([]);

  const refreshProjects = () => {
    getProjects().then((res) => {
      setProjects(res);
      if (res.length > 0 && selectedProject === null) {
        setSelectedProject(res[0].id);
      }
    });
  };

  const refreshSprints = () => {
    if (selectedProject === null) return;
    getProjectSprints(selectedProject).then(setSprints);
  };

  const refreshOrchestratorData = () => {
    if (selectedProject === null) return;
    getOrchestratorRun(selectedProject).then(setData);
  };

  useEffect(() => {
    refreshProjects();
  }, []);

  useEffect(() => {
    if (selectedProject === null) return;
    setLoading(true);
    getOrchestratorRun(selectedProject)
      .then((res) => setData(res))
      .finally(() => setLoading(false));
    refreshSprints();
  }, [selectedProject]);

  const latestSprintId = sprints[0]?.id ?? null;
  const nextSprintNumber = sprints.length > 0 ? sprints[0].sprint_number + 1 : 1;

  return (
    <div className="flex flex-col md:flex-row min-h-screen">
      <Sidebar active={activeView} onSelect={setActiveView} />
      <CommandPalette onSelect={setActiveView} />

      <main className="flex-1 p-4 md:p-8 overflow-x-hidden">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
          <h2 className="text-xl md:text-2xl font-bold text-white">
            {activeView === "Executive" ? "Executive Dashboard" : "Manager Dashboard"}
          </h2>
          {activeView !== "Executive" && (
            <div className="flex items-center gap-3 w-full sm:w-auto">
              <select
                value={selectedProject ?? ""}
                onChange={(e) => setSelectedProject(Number(e.target.value))}
                className="bg-[var(--surface-solid)] border border-[var(--border)] text-white text-sm rounded-lg px-3 py-2 flex-1 sm:flex-none"
              >
                {projects.map((p) => (
                  <option key={p.id} value={p.id} style={{ background: "#131a29", color: "#f1f5f9" }}>
                    {p.name}
                  </option>
                ))}
              </select>
              <NewProjectModal onCreated={refreshProjects} />
            </div>
          )}
        </div>

        {activeView === "Executive" ? (
          <ExecutiveDashboard />
        ) : (
          <>
            {loading && <p className="text-slate-500">Loading agent data...</p>}

            {data && !loading && (
              <AnimatePresence mode="wait">
                <motion.div
                  key={activeView}
                  initial={{ opacity: 0, x: 8 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -8 }}
                  transition={{ duration: 0.25 }}
                  className="space-y-4 md:space-y-6"
                >
                  {(activeView === "Overview" || activeView === "Sprint Report") && (
                    <HealthCard
                      status={data.risk_data.completion_forecast}
                      projectName={data.engineering_data.project_name}
                    />
                  )}

                  {activeView === "Sprint Report" && (
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 md:gap-6">
                      <SprintReportCard engineering={data.engineering_data} planning={data.planning_data} />
                      <RiskReportCard risk={data.risk_data} />
                    </div>
                  )}

                  {activeView === "Risk Report" && (
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 md:gap-6">
                      <RiskReportCard risk={data.risk_data} />
                      <ProductivityReportCard engineering={data.engineering_data} qa={data.qa_data} />
                    </div>
                  )}

                  {activeView === "Team Performance" && selectedProject !== null && (
                    <div className="space-y-4">
                      <div className="flex justify-end gap-2">
                        <AddSprintModal
                          projectId={selectedProject}
                          nextSprintNumber={nextSprintNumber}
                          onCreated={refreshSprints}
                        />
                        <AddTaskModal
                          sprints={sprints}
                          defaultSprintId={latestSprintId}
                          onCreated={refreshOrchestratorData}
                        />
                      </div>
                      <TeamPerformanceCard planning={data.planning_data} engineering={data.engineering_data} />
                    </div>
                  )}

                  {activeView === "Overview" && (
                    <div className="space-y-4 md:space-y-6">
                      <AgentPipeline3D agentTrace={data.agent_trace} />
                      <AskEngiPilot />
                      <RetrospectiveCard projectId={selectedProject!} />
                      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 md:gap-6">
                        <SprintReportCard engineering={data.engineering_data} planning={data.planning_data} />
                        <RiskReportCard risk={data.risk_data} />
                      </div>
                    </div>
                  )}
                </motion.div>
              </AnimatePresence>
            )}
          </>
        )}
      </main>
    </div>
  );
}