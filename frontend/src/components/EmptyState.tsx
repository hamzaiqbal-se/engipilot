"use client";

import { FolderPlus } from "lucide-react";

export default function EmptyState({ message, action }: { message: string; action?: React.ReactNode }) {
  return (
    <div className="glass-card p-12 flex flex-col items-center justify-center text-center">
      <FolderPlus size={32} className="text-slate-600 mb-3" />
      <p className="text-slate-400 text-sm mb-4">{message}</p>
      {action}
    </div>
  );
}