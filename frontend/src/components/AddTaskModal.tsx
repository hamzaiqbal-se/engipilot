"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, Plus, Loader2, CheckCircle2 } from "lucide-react";
import { createTask } from "@/lib/api";

const STATUS_OPTIONS = ["todo", "in_progress", "blocked", "done"];
const PRIORITY_OPTIONS = ["low", "medium", "high"];

export default function AddTaskModal({ sprintId, onCreated }: { sprintId: number | null; onCreated: () => void }) {
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState("");
  const [form, setForm] = useState({ title: "", status: "todo", priority: "medium" });

  const resetAndClose = () => {
    setOpen(false);
    setSuccess(false);
    setError("");
    setForm({ title: "", status: "todo", priority: "medium" });
  };

  const handleSubmit = async () => {
    if (!form.title.trim()) {
      setError("Task title is required.");
      return;
    }
    if (!sprintId) {
      setError("No active sprint found for this project.");
      return;
    }
    setError("");
    setLoading(true);
    try {
      await createTask({ sprint_id: sprintId, title: form.title, status: form.status, priority: form.priority });
      setSuccess(true);
      onCreated();
      setTimeout(resetAndClose, 1000);
    } catch {
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const optionStyle = { background: "#131a29", color: "#f1f5f9" };

  return (
    <>
      <button
        onClick={() => setOpen(true)}
        className="flex items-center gap-1.5 text-xs bg-white/5 hover:bg-white/10 border border-[var(--border)] text-slate-300 rounded-lg px-3 py-1.5 transition-colors"
      >
        <Plus size={13} /> Add Task
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
                  <p className="text-white font-medium">Task added successfully!</p>
                </div>
              ) : (
                <>
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-white font-semibold">Add Task</h3>
                    <button onClick={resetAndClose} className="text-slate-400"><X size={18} /></button>
                  </div>

                  <div className="space-y-3">
                    <div>
                      <label className="text-xs text-slate-500">Task Title *</label>
                      <input
                        value={form.title}
                        onChange={(e) => setForm({ ...form, title: e.target.value })}
                        className="w-full mt-1 bg-white/5 border border-[var(--border)] text-white text-sm rounded-lg px-3 py-2 outline-none focus:border-blue-500/50"
                        placeholder="e.g. Fix login bug"
                      />
                    </div>

                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <label className="text-xs text-slate-500">Status</label>
                        <select
                          value={form.status}
                          onChange={(e) => setForm({ ...form, status: e.target.value })}
                          className="w-full mt-1 bg-white/5 border border-[var(--border)] text-white text-sm rounded-lg px-3 py-2 outline-none focus:border-blue-500/50"
                        >
                          {STATUS_OPTIONS.map((s) => (
                            <option key={s} value={s} style={optionStyle}>{s}</option>
                          ))}
                        </select>
                      </div>

                      <div>
                        <label className="text-xs text-slate-500">Priority</label>
                        <select
                          value={form.priority}
                          onChange={(e) => setForm({ ...form, priority: e.target.value })}
                          className="w-full mt-1 bg-white/5 border border-[var(--border)] text-white text-sm rounded-lg px-3 py-2 outline-none focus:border-blue-500/50"
                        >
                          {PRIORITY_OPTIONS.map((p) => (
                            <option key={p} value={p} style={optionStyle}>{p}</option>
                          ))}
                        </select>
                      </div>
                    </div>
                  </div>

                  {error && <p className="text-red-400 text-xs mt-3">{error}</p>}

                  <button
                    onClick={handleSubmit}
                    disabled={loading}
                    className="w-full mt-5 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white rounded-lg py-2.5 text-sm font-medium transition-colors flex items-center justify-center gap-2"
                  >
                    {loading ? <Loader2 size={15} className="animate-spin" /> : <Plus size={15} />}
                    Add Task
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