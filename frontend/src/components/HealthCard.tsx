"use client";

import { motion } from "framer-motion";

const statusConfig: Record<string, { color: string; bg: string; label: string }> = {
  "On Track": { color: "#22c55e", bg: "rgba(34,197,94,0.1)", label: "🟢 On Track" },
  "Needs Attention": { color: "#f59e0b", bg: "rgba(245,158,11,0.1)", label: "🟡 Needs Attention" },
  "At Risk": { color: "#ef4444", bg: "rgba(239,68,68,0.1)", label: "🔴 At Risk" },
};

export default function HealthCard({ status, projectName }: { status: string; projectName: string }) {
  const config = statusConfig[status] || statusConfig["Needs Attention"];

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="glass-card p-8"
      style={{ borderColor: config.color + "40" }}
    >
      <p className="text-sm text-slate-400 mb-2">{projectName}</p>
      <div className="flex items-baseline gap-3">
        <span className="text-3xl sm:text-4xl md:text-5xl font-bold" style={{ color: config.color }}>
          {config.label.split(" ").slice(1).join(" ")}
        </span>
      </div>
      <p className="text-slate-500 text-sm mt-2">Overall Project Health</p>
    </motion.div>
  );
}