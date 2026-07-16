"use client";

import { motion } from "framer-motion";
import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer, Tooltip, CartesianGrid } from "recharts";
import { EngineeringData } from "@/lib/types";

export default function ProductivityReportCard({
  engineering,
  qa,
}: {
  engineering: EngineeringData;
  qa: { total_open_prs: number; high_priority_count: number };
}) {
  const chartData = [
    { name: "Done", count: engineering.done_tasks },
    { name: "Blocked", count: engineering.blocked_task_count },
    { name: "Total", count: engineering.total_tasks },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="glass-card p-6"
    >
      <h3 className="text-white font-semibold mb-4">Productivity Report</h3>

      <div className="h-40 mb-4">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" vertical={false} />
            <XAxis dataKey="name" stroke="#64748b" fontSize={12} />
            <YAxis stroke="#64748b" fontSize={12} allowDecimals={false} />
            <Tooltip contentStyle={{ background: "#131a29", border: "1px solid #1f2937", borderRadius: 8 }} />
            <Bar dataKey="count" fill="#3b82f6" radius={[6, 6, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div className="bg-white/5 rounded-lg p-3">
          <p className="text-xs text-slate-500">Open PRs</p>
          <p className="text-xl font-semibold text-white">{qa.total_open_prs}</p>
        </div>
        <div className="bg-white/5 rounded-lg p-3">
          <p className="text-xs text-slate-500">High Priority Reviews</p>
          <p className="text-xl font-semibold text-white">{qa.high_priority_count}</p>
        </div>
      </div>
    </motion.div>
  );
}