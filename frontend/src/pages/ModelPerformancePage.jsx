import React, { useState, useEffect } from "react";
import { Cpu, Trophy, BarChart2, Layers, CheckCircle2, ArrowUpRight, Zap, Target } from "lucide-react";
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Legend, CartesianGrid } from "recharts";
import { api } from "../api";

export default function ModelPerformancePage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const metrics = await api.getModelComparison();
        setData(metrics);
      } catch (err) {
        console.error("Failed to load model comparison metrics", err);
      } finally {
        setLoading(false);
      }
    };
    fetchMetrics();
  }, []);

  const benchmarkResults = data?.benchmark_results || [];

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-8">
      {/* Header */}
      <div className="p-6 rounded-2xl glass-panel relative overflow-hidden">
        <div className="absolute -top-12 -right-12 w-48 h-48 bg-amber-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="relative z-10">
          <div className="inline-flex items-center space-x-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-500/20 text-amber-300 border border-amber-500/30 mb-2">
            <Cpu className="w-3.5 h-3.5 text-amber-400" />
            <span>Phase 2 Deep Learning Benchmark Report</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Multi-Model Evaluation & Comparative Analysis
          </h1>
          <p className="text-sm text-slate-400 mt-1 max-w-2xl">
            Empirical comparison of 6 multi-label architectures evaluated on identical test splits
            using Macro F1-Score, ROC-AUC, Exact Match Accuracy, and Hamming Loss.
          </p>
        </div>
      </div>

      {/* Production Winner Card */}
      <div className="p-6 rounded-2xl bg-gradient-to-r from-indigo-950/50 via-slate-900 to-beige-950/40 border border-indigo-500/35 flex flex-col md:flex-row md:items-center justify-between gap-6 shadow-lg shadow-indigo-950/20">
        <div className="flex items-start space-x-4">
          <div className="w-12 h-12 rounded-xl bg-indigo-500/20 border border-indigo-500/40 flex items-center justify-center text-indigo-400 shrink-0">
            <Trophy className="w-6 h-6" />
          </div>
          <div>
            <div className="inline-block px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 text-[10px] font-bold uppercase tracking-wider mb-1">
              Production Architecture
            </div>
            <h2 className="text-xl font-bold text-white">Hybrid CNN + BiLSTM with Sigmoid Multi-Head</h2>
            <p className="text-xs text-slate-300 mt-1 max-w-xl">
              Selected as the final production engine. Combines 1D convolutional feature map extraction
              (local phrase patterns & insults) with bidirectional LSTM recurrent layers (long-range semantic intent).
            </p>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-3 text-center shrink-0">
          <div className="p-3 rounded-xl bg-white/80 border border-slate-800 shadow-sm">
            <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block">
              ROC-AUC (Macro)
            </span>
            <span className="text-xl font-extrabold text-emerald-600 font-mono">0.988+</span>
          </div>
          <div className="p-3 rounded-xl bg-white/80 border border-slate-800 shadow-sm">
            <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider block">
              Inference Latency
            </span>
            <span className="text-xl font-extrabold text-indigo-600 font-mono">&lt; 15 ms</span>
          </div>
        </div>
      </div>

      {/* Comparison Table */}
      <div className="p-6 rounded-2xl glass-panel border border-slate-800 space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center space-x-2">
            <BarChart2 className="w-4 h-4 text-indigo-600" />
            <span>Benchmark Metrics Comparison Matrix</span>
          </h3>
          <span className="text-xs text-slate-500">Multi-label classification (6 targets)</span>
        </div>

        {loading ? (
          <div className="text-center py-12 text-slate-500 text-sm">Loading benchmark data...</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-600">
              <thead className="bg-slate-900/60 text-[11px] uppercase tracking-wider text-slate-500 border-b border-slate-800">
                <tr>
                  <th className="py-3 px-4">Architecture</th>
                  <th className="py-3 px-3">F1 (Macro)</th>
                  <th className="py-3 px-3">ROC-AUC</th>
                  <th className="py-3 px-3">Precision</th>
                  <th className="py-3 px-3">Recall</th>
                  <th className="py-3 px-3">Subset Acc</th>
                  <th className="py-3 px-3">Hamming Acc</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/80 font-mono">
                {benchmarkResults.map((m, idx) => (
                  <tr
                    key={idx}
                    className={`hover:bg-slate-900/40 transition ${
                      m.model_name.includes("Hybrid") ? "bg-indigo-900/30 font-semibold" : ""
                    }`}
                  >
                    <td className="py-3.5 px-4 font-sans font-medium text-slate-800 flex items-center space-x-2">
                      <span>{m.model_name}</span>
                      {m.model_name.includes("Hybrid") && (
                        <span className="px-1.5 py-0.2 bg-indigo-600/15 text-indigo-700 text-[9px] rounded font-bold uppercase border border-indigo-600/30">
                          BEST
                        </span>
                      )}
                    </td>
                    <td className="py-3.5 px-3 text-indigo-700 font-bold">
                      {(m.f1_macro * 100).toFixed(1)}%
                    </td>
                    <td className="py-3.5 px-3 text-emerald-700 font-bold">
                      {(m.roc_auc_macro * 100).toFixed(1)}%
                    </td>
                    <td className="py-3.5 px-3 text-slate-700">
                      {(m.precision_macro * 100).toFixed(1)}%
                    </td>
                    <td className="py-3.5 px-3 text-slate-700">
                      {(m.recall_macro * 100).toFixed(1)}%
                    </td>
                    <td className="py-3.5 px-3 text-slate-600">
                      {(m.subset_accuracy * 100).toFixed(1)}%
                    </td>
                    <td className="py-3.5 px-3 text-emerald-700">
                      {(m.hamming_accuracy * 100).toFixed(1)}%
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Visual Bar Comparison Chart */}
      {benchmarkResults.length > 0 && (
        <div className="p-6 rounded-2xl glass-panel border border-slate-800 space-y-4">
          <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center space-x-2">
            <Zap className="w-4 h-4 text-amber-600" />
            <span>Interactive Multi-Metric Benchmark Chart</span>
          </h3>

          <div className="h-80 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={benchmarkResults.map((r) => ({
                  name: r.model_name.replace(" (Baseline)", "").replace(" Text Classifier", "").replace(" Classifier", "").replace(" (Production)", ""),
                  "F1 Macro": Number((r.f1_macro * 100).toFixed(1)),
                  "ROC-AUC": Number((r.roc_auc_macro * 100).toFixed(1)),
                  "Precision": Number((r.precision_macro * 100).toFixed(1)),
                  "Recall": Number((r.recall_macro * 100).toFixed(1)),
                }))}
                margin={{ top: 10, right: 10, left: -20, bottom: 25 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="#DCD0BD" />
                <XAxis dataKey="name" stroke="#6B7460" fontSize={10} angle={-15} textAnchor="end" interval={0} />
                <YAxis stroke="#6B7460" fontSize={10} domain={[0, 100]} />
                <Tooltip contentStyle={{ backgroundColor: "#FAF7F2", borderColor: "#DCD0BD", borderRadius: "10px", color: "#171E13", fontSize: 12, boxShadow: "0 4px 20px rgba(90, 75, 50, 0.12)" }} />
                <Legend wrapperStyle={{ fontSize: 11 }} />
                <Bar dataKey="F1 Macro" fill="#749655" radius={[3, 3, 0, 0]} />
                <Bar dataKey="ROC-AUC" fill="#8fb36c" radius={[3, 3, 0, 0]} />
                <Bar dataKey="Precision" fill="#d4c3a8" radius={[3, 3, 0, 0]} />
                <Bar dataKey="Recall" fill="#b4a285" radius={[3, 3, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* Architecture Deep-Dive Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        <div className="p-5 rounded-2xl glass-panel border border-slate-800 space-y-2">
          <div className="flex items-center space-x-2 text-indigo-400">
            <Layers className="w-4 h-4" />
            <h4 className="text-sm font-bold text-white">1. Classical Baselines</h4>
          </div>
          <p className="text-xs text-slate-400 leading-relaxed">
            TF-IDF with sublinear term-frequency scaling and n-gram extraction (1, 2) coupled with
            One-Vs-Rest Logistic Regression and Calibrated LinearSVC. Provides strong baseline performance.
          </p>
        </div>

        <div className="p-5 rounded-2xl glass-panel border border-slate-800 space-y-2">
          <div className="flex items-center space-x-2 text-amber-400">
            <Target className="w-4 h-4" />
            <h4 className="text-sm font-bold text-white">2. Sequential Recurrence</h4>
          </div>
          <p className="text-xs text-slate-400 leading-relaxed">
            LSTM & BiLSTM architectures preserve word order via gating mechanisms (Input, Forget, Output gates).
            Bidirectional passes process tokens chronologically and in reverse to capture preceding and succeeding contexts.
          </p>
        </div>

        <div className="p-5 rounded-2xl glass-panel border border-slate-800 space-y-2">
          <div className="flex items-center space-x-2 text-emerald-400">
            <CheckCircle2 className="w-4 h-4" />
            <h4 className="text-sm font-bold text-white">3. Hybrid CNN + BiLSTM</h4>
          </div>
          <p className="text-xs text-slate-400 leading-relaxed">
            Conv1D filters identify local toxic keyphrases and abusive slur n-grams. The sequential feature
            maps are then fed to BiLSTM layers, creating state-of-the-art multi-label toxicity representations.
          </p>
        </div>
      </div>
    </div>
  );
}
