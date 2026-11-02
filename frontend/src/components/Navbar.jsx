import React from "react";
import { ShieldAlert, Activity, MessageSquare, BarChart3, Cpu, User, LogOut, LogIn, Lock } from "lucide-react";

export default function Navbar({ activeTab, setActiveTab, user, onOpenAuth, onLogout }) {
  return (
    <header className="sticky top-0 z-40 border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand Logo */}
          <div className="flex items-center space-x-3 cursor-pointer" onClick={() => setActiveTab("feed")}>
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-amber-600 to-indigo-500 p-0.5 shadow-md shadow-indigo-600/20">
              <div className="w-full h-full bg-[#FCFBF8] rounded-[10px] flex items-center justify-center">
                <ShieldAlert className="w-5 h-5 text-indigo-600" />
              </div>
            </div>
            <div>
              <span className="text-lg font-extrabold tracking-tight text-slate-100">
                ToxicGuard<span className="text-indigo-600">AI</span>
              </span>
              <div className="flex items-center space-x-1.5">
                <p className="text-[10px] text-slate-500 uppercase tracking-widest font-semibold">Moderation System</p>
                <span className="px-1.5 py-0.2 rounded-full text-[9px] font-semibold bg-indigo-100 text-indigo-700 border border-indigo-200">Beige & Olive</span>
              </div>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="hidden md:flex items-center space-x-1">
            <button
              onClick={() => setActiveTab("feed")}
              className={`flex items-center space-x-2 px-3.5 py-2 rounded-lg text-sm font-medium transition-all duration-150 ${
                activeTab === "feed"
                  ? "bg-indigo-600/15 text-indigo-700 border border-indigo-600/30 font-semibold shadow-sm shadow-indigo-600/10"
                  : "text-slate-600 hover:text-slate-900 hover:bg-slate-900/60"
              }`}
            >
              <MessageSquare className="w-4 h-4 text-indigo-600" />
              <span>Social Feed</span>
            </button>

            <button
              onClick={() => setActiveTab("live-check")}
              className={`flex items-center space-x-2 px-3.5 py-2 rounded-lg text-sm font-medium transition-all duration-150 ${
                activeTab === "live-check"
                  ? "bg-indigo-600/15 text-indigo-700 border border-indigo-600/30 font-semibold shadow-sm shadow-indigo-600/10"
                  : "text-slate-600 hover:text-slate-900 hover:bg-slate-900/60"
              }`}
            >
              <Activity className="w-4 h-4 text-emerald-600" />
              <span>Live Check</span>
            </button>

            <button
              onClick={() => setActiveTab("admin")}
              className={`flex items-center space-x-2 px-3.5 py-2 rounded-lg text-sm font-medium transition-all duration-150 ${
                activeTab === "admin"
                  ? "bg-indigo-600/15 text-indigo-700 border border-indigo-600/30 font-semibold shadow-sm shadow-indigo-600/10"
                  : "text-slate-600 hover:text-slate-900 hover:bg-slate-900/60"
              }`}
            >
              <BarChart3 className="w-4 h-4 text-rose-600" />
              <span>Admin Dashboard</span>
              {(!user || user.role !== "admin") && (
                <Lock className="w-3 h-3 text-slate-500 ml-0.5" />
              )}
            </button>

            <button
              onClick={() => setActiveTab("performance")}
              className={`flex items-center space-x-2 px-3.5 py-2 rounded-lg text-sm font-medium transition-all duration-150 ${
                activeTab === "performance"
                  ? "bg-indigo-600/15 text-indigo-700 border border-indigo-600/30 font-semibold shadow-sm shadow-indigo-600/10"
                  : "text-slate-600 hover:text-slate-900 hover:bg-slate-900/60"
              }`}
            >
              <Cpu className="w-4 h-4 text-amber-600" />
              <span>Model Performance</span>
            </button>
          </nav>

          {/* User Profile / Auth Action */}
          <div className="flex items-center space-x-3">
            {user ? (
              <div className="flex items-center space-x-3">
                <div className="text-right hidden sm:block">
                  <div className="text-xs font-semibold text-slate-200">{user.username}</div>
                  <span
                    className={`inline-block px-1.5 py-0.2 rounded text-[10px] font-bold uppercase tracking-wider ${
                      user.role === "admin"
                        ? "bg-rose-500/20 text-rose-300 border border-rose-500/30"
                        : "bg-indigo-500/20 text-indigo-300 border border-indigo-500/30"
                    }`}
                  >
                    {user.role}
                  </span>
                </div>
                <button
                  onClick={onLogout}
                  title="Sign Out"
                  className="p-2 rounded-lg bg-slate-900 hover:bg-rose-950/40 text-slate-400 hover:text-rose-300 border border-slate-800 transition-colors"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <button
                onClick={onOpenAuth}
                className="flex items-center space-x-1.5 px-3.5 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-xs shadow-md shadow-indigo-600/25 transition-all"
              >
                <LogIn className="w-3.5 h-3.5" />
                <span>Sign In / Demo</span>
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Mobile Nav Bar */}
      <div className="md:hidden flex border-t border-slate-800/60 px-2 py-1.5 justify-around bg-slate-950/90 text-xs">
        <button
          onClick={() => setActiveTab("feed")}
          className={`py-1 px-2.5 rounded ${activeTab === "feed" ? "text-indigo-400 font-semibold" : "text-slate-400"}`}
        >
          Feed
        </button>
        <button
          onClick={() => setActiveTab("live-check")}
          className={`py-1 px-2.5 rounded ${activeTab === "live-check" ? "text-indigo-400 font-semibold" : "text-slate-400"}`}
        >
          Live Check
        </button>
        <button
          onClick={() => setActiveTab("admin")}
          className={`py-1 px-2.5 rounded ${activeTab === "admin" ? "text-indigo-400 font-semibold" : "text-slate-400"}`}
        >
          Admin
        </button>
        <button
          onClick={() => setActiveTab("performance")}
          className={`py-1 px-2.5 rounded ${activeTab === "performance" ? "text-indigo-400 font-semibold" : "text-slate-400"}`}
        >
          Models
        </button>
      </div>
    </header>
  );
}
