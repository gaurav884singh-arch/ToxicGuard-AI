/**
 * API Client & Network Service
 * Toxic Comment Moderation System
 */

const API_BASE = ""; // Relative path proxies to backend via Vite in dev

export const authStorage = {
  getToken: () => localStorage.getItem("toxic_mod_token"),
  setToken: (token) => localStorage.setItem("toxic_mod_token", token),
  getUser: () => {
    const raw = localStorage.getItem("toxic_mod_user");
    return raw ? JSON.parse(raw) : null;
  },
  setUser: (user) => localStorage.setItem("toxic_mod_user", JSON.stringify(user)),
  clear: () => {
    localStorage.removeItem("toxic_mod_token");
    localStorage.removeItem("toxic_mod_user");
  },
};

async function request(endpoint, options = {}) {
  const token = authStorage.getToken();
  const headers = {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  };

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: "Network request failed" }));
    throw new Error(errorData.detail || `Request failed with status ${response.status}`);
  }

  return response.json();
}

export const api = {
  // Auth
  login: (username_or_email, password) =>
    request("/api/auth/login", {
      method: "POST",
      body: JSON.stringify({ username_or_email, password }),
    }),

  register: (username, email, password, role = "user") =>
    request("/api/auth/register", {
      method: "POST",
      body: JSON.stringify({ username, email, password, role }),
    }),

  getProfile: () => request("/api/auth/me"),

  // Prediction (Live Check)
  predict: (text) =>
    request("/api/predict", {
      method: "POST",
      body: JSON.stringify({ text }),
    }),

  // Comments Feed
  getComments: (status_filter = "approved", limit = 50) =>
    request(`/api/comments?status_filter=${status_filter}&limit=${limit}`),

  createComment: (text) =>
    request("/api/comments", {
      method: "POST",
      body: JSON.stringify({ text }),
    }),

  // Admin Queue & Actions
  getFlaggedQueue: () => request("/api/admin/flagged"),

  moderateComment: (id, action, notes = "") =>
    request(`/api/admin/comments/${id}`, {
      method: "PUT",
      body: JSON.stringify({ action, notes }),
    }),

  getAdminAnalytics: () => request("/api/admin/analytics"),

  // Model Evaluation Benchmark
  getModelComparison: () => request("/api/models/comparison"),
};
