"use client";

import { motion } from "framer-motion";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";
import { RiskData } from "@/lib/types";

export default function RiskReportCard({ risk }: { risk: RiskData }) {
  const f = risk.features_used;

  // Explainable breakdown: approximate contribution of each factor to delay_risk
  const breakdown = [
    { name: "Blocked Tasks", value: Math.round(f.blocked_ratio * 100), color: "#ef4444" },
    { name: "Low Completion", value: Math.round((1 - f.completion_rate) * 100), color: "#f59e0b" },
    { name: "Deadline Pressure", value: f.days_to_deadline !== null && f.days_to_deadline < 5 ? 30 : 5, color: "#8b5cf6" },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: 0.2 }}
      className="glass-card p-6"
    >
      <h3 className="text-white font-semibold mb-1">Project Risk Report</h3>
      <p className="text-slate-500 text-xs mb-4">{risk.completion_forecast}</p>

      <div className="flex items-center gap-6">
        <div className="w-32 h-32">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={breakdown}
                dataKey="value"
                innerRadius={35}
                outerRadius={55}
                paddingAngle={4}
              >
                {breakdown.map((entry, i) => (
                  <Cell key={i} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{ background: "#131a29", border: "1px solid #1f2937", borderRadius: 8 }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="flex-1 space-y-2">
          {breakdown.map((item) => (
            <div key={item.name} className="flex items-center justify-between text-sm">
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full" style={{ background: item.color }} />
                <span className="text-slate-300">{item.name}</span>
              </div>
              <span className="text-slate-400">{item.value}%</span>
            </div>
          ))}
        </div>
      </div>

      <div className="mt-4 pt-4 border-t border-[var(--border)] flex justify-between text-sm">
        <span className="text-slate-400">Delay Risk</span>
        <span className="text-white font-medium">{(risk.delay_risk * 100).toFixed(0)}%</span>
      </div>
      <div className="flex justify-between text-sm mt-1">
        <span className="text-slate-400">Burnout Risk</span>
        <span className="text-white font-medium">{(risk.burnout_risk * 100).toFixed(0)}%</span>
      </div>
    </motion.div>
  );
}