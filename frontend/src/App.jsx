import React, { useState, useEffect } from "react";
import Navbar from "./components/Navbar";
import AuthModal from "./components/AuthModal";
import FeedPage from "./pages/FeedPage";
import LiveCheckPage from "./pages/LiveCheckPage";
import AdminDashboard from "./pages/AdminDashboard";
import ModelPerformancePage from "./pages/ModelPerformancePage";
import { authStorage } from "./api";
import { ShieldCheck, BookOpen, ExternalLink, Code2 } from "lucide-react";

export default function App() {
  const [activeTab, setActiveTab] = useState("feed");
  const [user, setUser] = useState(null);
  const [isAuthOpen, setIsAuthOpen] = useState(false);

  useEffect(() => {
    const savedUser = authStorage.getUser();
    if (savedUser) {
      setUser(savedUser);
    }
  }, []);

  const handleAuthSuccess = (authenticatedUser) => {
    setUser(authenticatedUser);
  };

  const handleLogout = () => {
    authStorage.clear();
    setUser(null);
    if (activeTab === "admin") {
      setActiveTab("feed");
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      {/* Navbar */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        user={user}
        onOpenAuth={() => setIsAuthOpen(true)}
        onLogout={handleLogout}
      />

      {/* Main Content Body */}
      <main className="flex-1">
        {activeTab === "feed" && (
          <FeedPage user={user} onRequireAuth={() => setIsAuthOpen(true)} />
        )}
        {activeTab === "live-check" && <LiveCheckPage />}
        {activeTab === "admin" && (
          <AdminDashboard user={user} onRequireAuth={() => setIsAuthOpen(true)} />
        )}
        {activeTab === "performance" && <ModelPerformancePage />}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-900 bg-slate-950/90 py-8 px-4 text-xs text-slate-500">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center space-x-2">
            <ShieldCheck className="w-4 h-4 text-indigo-400" />
            <span className="font-semibold text-slate-300">
              Toxic Comment Moderation System
            </span>
            <span>• College Capstone Project</span>
            <span className="hidden sm:inline px-2 py-0.5 rounded-full text-[10px] font-semibold bg-beige-950/80 text-beige-300 border border-beige-800/60">Olive & Beige Edition</span>
          </div>

          <div className="flex items-center space-x-4">
            <span className="text-slate-400">
              Stack: <span className="text-slate-300 font-mono">NLP + PyTorch/Keras + FastAPI + React</span>
            </span>
            <a
              href="http://127.0.0.1:8000/docs"
              target="_blank"
              rel="noopener noreferrer"
              className="text-indigo-400 hover:text-indigo-300 flex items-center space-x-1 transition"
            >
              <span>Swagger API Docs</span>
              <ExternalLink className="w-3 h-3" />
            </a>
          </div>
        </div>
      </footer>

      {/* Authentication Modal */}
      <AuthModal
        isOpen={isAuthOpen}
        onClose={() => setIsAuthOpen(false)}
        onAuthSuccess={handleAuthSuccess}
      />
    </div>
  );
}
