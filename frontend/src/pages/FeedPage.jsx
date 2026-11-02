import React, { useState, useEffect } from "react";
import { MessageSquare, Send, AlertTriangle, ShieldX, CheckCircle, Clock, Filter, Sparkles, RefreshCw } from "lucide-react";
import { api } from "../api";

export default function FeedPage({ user, onRequireAuth }) {
  const [comments, setComments] = useState([]);
  const [newText, setNewText] = useState("");
  const [statusFilter, setStatusFilter] = useState("approved");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [postFeedback, setPostFeedback] = useState(null);

  const fetchFeed = async () => {
    setLoading(true);
    try {
      const data = await api.getComments(statusFilter, 40);
      setComments(data);
    } catch (err) {
      console.error("Failed to load feed", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFeed();
  }, [statusFilter]);

  const handlePost = async (e) => {
    e.preventDefault();
    if (!newText.trim()) return;

    if (!user) {
      onRequireAuth();
      return;
    }

    setSubmitting(true);
    setPostFeedback(null);

    try {
      const created = await api.createComment(newText.trim());
      setNewText("");

      if (created.status === "approved") {
        setPostFeedback({
          type: "success",
          message: "Comment approved and published to the feed!",
        });
        setComments((prev) => [created, ...prev]);
      } else if (created.status === "flagged") {
        setPostFeedback({
          type: "warning",
          message: "Comment contains potential sensitivity and has been queued for human moderation review.",
        });
      } else {
        setPostFeedback({
          type: "blocked",
          message: `Comment blocked: High toxicity score (${(created.max_score * 100).toFixed(1)}%). It violated platform safety policies.`,
        });
      }
    } catch (err) {
      setPostFeedback({
        type: "blocked",
        message: err.message || "Failed to submit comment.",
      });
    } finally {
      setSubmitting(false);
    }
  };

  const getScoreBadge = (score) => {
    const pct = (score * 100).toFixed(0);
    if (score >= 0.60) {
      return <span className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-rose-100 text-rose-800 border border-rose-200">{pct}% High</span>;
    }
    if (score >= 0.35) {
      return <span className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-800 border border-amber-200">{pct}% Med</span>;
    }
    return <span className="px-1.5 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-200">{pct}% Low</span>;
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-8">
      {/* Platform Banner */}
      <div className="p-6 rounded-2xl glass-panel relative overflow-hidden">
        <div className="absolute -top-12 -right-12 w-48 h-48 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 relative z-10">
          <div>
            <div className="inline-flex items-center space-x-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 mb-2">
              <Sparkles className="w-3 h-3 text-indigo-400" />
              <span>Deep Learning Content Filter Active</span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              Community Discourse Feed
            </h1>
            <p className="text-sm text-slate-400 mt-1 max-w-xl">
              Every comment submitted is evaluated in real-time by a Hybrid CNN + BiLSTM model. 
              Civil contributions pass instantly, while toxic speech is auto-flagged or blocked.
            </p>
          </div>
          <button
            onClick={fetchFeed}
            className="self-start sm:self-center flex items-center space-x-1.5 px-3 py-2 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-700 text-xs font-medium transition"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Refresh</span>
          </button>
        </div>
      </div>

      {/* Post Comment Input Box */}
      <div className="p-5 sm:p-6 rounded-2xl glass-panel border border-slate-800">
        <h2 className="text-sm font-semibold text-slate-200 mb-3 flex items-center space-x-2">
          <MessageSquare className="w-4 h-4 text-indigo-400" />
          <span>Join the Conversation</span>
        </h2>

        <form onSubmit={handlePost} className="space-y-3">
          <div className="relative">
            <textarea
              rows={3}
              value={newText}
              onChange={(e) => setNewText(e.target.value)}
              placeholder={user ? "Share your perspective on this topic..." : "Sign in to post comments..."}
              disabled={!user || submitting}
              className="w-full p-3.5 text-sm bg-slate-950/80 border border-slate-800 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition resize-none disabled:opacity-60"
            />
            <div className="absolute bottom-2.5 right-3 text-[11px] text-slate-500 font-mono">
              {newText.length} / 5000
            </div>
          </div>

          <div className="flex items-center justify-between pt-1">
            <div className="text-xs text-slate-400 flex items-center space-x-1">
              <span className="w-2 h-2 rounded-full bg-emerald-400 inline-block animate-pulse"></span>
              <span>AI Policy: Zero-tolerance for hate speech & violent threats.</span>
            </div>

            {user ? (
              <button
                type="submit"
                disabled={submitting || !newText.trim()}
                className="flex items-center space-x-2 px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-medium text-xs shadow-md shadow-indigo-600/30 transition"
              >
                <Send className="w-3.5 h-3.5" />
                <span>{submitting ? "Analyzing..." : "Post Comment"}</span>
              </button>
            ) : (
              <button
                type="button"
                onClick={onRequireAuth}
                className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-xs shadow-md shadow-indigo-600/25 transition"
              >
                Sign In to Post
              </button>
            )}
          </div>
        </form>

        {/* Real-time Post Moderation Alert Banner */}
        {postFeedback && (
          <div
            className={`mt-4 p-4 rounded-xl border flex items-start space-x-3 text-xs animate-in fade-in slide-in-from-top-2 duration-200 ${
              postFeedback.type === "success"
                ? "bg-emerald-950/40 border-emerald-500/30 text-emerald-300"
                : postFeedback.type === "warning"
                ? "bg-amber-950/40 border-amber-500/30 text-amber-300"
                : "bg-rose-950/40 border-rose-500/30 text-rose-300"
            }`}
          >
            {postFeedback.type === "success" && <CheckCircle className="w-4 h-4 shrink-0 mt-0.5" />}
            {postFeedback.type === "warning" && <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5" />}
            {postFeedback.type === "blocked" && <ShieldX className="w-4 h-4 shrink-0 mt-0.5" />}
            <div>
              <p className="font-semibold">{postFeedback.message}</p>
              {postFeedback.type !== "success" && (
                <p className="text-[11px] opacity-80 mt-0.5">
                  Our system evaluates severity across 6 distinct categories: toxic, severe toxic, obscene, threat, insult, and identity hate.
                </p>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Feed Filters */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center space-x-2">
          <Filter className="w-4 h-4 text-slate-400" />
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Feed Filter:</span>
        </div>
        <div className="flex space-x-1.5">
          {[
            { id: "approved", label: "Approved Only" },
            { id: "flagged", label: "Flagged" },
            { id: "all", label: "All Comments" },
          ].map((f) => (
            <button
              key={f.id}
              onClick={() => setStatusFilter(f.id)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition ${
                statusFilter === f.id
                  ? "bg-indigo-600 text-white"
                  : "bg-slate-900 text-slate-400 hover:text-slate-200"
              }`}
            >
              {f.label}
            </button>
          ))}
        </div>
      </div>

      {/* Comments List */}
      <div className="space-y-4">
        {loading ? (
          <div className="text-center py-12 text-slate-500 text-sm">Loading feed comments...</div>
        ) : comments.length === 0 ? (
          <div className="text-center py-12 text-slate-500 text-sm">No comments found matching this filter.</div>
        ) : (
          comments.map((c) => (
            <div
              key={c.id}
              className={`p-5 rounded-2xl glass-panel transition border ${
                c.status === "blocked"
                  ? "border-rose-900/60 bg-rose-950/10"
                  : c.status === "flagged"
                  ? "border-amber-900/60 bg-amber-950/10"
                  : "border-slate-800/80 hover:border-slate-700/80"
              }`}
            >
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-600 via-indigo-500 to-beige-600 flex items-center justify-center text-xs font-bold text-white uppercase shadow-sm">
                    {c.author?.username ? c.author.username[0] : "U"}
                  </div>
                  <div>
                    <div className="flex items-center space-x-2">
                      <span className="text-xs font-semibold text-slate-200">
                        {c.author?.username || "Anonymous"}
                      </span>
                      {c.author?.role === "admin" && (
                        <span className="px-1.5 py-0.2 bg-rose-500/20 text-rose-300 text-[10px] font-bold rounded border border-rose-500/30">
                          ADMIN
                        </span>
                      )}
                    </div>
                    <span className="text-[11px] text-slate-500 flex items-center space-x-1">
                      <Clock className="w-3 h-3" />
                      <span>{new Date(c.created_at).toLocaleDateString()}</span>
                    </span>
                  </div>
                </div>

                {/* Status Badge */}
                <div className="flex items-center space-x-2">
                  {c.status === "approved" && (
                    <span className="px-2 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 flex items-center space-x-1">
                      <CheckCircle className="w-3 h-3" />
                      <span>Approved</span>
                    </span>
                  )}
                  {c.status === "flagged" && (
                    <span className="px-2 py-0.5 rounded-full text-[11px] font-semibold bg-amber-500/15 text-amber-400 border border-amber-500/30 flex items-center space-x-1">
                      <AlertTriangle className="w-3 h-3" />
                      <span>Under Review</span>
                    </span>
                  )}
                  {c.status === "blocked" && (
                    <span className="px-2 py-0.5 rounded-full text-[11px] font-semibold bg-rose-500/15 text-rose-400 border border-rose-500/30 flex items-center space-x-1">
                      <ShieldX className="w-3 h-3" />
                      <span>Blocked</span>
                    </span>
                  )}
                </div>
              </div>

              {/* Text */}
              <p className="text-sm text-slate-300 leading-relaxed break-words">{c.text}</p>

              {/* Toxicity Category Probabilities Bar */}
              <div className="mt-4 pt-3 border-t border-slate-800/60 flex flex-wrap items-center gap-2 text-xs">
                <span className="text-[11px] text-slate-500 font-semibold uppercase tracking-wider mr-1">
                  AI Scores:
                </span>
                <span className="text-[11px] text-slate-400">Toxic: {getScoreBadge(c.toxic)}</span>
                <span className="text-[11px] text-slate-400">Severe: {getScoreBadge(c.severe_toxic)}</span>
                <span className="text-[11px] text-slate-400">Obscene: {getScoreBadge(c.obscene)}</span>
                <span className="text-[11px] text-slate-400">Threat: {getScoreBadge(c.threat)}</span>
                <span className="text-[11px] text-slate-400">Insult: {getScoreBadge(c.insult)}</span>
                <span className="text-[11px] text-slate-400">Hate: {getScoreBadge(c.identity_hate)}</span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
