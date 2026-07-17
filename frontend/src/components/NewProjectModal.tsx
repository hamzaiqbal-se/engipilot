"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, Plus, Loader2, CheckCircle2 } from "lucide-react";
import { createProject, createSprint } from "@/lib/api";

const TECH_OPTIONS = ["AI/ML", "MERN Stack", "Laravel", "Flutter", "UI/UX", "DevOps", "Data Science"];

export default function NewProjectModal({ onCreated }: { onCreated: () => void }) {
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState("");
  const [form, setForm] = useState({
    name: "",
    technology: "AI/ML",
    deadline: "",
    github_repo: "",
  });

  const resetAndClose = () => {
    setOpen(false);
    setSuccess(false);
    setError("");
    setForm({ name: "", technology: "AI/ML", deadline: "", github_repo: "" });
  };

  const handleSubmit = async () => {
    if (!form.name.trim()) {
      setError("Project name is required.");
      return;
    }
    setError("");
    setLoading(true);
    try {
      const project = await createProject({
        name: form.name,
        technology: form.technology,
        deadline: form.deadline ? new Date(form.deadline).toISOString() : undefined,
        github_repo: form.github_repo || undefined,
      });
      await createSprint({
        project_id: project.id,
        sprint_number: 1,
        goal: "Initial sprint",
      });
      setSuccess(true);
      onCreated();
      setTimeout(resetAndClose, 1200);
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
        className="flex items-center gap-1.5 text-xs bg-blue-600 hover:bg-blue-500 text-white rounded-lg px-3 py-2 transition-colors"
      >
        <Plus size={14} /> New Project
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
                  <p className="text-white font-medium">Project created successfully!</p>
                </div>
              ) : (
                <>
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-white font-semibold">New Project</h3>
                    <button onClick={resetAndClose} className="text-slate-400"><X size={18} /></button>
                  </div>

                  <div className="space-y-3">
                    <div>
                      <label className="text-xs text-slate-500">Project Name *</label>
                      <input
                        value={form.name}
                        onChange={(e) => setForm({ ...form, name: e.target.value })}
                        className="w-full mt-1 bg-white/5 border border-[var(--border)] text-white text-sm rounded-lg px-3 py-2 outline-none focus:border-blue-500/50"
                        placeholder="e.g. Mobile App Redesign"
                      />
                    </div>

                    <div>
                      <label className="text-xs text-slate-500">Technology</label>
                      <select
                        value={form.technology}
                        onChange={(e) => setForm({ ...form, technology: e.target.value })}
                        className="w-full mt-1 bg-white/5 border border-[var(--border)] text-white text-sm rounded-lg px-3 py-2 outline-none focus:border-blue-500/50"
                      >
                        {TECH_OPTIONS.map((t) => (
                          <option key={t} value={t} style={{ background: "#131a29", color: "#f1f5f9" }}>
                            {t}
                          </option>
                        ))}
                      </select>
                    </div>

                    <div>
                      <label className="text-xs text-slate-500">Deadline (optional)</label>
                      <input
                        type="date"
                        value={form.deadline}
                        onChange={(e) => setForm({ ...form, deadline: e.target.value })}
                        className="w-full mt-1 bg-white/5 border border-[var(--border)] text-white text-sm rounded-lg px-3 py-2 outline-none focus:border-blue-500/50"
                      />
                    </div>

                    <div>
                      <label className="text-xs text-slate-500">GitHub Repo (optional — e.g. username/repo)</label>
                      <input
                        value={form.github_repo}
                        onChange={(e) => setForm({ ...form, github_repo: e.target.value })}
                        className="w-full mt-1 bg-white/5 border border-[var(--border)] text-white text-sm rounded-lg px-3 py-2 outline-none focus:border-blue-500/50"
                        placeholder="hamzaiqbal-se/my-repo"
                      />
                    </div>
                  </div>

                  {error && <p className="text-red-400 text-xs mt-3">{error}</p>}

                  <button
                    onClick={handleSubmit}
                    disabled={loading}
                    className="w-full mt-5 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white rounded-lg py-2.5 text-sm font-medium transition-colors flex items-center justify-center gap-2"
                  >
                    {loading ? <Loader2 size={15} className="animate-spin" /> : <Plus size={15} />}
                    Create Project
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