"use client";

import { useState, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Sparkles, Send, Loader2, Mic, MicOff } from "lucide-react";
import { askDocumentation } from "@/lib/api";

export default function AskEngiPilot() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState<{ answer: string; sources: string[] } | null>(null);
  const [loading, setLoading] = useState(false);
  const [listening, setListening] = useState(false);
  const [voiceSupported] = useState(
    typeof window !== "undefined" &&
      ("SpeechRecognition" in window || "webkitSpeechRecognition" in window)
  );
  const recognitionRef = useRef<any>(null);

  const handleAsk = async (textOverride?: string) => {
    const finalQuery = textOverride ?? query;
    if (!finalQuery.trim()) return;
    setLoading(true);
    setAnswer(null);
    try {
      const res = await askDocumentation(finalQuery);
      setAnswer(res);
    } catch {
      setAnswer({ answer: "Something went wrong. Please try again.", sources: [] });
    } finally {
      setLoading(false);
    }
  };

  const handleVoiceInput = () => {
    if (!voiceSupported) return;

    const SpeechRecognition =
      (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognitionRef.current = recognition;

    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => setListening(true);
    recognition.onend = () => setListening(false);
    recognition.onerror = () => setListening(false);

    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      setQuery(transcript);
      handleAsk(transcript);
    };

    recognition.start();
  };

  const stopListening = () => {
    recognitionRef.current?.stop();
    setListening(false);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="glass-card p-6"
    >
      <div className="flex items-center gap-2 mb-4">
        <Sparkles size={18} className="text-purple-400" />
        <h3 className="text-white font-semibold">Ask EngiPilot</h3>
      </div>

      <div className="flex gap-2">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleAsk()}
          placeholder={listening ? "Listening..." : "Ask anything about this project..."}
          className="flex-1 bg-white/5 border border-[var(--border)] text-white text-sm rounded-lg px-4 py-2.5 outline-none focus:border-blue-500/50 transition-colors"
        />

        {voiceSupported && (
          <button
            onClick={listening ? stopListening : handleVoiceInput}
            className={`rounded-lg px-4 py-2.5 transition-colors shrink-0 ${
              listening
                ? "bg-red-500/20 text-red-400 animate-pulse"
                : "bg-white/5 hover:bg-white/10 text-slate-300 border border-[var(--border)]"
            }`}
            title={listening ? "Stop listening" : "Ask by voice"}
          >
            {listening ? <MicOff size={16} /> : <Mic size={16} />}
          </button>
        )}

        <button
          onClick={() => handleAsk()}
          disabled={loading}
          className="bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white rounded-lg px-4 py-2.5 transition-colors shrink-0"
        >
          {loading ? <Loader2 size={16} className="animate-spin" /> : <Send size={16} />}
        </button>
      </div>

      {!voiceSupported && (
        <p className="text-xs text-slate-600 mt-2">Voice input is not supported in this browser — try Chrome or Edge.</p>
      )}

      <AnimatePresence>
        {answer && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="mt-4 pt-4 border-t border-[var(--border)] overflow-hidden"
          >
            <p className="text-slate-300 text-sm leading-relaxed">{answer.answer}</p>
            {answer.sources && answer.sources.length > 0 && (
              <div className="flex flex-wrap gap-1.5 mt-3">
                {answer.sources.map((s) => (
                  <span key={s} className="text-xs bg-purple-500/10 text-purple-400 px-2 py-0.5 rounded-full">
                    {s}
                  </span>
                ))}
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}