"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Crown, TrendingUp, AlertTriangle, Loader2 } from "lucide-react";
import { getExecutiveSummary } from "@/lib/api";

interface ProjectSummary {
  project_id: number;
  project_name: string;
  technology: string;
  progress_percentage: number;
  delay_risk: number;
  completion_forecast: string;
  blocked_task_count: number;
}

interface ExecutiveSummary {
  total_projects: number;
  at_risk_count: number;
  needs_attention_count: number;
  on_track_count: number;
  avg_progress: number;
  avg_delay_risk: number;
  projects: ProjectSummary[];
}

const statusColor: Record<string, string> = {
  "On Track": "#22c55e",
  "Needs Attention": "#f59e0b",
  "At Risk": "#ef4444",
};

export default function ExecutiveDashboard() {
  const [summary, setSummary] = useState<ExecutiveSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getExecutiveSummary()
      .then(setSummary)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="glass-card p-12 flex items-center justify-center">
        <Loader2 className="animate-spin text-slate-500" size={24} />
      </div>
    );
  }

  if (!summary) return null;

  return (
    <div className="space-y-4 md:space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="glass-card p-6"
      >
        <div className="flex items-center gap-2 mb-4">
          <Crown size={18} className="text-amber-400" />
          <h3 className="text-white font-semibold">Organization Overview</h3>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          <div className="bg-white/5 rounded-lg p-4 text-center">
            <p className="text-2xl font-bold text-white">{summary.total_projects}</p>
            <p className="text-xs text-slate-500 mt-1">Total Projects</p>
          </div>
          <div className="bg-green-500/10 rounded-lg p-4 text-center">
            <p className="text-2xl font-bold text-green-400">{summary.on_track_count}</p>
            <p className="text-xs text-slate-500 mt-1">On Track</p>
          </div>
          <div className="bg-amber-500/10 rounded-lg p-4 text-center">
            <p className="text-2xl font-bold text-amber-400">{summary.needs_attention_count}</p>
            <p className="text-xs text-slate-500 mt-1">Needs Attention</p>
          </div>
          <div className="bg-red-500/10 rounded-lg p-4 text-center">
            <p className="text-2xl font-bold text-red-400">{summary.at_risk_count}</p>
            <p className="text-xs text-slate-500 mt-1">At Risk</p>
          </div>
          <div className="bg-blue-500/10 rounded-lg p-4 text-center">
            <p className="text-2xl font-bold text-blue-400">{summary.avg_progress}%</p>
            <p className="text-xs text-slate-500 mt-1">Avg Progress</p>
          </div>
        </div>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.1 }}
        className="glass-card p-6"
      >
        <h3 className="text-white font-semibold mb-4">Portfolio Comparison</h3>

        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-slate-500 text-xs uppercase border-b border-[var(--border)]">
                <th className="pb-2 pr-4">Project</th>
                <th className="pb-2 pr-4">Tech</th>
                <th className="pb-2 pr-4">Progress</th>
                <th className="pb-2 pr-4">Delay Risk</th>
                <th className="pb-2 pr-4">Blocked</th>
                <th className="pb-2">Status</th>
              </tr>
            </thead>
            <tbody>
              {summary.projects.map((p) => (
                <tr key={p.project_id} className="border-b border-[var(--border)] last:border-0">
                  <td className="py-3 pr-4 text-slate-200">{p.project_name}</td>
                  <td className="py-3 pr-4 text-slate-400">{p.technology}</td>
                  <td className="py-3 pr-4 text-slate-300">{p.progress_percentage}%</td>
                  <td className="py-3 pr-4 text-slate-300">{(p.delay_risk * 100).toFixed(0)}%</td>
                  <td className="py-3 pr-4 text-slate-300">{p.blocked_task_count}</td>
                  <td className="py-3">
                    <span
                      className="text-xs px-2 py-0.5 rounded-full"
                      style={{
                        background: (statusColor[p.completion_forecast] || "#64748b") + "22",
                        color: statusColor[p.completion_forecast] || "#64748b",
                      }}
                    >
                      {p.completion_forecast}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </motion.div>
    </div>
  );
}