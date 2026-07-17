"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, Plus, Loader2, CheckCircle2 } from "lucide-react";
import { createSprint } from "@/lib/api";

export default function AddSprintModal({
  projectId,
  nextSprintNumber,
  onCreated,
}: {
  projectId: number;
  nextSprintNumber: number;
  onCreated: () => void;
}) {
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState("");
  const [goal, setGoal] = useState("");

  const resetAndClose = () => {
    setOpen(false);
    setSuccess(false);
    setError("");
    setGoal("");
  };

  const handleSubmit = async () => {
    setError("");
    setLoading(true);
    try {
      await createSprint({
        project_id: projectId,
        sprint_number: nextSprintNumber,
        goal: goal || undefined,
      });
      setSuccess(true);
      onCreated();
      setTimeout(resetAndClose, 1000);
    } catch {
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <button
        onClick={() => setOpen(true)}
        className="flex items-center gap-1.5 text-xs bg-white/5 hover:bg-white/10 border border-[var(--border)] text-slate-300 rounded-lg px-3 py-1.5 transition-colors"
      >
        <Plus size={13} /> New Sprint
      </button>

      <AnimatePresence>
        {open && (
          <div className="fixed inset-0 bg-black/70 z-[90] flex items-center justify-center p-4" onClick={resetAndClose}>
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="glass-card p-6 w-full max-w-md"
              onClick={(e) => e.stopPropagation()}
            >
              {success ? (
                <div className="flex flex-col items-center py-8 gap-3">
                  <CheckCircle2 size={40} className="text-green-400" />
                  <p className="text-white font-medium">Sprint {nextSprintNumber} created!</p>
                </div>
              ) : (
                <>
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-white font-semibold">New Sprint — #{nextSprintNumber}</h3>
                    <button onClick={resetAndClose} className="text-slate-400"><X size={18} /></button>
                  </div>

                  <div>
                    <label className="text-xs text-slate-500">Sprint Goal (optional)</label>
                    <input
                      value={goal}
                      onChange={(e) => setGoal(e.target.value)}
                      className="w-full mt-1 bg-white/5 border border-[var(--border)] text-white text-sm rounded-lg px-3 py-2 outline-none focus:border-blue-500/50"
                      placeholder="e.g. Complete user authentication flow"
                    />
                  </div>

                  {error && <p className="text-red-400 text-xs mt-3">{error}</p>}

                  <button
                    onClick={handleSubmit}
                    disabled={loading}
                    className="w-full mt-5 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white rounded-lg py-2.5 text-sm font-medium transition-colors flex items-center justify-center gap-2"
                  >
                    {loading ? <Loader2 size={15} className="animate-spin" /> : <Plus size={15} />}
                    Create Sprint
                  </button>
                </>
              )}
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </>
  );
}