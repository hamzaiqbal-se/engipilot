"use client";

import { useEffect, useState } from "react";
import { getProjects } from "@/lib/api";

export default function Home() {
  const [status, setStatus] = useState("Connecting to backend...");

  useEffect(() => {
    getProjects()
      .then(() => setStatus("✅ Backend connected successfully!"))
      .catch(() => setStatus("❌ Backend connection failed"));
  }, []);

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="glass-card p-8">
        <h1 className="text-3xl font-bold text-white">EngiPilot</h1>
        <p className="text-slate-400 mt-2">{status}</p>
      </div>
    </div>
  );
}