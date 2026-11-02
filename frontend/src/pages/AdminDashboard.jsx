import React, { useState, useEffect } from "react";
import {
  ShieldAlert,
  Check,
  Trash2,
  Lock,
  TrendingUp,
  PieChart as PieIcon,
  Users,
  AlertTriangle,
  FileText,
  BarChart2,
  RefreshCw,
  Clock,
  Sparkles,
} from "lucide-react";
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid,
} from "recharts";
import { api } from "../api";

const PIE_COLORS = ["#749655", "#d1c3a8", "#d9a043", "#d25d53", "#8ea977", "#b4a285"];

export default function AdminDashboard({ user, onRequireAuth }) {
  const [analytics, setAnalytics] = useState(null);
  const [flaggedQueue, setFlaggedQueue] = useState([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState({});

  const isAdmin = user && user.role === "admin";

  const loadData = async () => {
    if (!isAdmin) return;
    setLoading(true);
    try {
      const [analyticsData, queueData] = await Promise.all([
        api.getAdminAnalytics(),
        api.getFlaggedQueue(),
      ]);
      setAnalytics(analyticsData);
      setFlaggedQueue(queueData);
    } catch (err) {
      console.error("Failed to load admin data:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [isAdmin]);

  const handleModerate = async (id, action) => {
    setActionLoading((prev) => ({ ...prev, [id]: true }));
    try {
      await api.moderateComment(id, action);
      // Remove from queue
      setFlaggedQueue((prev) => prev.filter((item) => item.id !== id));
      // Refresh analytics
      const updatedAnalytics = await api.getAdminAnalytics();
      setAnalytics(updatedAnalytics);
    } catch (err) {
      alert("Failed to moderate comment: " + err.message);
    } finally {
      setActionLoading((prev) => ({ ...prev, [id]: false }));
    }
  };

  if (!isAdmin) {
    return (
      <div className="max-w-md mx-auto my-16 p-8 rounded-2xl glass-panel border border-slate-800 text-center space-y-4">
        <div className="w-14 h-14 mx-auto rounded-2xl bg-rose-500/10 border border-rose-500/20 flex items-center justify-center text-rose-400">
          <Lock className="w-7 h-7" />
        </div>
        <h2 className="text-xl font-bold text-white">Administrator Access Required</h2>
        <p className="text-xs text-slate-400">
          The moderation queue and platform analytics dashboard are reserved for administrator roles.
        </p>
        <button
          onClick={onRequireAuth}
          className="w-full py-2.5 px-4 bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-xs rounded-xl shadow-lg shadow-indigo-600/30 transition"
        >
          Sign In as Admin (1-Click Demo)
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 space-y-8">
      {/* Dashboard Top Header */}
      <div className="p-6 rounded-2xl glass-panel relative overflow-hidden flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="absolute -top-12 -right-12 w-48 h-48 bg-rose-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="relative z-10">
          <div className="inline-flex items-center space-x-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-rose-500/20 text-rose-300 border border-rose-500/30 mb-2">
            <ShieldAlert className="w-3.5 h-3.5 text-rose-400" />
            <span>Admin Moderation Control Center</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Moderation Operations & Analytics
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Real-time telemetry, model confidence distributions, and human-in-the-loop review queue.
          </p>
        </div>
        <button
          onClick={loadData}
          className="self-start sm:self-center flex items-center space-x-1.5 px-3.5 py-2 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-700 text-xs font-medium transition"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh Analytics</span>
        </button>
      </div>

      {/* KPI Cards */}
      {analytics && (
        <div className="grid grid-cols-2 lg:grid-cols-5 gap-4">
          <div className="p-4 rounded-xl glass-panel border border-slate-800">
            <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
              Total Comments
            </span>
            <div className="text-2xl font-extrabold text-white mt-1">
              {analytics.total_comments}
            </div>
            <span className="text-[10px] text-indigo-400 mt-1 block">Platform Lifetime</span>
          </div>

          <div className="p-4 rounded-xl glass-panel border border-slate-800">
            <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
              Approved Clean
            </span>
            <div className="text-2xl font-extrabold text-emerald-400 mt-1">
              {analytics.approved_comments}
            </div>
            <span className="text-[10px] text-emerald-500 mt-1 block">
              {((analytics.approved_comments / analytics.total_comments) * 100).toFixed(1)}% of total
            </span>
          </div>

          <div className="p-4 rounded-xl glass-panel border border-slate-800">
            <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
              Flagged in Queue
            </span>
            <div className="text-2xl font-extrabold text-amber-400 mt-1">
              {analytics.flagged_comments}
            </div>
            <span className="text-[10px] text-amber-500 mt-1 block">Needs Manual Review</span>
          </div>

          <div className="p-4 rounded-xl glass-panel border border-slate-800">
            <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
              Auto-Blocked
            </span>
            <div className="text-2xl font-extrabold text-rose-400 mt-1">
              {analytics.blocked_comments}
            </div>
            <span className="text-[10px] text-rose-500 mt-1 block">Severe Violations</span>
          </div>

          <div className="p-4 rounded-xl glass-panel border border-slate-800 col-span-2 lg:col-span-1">
            <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
              Toxicity Rate
            </span>
            <div className="text-2xl font-extrabold text-indigo-400 mt-1">
              {analytics.toxic_rate_percentage}%
            </div>
            <span className="text-[10px] text-slate-400 mt-1 block">Flagged + Blocked</span>
          </div>
        </div>
      )}

      {/* Flagged Comments Moderation Queue */}
      <div className="p-6 rounded-2xl glass-panel border border-slate-800 space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <AlertTriangle className="w-5 h-5 text-amber-400" />
            <h2 className="text-base font-bold text-white">
              Flagged Comments Review Queue ({flaggedQueue.length})
            </h2>
          </div>
          <span className="text-xs text-slate-400">Human-In-The-Loop AI Oversight</span>
        </div>

        {flaggedQueue.length === 0 ? (
          <div className="p-8 text-center border border-dashed border-slate-800 rounded-xl text-slate-500 text-sm">
            🎉 Review queue is empty! No comments currently pending administrator action.
          </div>
        ) : (
          <div className="space-y-3 max-h-96 overflow-y-auto pr-1">
            {flaggedQueue.map((item) => (
              <div
                key={item.id}
                className="p-4 rounded-xl bg-slate-950/70 border border-slate-800/90 flex flex-col md:flex-row md:items-center justify-between gap-4"
              >
                <div className="space-y-1.5 flex-1">
                  <div className="flex items-center space-x-2 text-xs">
                    <span className="font-semibold text-slate-200">
                      @{item.author?.username || "Unknown"}
                    </span>
                    <span className="text-slate-500">•</span>
                    <span className="text-[11px] text-slate-400 flex items-center space-x-1">
                      <Clock className="w-3 h-3" />
                      <span>{new Date(item.created_at).toLocaleString()}</span>
                    </span>
                    <span className="px-2 py-0.5 rounded bg-amber-500/15 text-amber-300 font-mono text-[10px] font-bold">
                      Confidence: {(item.max_score * 100).toFixed(1)}%
                    </span>
                  </div>
                  <p className="text-sm text-slate-300 italic">"{item.text}"</p>
                  <div className="flex flex-wrap gap-1.5 text-[10px] text-slate-400">
                    <span className="font-semibold text-slate-500">Probabilities:</span>
                    <span>Toxic: {(item.toxic * 100).toFixed(0)}%</span>
                    <span>Severe: {(item.severe_toxic * 100).toFixed(0)}%</span>
                    <span>Obscene: {(item.obscene * 100).toFixed(0)}%</span>
                    <span>Threat: {(item.threat * 100).toFixed(0)}%</span>
                    <span>Insult: {(item.insult * 100).toFixed(0)}%</span>
                    <span>Hate: {(item.identity_hate * 100).toFixed(0)}%</span>
                  </div>
                </div>

                {/* Moderation Actions */}
                <div className="flex items-center space-x-2 shrink-0">
                  <button
                    onClick={() => handleModerate(item.id, "approve")}
                    disabled={actionLoading[item.id]}
                    className="flex items-center space-x-1 px-3 py-1.5 rounded-lg bg-emerald-600/20 hover:bg-emerald-600/30 text-emerald-300 border border-emerald-500/30 text-xs font-semibold transition"
                  >
                    <Check className="w-3.5 h-3.5" />
                    <span>Approve</span>
                  </button>
                  <button
                    onClick={() => handleModerate(item.id, "delete")}
                    disabled={actionLoading[item.id]}
                    className="flex items-center space-x-1 px-3 py-1.5 rounded-lg bg-rose-600/20 hover:bg-rose-600/30 text-rose-300 border border-rose-500/30 text-xs font-semibold transition"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                    <span>Delete</span>
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Analytics Charts Grid */}
      {analytics && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Chart 1: Daily Trends */}
          <div className="p-6 rounded-2xl glass-panel border border-slate-800 space-y-4">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center space-x-2">
              <TrendingUp className="w-4 h-4 text-indigo-400" />
              <span>14-Day Comment Volume & Toxicity Trends</span>
            </h3>
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={analytics.daily_trends}>
                  <defs>
                    <linearGradient id="colorClean" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#749655" stopOpacity={0.4} />
                      <stop offset="95%" stopColor="#749655" stopOpacity={0.0} />
                    </linearGradient>
                    <linearGradient id="colorFlagged" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#d9a043" stopOpacity={0.4} />
                      <stop offset="95%" stopColor="#d9a043" stopOpacity={0.0} />
                    </linearGradient>
                    <linearGradient id="colorBlocked" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#d25d53" stopOpacity={0.4} />
                      <stop offset="95%" stopColor="#d25d53" stopOpacity={0.0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#DCD0BD" />
                  <XAxis dataKey="date" stroke="#6B7460" fontSize={10} tickFormatter={(d) => d.slice(5)} />
                  <YAxis stroke="#6B7460" fontSize={10} />
                  <Tooltip contentStyle={{ backgroundColor: "#FAF7F2", borderColor: "#DCD0BD", borderRadius: "10px", color: "#171E13", fontSize: 12, boxShadow: "0 4px 20px rgba(90, 75, 50, 0.12)" }} />
                  <Legend wrapperStyle={{ fontSize: 11 }} />
                  <Area type="monotone" dataKey="clean" stroke="#749655" fillOpacity={1} fill="url(#colorClean)" name="Clean" />
                  <Area type="monotone" dataKey="flagged" stroke="#d9a043" fillOpacity={1} fill="url(#colorFlagged)" name="Flagged" />
                  <Area type="monotone" dataKey="blocked" stroke="#d25d53" fillOpacity={1} fill="url(#colorBlocked)" name="Blocked" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Chart 2: Category Distribution */}
          <div className="p-6 rounded-2xl glass-panel border border-slate-800 space-y-4">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center space-x-2">
              <PieIcon className="w-4 h-4 text-rose-600" />
              <span>Multi-Label Category Distribution</span>
            </h3>
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={analytics.category_distribution}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#DCD0BD" />
                  <XAxis dataKey="category" stroke="#6B7460" fontSize={10} />
                  <YAxis stroke="#6B7460" fontSize={10} />
                  <Tooltip contentStyle={{ backgroundColor: "#FAF7F2", borderColor: "#DCD0BD", borderRadius: "10px", color: "#171E13", fontSize: 12, boxShadow: "0 4px 20px rgba(90, 75, 50, 0.12)" }} />
                  <Bar dataKey="count" fill="#749655" radius={[4, 4, 0, 0]} name="Violations Count">
                    {analytics.category_distribution.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={PIE_COLORS[index % PIE_COLORS.length]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Chart 3: Model Confidence Histogram */}
          <div className="p-6 rounded-2xl glass-panel border border-slate-800 space-y-4">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center space-x-2">
              <BarChart2 className="w-4 h-4 text-amber-600" />
              <span>Model Prediction Confidence Distribution</span>
            </h3>
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={analytics.confidence_histogram}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#DCD0BD" />
                  <XAxis dataKey="bin" stroke="#6B7460" fontSize={10} />
                  <YAxis stroke="#6B7460" fontSize={10} />
                  <Tooltip contentStyle={{ backgroundColor: "#FAF7F2", borderColor: "#DCD0BD", borderRadius: "10px", color: "#171E13", fontSize: 12, boxShadow: "0 4px 20px rgba(90, 75, 50, 0.12)" }} />
                  <Bar dataKey="count" fill="#749655" radius={[4, 4, 0, 0]} name="Comments" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Chart 4: Top Flagged Users & Top Toxic Words */}
          <div className="p-6 rounded-2xl glass-panel border border-slate-800 space-y-4">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center space-x-2">
              <Users className="w-4 h-4 text-emerald-400" />
              <span>Top Flagged Accounts & High-Risk Lexicon</span>
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 h-64 overflow-y-auto">
              {/* Users */}
              <div className="space-y-2">
                <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
                  Most Flagged Accounts:
                </span>
                <div className="space-y-1.5">
                  {analytics.top_flagged_users.map((u, i) => (
                    <div
                      key={i}
                      className="flex items-center justify-between p-2 rounded-lg bg-slate-950/80 border border-slate-800/80 text-xs"
                    >
                      <span className="font-semibold text-slate-200">@{u.username}</span>
                      <span className="px-1.5 py-0.5 rounded bg-rose-500/20 text-rose-300 font-mono font-bold text-[10px]">
                        {u.violations_count} strikes
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Toxic Words Cloud */}
              <div className="space-y-2">
                <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
                  Frequent Abusive Tokens:
                </span>
                <div className="flex flex-wrap gap-1.5">
                  {analytics.top_toxic_words.map((w, i) => (
                    <span
                      key={i}
                      className="px-2 py-1 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 text-xs flex items-center space-x-1"
                    >
                      <span className="font-medium text-rose-300">{w.text}</span>
                      <span className="text-[10px] text-slate-500 font-mono">({w.value})</span>
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
