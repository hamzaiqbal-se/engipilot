"use client";

import { useEffect, useState } from "react";
import { Command } from "cmdk";
import { LayoutDashboard, TrendingUp, AlertTriangle, Users, Crown, Search } from "lucide-react";

const commands = [
  { icon: LayoutDashboard, label: "Go to Overview", value: "Overview" },
  { icon: TrendingUp, label: "Go to Sprint Report", value: "Sprint Report" },
  { icon: AlertTriangle, label: "Go to Risk Report", value: "Risk Report" },
  { icon: Users, label: "Go to Team Performance", value: "Team Performance" },
  { icon: Crown, label: "Go to Executive", value: "Executive" },
];

export default function CommandPalette({ onSelect }: { onSelect: (view: string) => void }) {
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setOpen((o) => !o);
      }
      if (e.key === "Escape") setOpen(false);
    };
    document.addEventListener("keydown", down);
    return () => document.removeEventListener("keydown", down);
  }, []);

  if (!open) return null;

  return (
    <div
      className="fixed inset-0 bg-black/70 z-[100] flex items-start justify-center pt-24 px-4"
      onClick={() => setOpen(false)}
    >
      <Command
        className="w-full max-w-lg bg-[var(--surface-solid)] border border-[var(--border)] rounded-xl shadow-2xl overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center gap-2 px-4 py-3 border-b border-[var(--border)]">
          <Search size={16} className="text-slate-500" />
          <Command.Input
            placeholder="Type a command or search..."
            className="flex-1 bg-transparent text-white text-sm outline-none placeholder:text-slate-500"
          />
          <kbd className="text-[10px] text-slate-500 bg-white/5 px-1.5 py-0.5 rounded border border-[var(--border)]">
            ESC
          </kbd>
        </div>

        <Command.List className="max-h-80 overflow-y-auto p-2">
          <Command.Empty className="text-slate-500 text-sm text-center py-6">
            No results found.
          </Command.Empty>

          {commands.map((cmd) => (
            <Command.Item
              key={cmd.value}
              onSelect={() => {
                onSelect(cmd.value);
                setOpen(false);
              }}
              className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-slate-300 cursor-pointer aria-selected:bg-blue-600/20 aria-selected:text-white transition-colors"
            >
              <cmd.icon size={16} />
              {cmd.label}
            </Command.Item>
          ))}
        </Command.List>
      </Command>
    </div>
  );
}