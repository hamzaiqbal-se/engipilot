"use client";

import { motion } from "framer-motion";
import { PlanningData, EngineeringData } from "@/lib/types";
import { CheckCircle2, AlertCircle, Clock } from "lucide-react";

export default function TeamPerformanceCard({
  planning,
  engineering,
}: {
  planning: PlanningData;
  engineering: EngineeringData;
}) {
  const statusIcon = (status: string) => {
    if (status === "blocked") return <AlertCircle size={16} className="text-red-400" />;
    if (status === "in_progress") return <Clock size={16} className="text-blue-400" />;
    return <CheckCircle2 size={16} className="text-slate-500" />;
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="glass-card p-6"
    >
      <h3 className="text-white font-semibold mb-1">Team Performance Analysis</h3>
      <p className="text-slate-500 text-xs mb-4">
        {engineering.is_inactive ? "No recent activity detected" : "Active development"}
      </p>

      <div className="space-y-2">
        {planning.ranked_tasks.map((task, i) => (
          <motion.div
            key={task.id}
            initial={{ opacity: 0, x: -8 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.05 }}
            className="flex items-center gap-3 py-2.5 px-3 rounded-lg bg-white/5"
          >
            {statusIcon(task.status)}
            <div className="flex-1 min-w-0">
              <p className="text-slate-200 text-sm truncate">{task.title}</p>
              <p className="text-slate-500 text-xs">{task.recommended_action}</p>
            </div>
            <span
              className={`text-xs px-2 py-0.5 rounded-full shrink-0 ${
                task.priority === "high"
                  ? "bg-red-500/20 text-red-400"
                  : task.priority === "medium"
                  ? "bg-amber-500/20 text-amber-400"
                  : "bg-slate-500/20 text-slate-400"
              }`}
            >
              {task.priority}
            </span>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}