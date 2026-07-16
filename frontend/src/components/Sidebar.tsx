"use client";

import { useState } from "react";
import { LayoutDashboard, AlertTriangle, TrendingUp, Users, Crown, Menu, X } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

const navItems = [
  { icon: LayoutDashboard, label: "Overview" },
  { icon: TrendingUp, label: "Sprint Report" },
  { icon: AlertTriangle, label: "Risk Report" },
  { icon: Users, label: "Team Performance" },
  { icon: Crown, label: "Executive" },
];

export default function Sidebar({ active, onSelect }: { active: string; onSelect: (v: string) => void }) {
  const [mobileOpen, setMobileOpen] = useState(false);

  const NavContent = (
    <>
      <div className="mb-8 px-2">
        <h1 className="text-xl font-bold text-white">EngiPilot</h1>
        <p className="text-xs text-slate-500">AI Engineering Co-Pilot</p>
      </div>
      <nav className="flex flex-col gap-1">
        {navItems.map((item) => (
          <button
            key={item.label}
            onClick={() => {
              onSelect(item.label);
              setMobileOpen(false);
            }}
            className={`relative flex items-center gap-3 px-3 py-3 md:py-2.5 rounded-lg text-sm transition-colors ${
              active === item.label ? "text-white" : "text-slate-400 hover:text-slate-200"
            }`}
          >
            {active === item.label && (
              <motion.div
                layoutId="active-nav"
                className="absolute inset-0 bg-blue-600/20 border border-blue-500/40 rounded-lg"
                transition={{ type: "spring", duration: 0.4 }}
              />
            )}
            <item.icon size={18} className="relative z-10 shrink-0" />
            <span className="relative z-10">{item.label}</span>
          </button>
        ))}
      </nav>
    </>
  );

  return (
    <>
      {/* Mobile top bar */}
      <div className="md:hidden flex items-center justify-between p-4 border-b border-[var(--border)] bg-[var(--surface-solid)]">
        <h1 className="text-lg font-bold text-white">EngiPilot</h1>
        <button onClick={() => setMobileOpen(true)} className="text-slate-300 p-1">
          <Menu size={22} />
        </button>
      </div>

      {/* Mobile slide-in menu */}
      <AnimatePresence>
        {mobileOpen && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setMobileOpen(false)}
              className="fixed inset-0 bg-black/60 z-40 md:hidden"
            />
            <motion.div
              initial={{ x: -280 }}
              animate={{ x: 0 }}
              exit={{ x: -280 }}
              transition={{ type: "spring", damping: 25 }}
              className="fixed top-0 left-0 h-screen w-64 bg-[var(--surface-solid)] border-r border-[var(--border)] p-4 z-50 md:hidden"
            >
              <button onClick={() => setMobileOpen(false)} className="absolute top-4 right-4 text-slate-400">
                <X size={20} />
              </button>
              {NavContent}
            </motion.div>
          </>
        )}
      </AnimatePresence>

      {/* Desktop sidebar */}
      <div className="hidden md:flex w-64 h-screen border-r border-[var(--border)] bg-[var(--surface-solid)] flex-col p-4 shrink-0">
        {NavContent}
      </div>
    </>
  );
}