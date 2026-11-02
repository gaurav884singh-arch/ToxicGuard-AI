import React, { useState } from "react";
import { X, ShieldCheck, UserCheck, AlertCircle, Loader2 } from "lucide-react";
import { api, authStorage } from "../api";

export default function AuthModal({ isOpen, onClose, onAuthSuccess }) {
  const [isLogin, setIsLogin] = useState(true);
  const [usernameOrEmail, setUsernameOrEmail] = useState("");
  const [password, setPassword] = useState("");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [role, setRole] = useState("user");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      let data;
      if (isLogin) {
        data = await api.login(usernameOrEmail, password);
      } else {
        data = await api.register(username, email, password, role);
      }

      authStorage.setToken(data.access_token);
      authStorage.setUser(data.user);
      onAuthSuccess(data.user);
      onClose();
    } catch (err) {
      setError(err.message || "Authentication failed. Please verify details.");
    } finally {
      setLoading(false);
    }
  };

  const handleDemoLogin = async (demoRole) => {
    setError("");
    setLoading(true);
    try {
      const emailVal = demoRole === "admin" ? "admin@moderation.ai" : "user@social.com";
      const passVal = demoRole === "admin" ? "Admin@1234" : "User@1234";
      const data = await api.login(emailVal, passVal);
      authStorage.setToken(data.access_token);
      authStorage.setUser(data.user);
      onAuthSuccess(data.user);
      onClose();
    } catch (err) {
      setError("Demo credentials failed. Please verify database seeding.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
      <div className="relative w-full max-w-md bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl p-6 sm:p-8 text-slate-100 overflow-hidden">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-1.5 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded-lg transition"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Header */}
        <div className="mb-6">
          <h2 className="text-xl font-bold text-white tracking-tight">
            {isLogin ? "Welcome Back" : "Create Account"}
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            {isLogin
              ? "Sign in to post comments or access the moderation dashboard."
              : "Register to participate in the moderated community."}
          </p>
        </div>

        {/* Quick Demo Buttons for Evaluators */}
        <div className="mb-6 p-3 rounded-xl bg-slate-950/70 border border-indigo-950/50">
          <p className="text-[11px] font-semibold text-indigo-400 uppercase tracking-wider mb-2">
            🚀 1-Click Evaluation Accounts
          </p>
          <div className="grid grid-cols-2 gap-2">
            <button
              type="button"
              onClick={() => handleDemoLogin("admin")}
              disabled={loading}
              className="flex items-center justify-center space-x-1.5 py-2 px-3 rounded-lg bg-rose-600/20 hover:bg-rose-600/30 text-rose-300 border border-rose-500/30 text-xs font-semibold transition"
            >
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>Admin Demo</span>
            </button>
            <button
              type="button"
              onClick={() => handleDemoLogin("user")}
              disabled={loading}
              className="flex items-center justify-center space-x-1.5 py-2 px-3 rounded-lg bg-indigo-600/20 hover:bg-indigo-600/30 text-indigo-300 border border-indigo-500/30 text-xs font-semibold transition"
            >
              <UserCheck className="w-3.5 h-3.5" />
              <span>User Demo</span>
            </button>
          </div>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="mb-4 flex items-start space-x-2 p-3 rounded-lg bg-rose-950/40 border border-rose-800/60 text-rose-300 text-xs">
            <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
            <span>{error}</span>
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          {isLogin ? (
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">Username or Email</label>
              <input
                type="text"
                required
                value={usernameOrEmail}
                onChange={(e) => setUsernameOrEmail(e.target.value)}
                placeholder="admin@moderation.ai"
                className="w-full px-3.5 py-2 text-sm bg-slate-950/80 border border-slate-700/80 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
              />
            </div>
          ) : (
            <>
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Username</label>
                <input
                  type="text"
                  required
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="alex_dev"
                  className="w-full px-3.5 py-2 text-sm bg-slate-950/80 border border-slate-700/80 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Email</label>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="alex@dev.io"
                  className="w-full px-3.5 py-2 text-sm bg-slate-950/80 border border-slate-700/80 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                />
              </div>
            </>
          )}

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">Password</label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full px-3.5 py-2 text-sm bg-slate-950/80 border border-slate-700/80 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2.5 px-4 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-medium text-sm rounded-lg shadow-lg shadow-indigo-600/30 flex items-center justify-center space-x-2 transition"
          >
            {loading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <span>{isLogin ? "Sign In" : "Register"}</span>
            )}
          </button>
        </form>

        {/* Toggle between Sign In / Sign Up */}
        <div className="mt-5 text-center">
          <button
            type="button"
            onClick={() => {
              setIsLogin(!isLogin);
              setError("");
            }}
            className="text-xs text-indigo-400 hover:text-indigo-300 font-medium transition"
          >
            {isLogin
              ? "Don't have an account? Sign up here"
              : "Already have an account? Sign in here"}
          </button>
        </div>
      </div>
    </div>
  );
}
