import React, { useState, useEffect } from "react";
import { Activity, Sparkles, CheckCircle, AlertTriangle, ShieldX, Play, RotateCcw } from "lucide-react";
import { api } from "../api";

const PRESET_EXAMPLES = [
  {
    title: "Civil Academic Feedback",
    text: "Thank you for reviewing the methodology section. The empirical findings align well with our initial hypothesis.",
  },
  {
    title: "Internet Slang Normalization",
    text: "WTF r u doing? stfu, this tutorial makes zero sense lmao.",
  },
  {
    title: "Veiled Hostility / Insult",
    text: "You are an absolute clown with zero intelligence. Stop posting before you embarrass yourself further.",
  },
  {
    title: "Direct Physical Threat",
    text: "I swear I will track your IP address and make you regret ever messing with me. You are dead meat.",
  },
  {
    title: "Identity Hate & Bigotry",
    text: "People of your ethnicity are inferior parasites who should be banished from the civilized world.",
  },
];

export default function LiveCheckPage() {
  const [inputText, setInputText] = useState(PRESET_EXAMPLES[0].text);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [autoAnalyze, setAutoAnalyze] = useState(true);

  const runPrediction = async (textToAnalyze) => {
    const text = textToAnalyze !== undefined ? textToAnalyze : inputText;
    if (!text.trim()) {
      setResult(null);
      return;
    }

    setLoading(true);
    try {
      const data = await api.predict(text);
      setResult(data);
    } catch (err) {
      console.error("Prediction failed:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (autoAnalyze) {
      const timer = setTimeout(() => {
        runPrediction(inputText);
      }, 350);
      return () => clearTimeout(timer);
    }
  }, [inputText, autoAnalyze]);

  const getBarColor = (score) => {
    if (score >= 0.65) return "bg-[#d25d53] shadow-[#d25d53]/40";
    if (score >= 0.35) return "bg-[#d9a043] shadow-[#d9a043]/40";
    return "bg-[#749655] shadow-[#749655]/40";
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-8">
      {/* Header */}
      <div className="p-6 rounded-2xl glass-panel relative overflow-hidden">
        <div className="absolute -top-12 -right-12 w-48 h-48 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="relative z-10">
          <div className="inline-flex items-center space-x-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 mb-2">
            <Activity className="w-3.5 h-3.5 text-emerald-400" />
            <span>Interactive Real-time ML Inference</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Live Toxicity Analyzer
          </h1>
          <p className="text-sm text-slate-400 mt-1 max-w-xl">
            Test any arbitrary text against our multi-label Deep Learning classification model.
            Examine how normalized internet slang, toxicity categories, and confidence thresholds interact.
          </p>
        </div>
      </div>

      {/* Preset Pills for Quick Evaluator Testing */}
      <div className="space-y-2">
        <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block">
          Preset Benchmark Prompts (Click to Load):
        </label>
        <div className="flex flex-wrap gap-2">
          {PRESET_EXAMPLES.map((ex, i) => (
            <button
              key={i}
              type="button"
              onClick={() => {
                setInputText(ex.text);
                runPrediction(ex.text);
              }}
              className="px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 hover:border-indigo-500/40 text-xs font-medium transition"
            >
              {ex.title}
            </button>
          ))}
        </div>
      </div>

      {/* Input Textarea & Controls */}
      <div className="p-5 sm:p-6 rounded-2xl glass-panel border border-slate-800 space-y-4">
        <div className="flex items-center justify-between">
          <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
            Input Comment Text
          </label>
          <div className="flex items-center space-x-3 text-xs">
            <label className="flex items-center space-x-1.5 cursor-pointer text-slate-400 hover:text-slate-200">
              <input
                type="checkbox"
                checked={autoAnalyze}
                onChange={(e) => setAutoAnalyze(e.target.checked)}
                className="rounded bg-slate-900 border-slate-700 text-indigo-600 focus:ring-0"
              />
              <span>Live Auto-Analyze</span>
            </label>
            <button
              onClick={() => runPrediction()}
              disabled={loading}
              className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-medium shadow-sm transition"
            >
              <Play className="w-3 h-3 fill-current" />
              <span>Analyze</span>
            </button>
          </div>
        </div>

        <textarea
          rows={4}
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Type or paste any text to inspect toxicity probabilities..."
          className="w-full p-3.5 text-sm bg-slate-950/90 border border-slate-800 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition resize-none"
        />

        {result?.cleaned_text && (
          <div className="p-3 rounded-lg bg-slate-950/60 border border-slate-800/80 text-xs text-slate-400">
            <span className="font-semibold text-indigo-400 mr-1.5">NLP Pipeline Cleaned & Lemmatized:</span>
            <span className="font-mono text-slate-300">"{result.cleaned_text}"</span>
          </div>
        )}
      </div>

      {/* Results Section */}
      {result && (
        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-2 duration-200">
          {/* Main Verdict Card */}
          <div
            className={`p-6 rounded-2xl border flex flex-col sm:flex-row sm:items-center justify-between gap-4 ${
              result.status === "approved"
                ? "bg-emerald-950/20 border-emerald-500/40"
                : result.status === "flagged"
                ? "bg-amber-950/20 border-amber-500/40"
                : "bg-rose-950/20 border-rose-500/40"
            }`}
          >
            <div className="flex items-center space-x-3.5">
              <div
                className={`w-12 h-12 rounded-xl flex items-center justify-center shrink-0 ${
                  result.status === "approved"
                    ? "bg-emerald-500/20 text-emerald-400"
                    : result.status === "flagged"
                    ? "bg-amber-500/20 text-amber-400"
                    : "bg-rose-500/20 text-rose-400"
                }`}
              >
                {result.status === "approved" && <CheckCircle className="w-6 h-6" />}
                {result.status === "flagged" && <AlertTriangle className="w-6 h-6" />}
                {result.status === "blocked" && <ShieldX className="w-6 h-6" />}
              </div>
              <div>
                <span className="text-[11px] font-bold uppercase tracking-wider opacity-70">
                  Moderation Verdict
                </span>
                <h3 className="text-xl font-bold text-white">{result.verdict}</h3>
                <p className="text-xs opacity-80 mt-0.5">
                  Peak toxicity score: <span className="font-mono font-bold">{(result.max_score * 100).toFixed(1)}%</span>
                </p>
              </div>
            </div>

            <div className="flex items-center space-x-2">
              <span
                className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${
                  result.status === "approved"
                    ? "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30"
                    : result.status === "flagged"
                    ? "bg-amber-500/20 text-amber-300 border border-amber-500/30"
                    : "bg-rose-500/20 text-rose-300 border border-rose-500/30"
                }`}
              >
                Status: {result.status}
              </span>
            </div>
          </div>

          {/* 6 Category Probability Progress Bars */}
          <div className="p-6 rounded-2xl glass-panel border border-slate-800 space-y-5">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center space-x-2">
              <Sparkles className="w-4 h-4 text-indigo-400" />
              <span>Multi-Label Prediction Probabilities (Sigmoid Output)</span>
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {Object.entries(result.scores).map(([category, score]) => {
                const percentage = (score * 100).toFixed(1);
                const isFlagged = score >= 0.35;

                return (
                  <div
                    key={category}
                    className="p-3.5 rounded-xl bg-slate-950/70 border border-slate-800/80 space-y-2"
                  >
                    <div className="flex items-center justify-between text-xs">
                      <span className="font-semibold text-slate-200 capitalize">
                        {category.replace("_", " ")}
                      </span>
                      <span
                        className={`font-mono font-bold ${
                          score >= 0.65
                            ? "text-rose-400"
                            : score >= 0.35
                            ? "text-amber-400"
                            : "text-emerald-400"
                        }`}
                      >
                        {percentage}%
                      </span>
                    </div>

                    {/* Progress Bar Container */}
                    <div className="h-2.5 w-full bg-slate-800/80 rounded-full overflow-hidden p-0.5">
                      <div
                        className={`h-full rounded-full transition-all duration-300 ${getBarColor(score)}`}
                        style={{ width: `${Math.max(score * 100, 3)}%` }}
                      />
                    </div>

                    <div className="flex items-center justify-between text-[10px] text-slate-500">
                      <span>Threshold: 35%</span>
                      <span>{isFlagged ? "⚠️ Elevated Risk" : "✓ Low Risk"}</span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
