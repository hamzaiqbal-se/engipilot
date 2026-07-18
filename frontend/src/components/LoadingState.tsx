"use client";

import { motion } from "framer-motion";

export default function LoadingState() {
  return (
    <div className="space-y-4 md:space-y-6">
      {[1, 2].map((i) => (
        <motion.div
          key={i}
          initial={{ opacity: 0.3 }}
          animate={{ opacity: [0.3, 0.6, 0.3] }}
          transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
          className="glass-card p-6 h-32"
        />
      ))}
    </div>
  );
}