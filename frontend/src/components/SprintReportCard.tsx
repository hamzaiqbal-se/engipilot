"use client";

import { motion } from "framer-motion";
import { PlanningData, EngineeringData } from "@/lib/types";
import { Calendar, TrendingUp, TrendingDown } from "lucide-react";

export default function SprintReportCard({
  engineering,
  planning,
}: {
  engineering: EngineeringData;
  planning: PlanningData;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: 0.1 }}
      className="glass-card p-6"
    >
      <h3 className="text-white font-semibold mb-4">Weekly Sprint Report</h3>

      <div className="flex items-center gap-4 mb-4">
        <div className="flex-1 h-2 bg-slate-800 rounded-full overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${engineering.progress_percentage}%` }}
            transition={{ duration: 0.8, delay: 0.3 }}
            className="h-full bg-blue-500 rounded-full"
          />
        </div>
        <span className="text-white font-medium">{engineering.progress_percentage}%</span>
      </div>

      <p className="text-slate-400 text-sm mb-4">
        {engineering.done_tasks} of {engineering.total_tasks} tasks complete
      </p>

      <div className="border-t border-[var(--border)] pt-4">
        <p className="text-xs text-slate-500 uppercase mb-2">Suggested Sprint Goal</p>
        <p className="text-slate-200 text-sm">{planning.suggested_sprint_goal}</p>
      </div>

      {planning.timeline_adjustment && planning.timeline_adjustment.suggested_deadline && (
        <div className="border-t border-[var(--border)] pt-4 mt-4">
          <div className="flex items-center gap-1.5 text-xs text-slate-500 uppercase mb-2">
            <Calendar size={12} /> Timeline Forecast
          </div>
          <div className="flex items-center justify-between text-sm">
            <div>
              <p className="text-slate-500 text-xs">Original Deadline</p>
              <p className="text-slate-300">
                {planning.timeline_adjustment.original_deadline
                  ? new Date(planning.timeline_adjustment.original_deadline).toLocaleDateString()
                  : "Not set"}
              </p>
            </div>
            <div className={planning.timeline_adjustment.is_at_risk ? "text-red-400" : "text-green-400"}>
              {planning.timeline_adjustment.is_at_risk ? <TrendingDown size={18} /> : <TrendingUp size={18} />}
            </div>
            <div className="text-right">
              <p className="text-slate-500 text-xs">Projected Completion</p>
              <p className={planning.timeline_adjustment.is_at_risk ? "text-red-400" : "text-green-400"}>
                {new Date(planning.timeline_adjustment.suggested_deadline).toLocaleDateString()}
              </p>
            </div>
          </div>
          <p className="text-xs text-slate-500 mt-2">{planning.timeline_adjustment.adjustment_message}</p>
        </div>
      )}

      <div className="mt-4 space-y-2">
        {planning.ranked_tasks.slice(0, 4).map((task) => (
          <div key={task.id} className="flex items-center justify-between text-sm py-1.5 px-3 rounded-lg bg-white/5">
            <span className="text-slate-300">{task.title}</span>
            <span
              className={`text-xs px-2 py-0.5 rounded-full ${
                task.status === "blocked"
                  ? "bg-red-500/20 text-red-400"
                  : task.status === "in_progress"
                  ? "bg-blue-500/20 text-blue-400"
                  : "bg-slate-500/20 text-slate-400"
              }`}
            >
              {task.status}
            </span>
          </div>
        ))}
      </div>
    </motion.div>
  );
}