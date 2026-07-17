"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { ThumbsUp, ThumbsDown, ListChecks, Sparkles, Loader2 } from "lucide-react";
import { getRetrospective } from "@/lib/api";

interface RetroData {
  went_well: string[];
  went_wrong: string[];
  action_items: string[];
  error?: string;
}

export default function RetrospectiveCard({ projectId }: { projectId: number }) {
  const [data, setData] = useState<RetroData | null>(null);
  const [loading, setLoading] = useState(false);
  const [generated, setGenerated] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const res = await getRetrospective(projectId);
      setData(res);
      setGenerated(true);
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="glass-card p-6"
    >
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Sparkles size={18} className="text-purple-400" />
          <h3 className="text-white font-semibold">AI Sprint Retrospective</h3>
        </div>
        <button
          onClick={handleGenerate}
          disabled={loading}
          className="text-xs bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white rounded-lg px-3 py-1.5 transition-colors flex items-center gap-1.5"
        >
          {loading ? <Loader2 size={13} className="animate-spin" /> : <Sparkles size={13} />}
          {generated ? "Regenerate" : "Generate"}
        </button>
      </div>

      {!generated && !loading && (
        <p className="text-slate-500 text-sm">
          Click &quot;Generate&quot; to create an AI-powered retrospective for this sprint.
        </p>
      )}

      {data && !data.error && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <div className="flex items-center gap-1.5 text-green-400 text-xs font-medium mb-2">
              <ThumbsUp size={13} /> WENT WELL
            </div>
            <ul className="space-y-1.5">
              {data.went_well.map((item, i) => (
                <li key={i} className="text-sm text-slate-300 bg-green-500/5 rounded-lg px-3 py-2">
                  {item}
                </li>
              ))}
            </ul>
          </div>

          <div>
            <div className="flex items-center gap-1.5 text-red-400 text-xs font-medium mb-2">
              <ThumbsDown size={13} /> WENT WRONG
            </div>
            <ul className="space-y-1.5">
              {data.went_wrong.map((item, i) => (
                <li key={i} className="text-sm text-slate-300 bg-red-500/5 rounded-lg px-3 py-2">
                  {item}
                </li>
              ))}
            </ul>
          </div>

          <div>
            <div className="flex items-center gap-1.5 text-blue-400 text-xs font-medium mb-2">
              <ListChecks size={13} /> ACTION ITEMS
            </div>
            <ul className="space-y-1.5">
              {data.action_items.map((item, i) => (
                <li key={i} className="text-sm text-slate-300 bg-blue-500/5 rounded-lg px-3 py-2">
                  {item}
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {data?.error && (
        <p className="text-amber-400 text-sm">Could not generate retrospective right now. Please try again.</p>
      )}
    </motion.div>
  );
}