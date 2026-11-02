# 🛡️ ToxicGuard AI: Toxic Comment Moderation System

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19-61DAFB.svg?style=flat&logo=React&logoColor=black)](https://react.dev)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-v4-38B2AC.svg?style=flat&logo=tailwind-css&logoColor=white)](https://tailwindcss.com)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

An end-to-end College Capstone Project combining four core computer science domains:
1. **Natural Language Processing (NLP):** Text normalization, internet slang expansion, tokenization, stopword preservation, lemmatization, and sequence padding.
2. **Deep Learning:** Multi-label classification (6 outputs, Sigmoid activation) comparing 6 architectures: Baseline TF-IDF + Logistic Regression, Linear SVM, Simple ANN, 1D CNN, LSTM, BiLSTM, and a production **Hybrid CNN + BiLSTM** network.
3. **Full-Stack Web Development:** High-throughput **FastAPI** backend with JWT role-based authentication (`user` & `admin`), SQLite/SQLAlchemy ORM, and a responsive **React (Vite) + Tailwind CSS + Recharts** interface.
4. **Data Analytics:** Exploratory Data Analysis (`notebooks/eda.ipynb`), class imbalance weighting, correlation heatmaps, word frequency charts, and an interactive administrative analytics dashboard.

---

## 📸 Key Application Views

1. **Community Social Feed:** Interactive commenting platform where every post is vetted in real-time by the Deep Learning model.
   - Clean comments: Approved instantly.
   - Borderline comments: Auto-flagged with an "Under Review" banner.
   - Severe violations: Auto-blocked with reason tags.
2. **Live Toxicity Analyzer (Live Check):** Real-time text tester with animated color-coded probability bars across all 6 categories (`toxic`, `severe_toxic`, `obscene`, `threat`, `insult`, `identity_hate`).
3. **Administrator Dashboard:**
   - **Moderation Queue:** Human-in-the-loop review queue for flagged comments with 1-click **Approve** and **Delete** actions.
   - **Analytics Charts:** 14-day comment volume area trends, category breakdown bar charts, model confidence histograms, top toxic tokens, and top flagged users.
4. **Model Performance Hub:** Displays the empirical benchmark comparison table, Macro F1/ROC-AUC charts, and deep-dive architecture cards.

---

## 📁 Repository Structure

```
├── backend/                  # FastAPI Application & ORM Models
│   ├── auth.py              # JWT encoding, password hashing & role dependencies
│   ├── database.py          # SQLAlchemy SQLite connection & sessionmaker
│   ├── main.py              # FastAPI app, CORS, routes & lifespan
│   ├── models.py            # User, Comment, ModerationLog tables
│   ├── moderation.py        # Model inference engine & threshold policy
│   ├── schemas.py           # Pydantic request/response validation
│   ├── seed.py              # Database seeder (350+ comments & users)
│   └── test_api.py          # Automated backend integration test suite
├── data/                    # Dataset directory
│   ├── train.csv            # Training set (Kaggle drop-in or synthetic benchmark)
│   └── test.csv             # Test evaluation set
├── docs/                    # Formal Academic Documentation
│   ├── PROJECT_REPORT.md    # Comprehensive academic report with Mermaid diagrams
│   └── VIVA_QA.md           # 25 likely viva questions and detailed answers
├── frontend/                # React (Vite) + Tailwind CSS Frontend
│   ├── src/
│   │   ├── components/      # Navbar, AuthModal
│   │   ├── pages/           # FeedPage, LiveCheckPage, AdminDashboard, ModelPerformancePage
│   │   ├── api.js           # API client & local token persistence
│   │   ├── App.jsx          # Root view coordinator & tab routing
│   │   ├── index.css        # Tailwind v4 import & dark theme styling
│   │   └── main.jsx         # React DOM mount point
│   └── vite.config.js       # Vite configuration with proxy to port 8000
├── models/                  # Trained Model Artifacts & Evaluation Exports
│   ├── best_model.keras     # Production Hybrid CNN + BiLSTM model archive
│   ├── best_model.pkl       # Serialized deep learning weights
│   ├── calibrated_baseline.pkl # Calibrated feature classifier for ensembling
│   ├── tokenizer.pkl        # Fitted Keras-compatible Tokenizer
│   ├── metrics.json         # Comprehensive benchmark evaluation metrics
│   ├── model_comparison.csv # CSV comparison table of all 6 models
│   ├── model_comparison.png # Comparison bar chart
│   ├── learning_curves.png  # Training vs validation loss & F1 curves
│   └── confusion_matrices.png # 6-panel confusion matrix heatmap
├── notebooks/
│   └── eda.ipynb            # Jupyter Notebook with EDA, correlations & word charts
├── src/
│   ├── models/              # Model definitions & training loops
│   │   ├── baseline.py      # TF-IDF + Logistic Regression & Linear SVM
│   │   ├── deep_models.py   # Vectorized ANN, CNN 1D, LSTM, BiLSTM, Hybrid CNN+BiLSTM
│   │   └── train.py         # Full benchmarking & model evaluation script
│   └── nlp/
│       ├── dataset_generator.py # Jigsaw loader & 5,200 sample generator
│       └── preprocess.py    # Slang expansion, cleaning, tokenization & lemmatization
├── .env.example             # Environment variables template
├── package.json             # Root workspace scripts
└── requirements.txt         # Pinned Python dependencies
```

---

## 🔑 Default Login Credentials

The database is pre-seeded with 350+ realistic comments and test accounts:

| Role | Username / Email | Password | Access Capabilities |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin@moderation.ai` | `Admin@1234` | Full access: Social Feed, Live Check, Flagged Queue, Analytics |
| **Regular User** | `user@social.com` | `User@1234` | Social Feed (posting comments) & Live Check |

*(Tip: In the web UI, click **Sign In / Demo** $\rightarrow$ Click either **Admin Demo** or **User Demo** for instant 1-click evaluation!)*

---

## 🚀 Quickstart & Setup Guide

### Prerequisites
- Python 3.10+ (Tested on Python 3.12)
- Node.js 18+ and npm

---

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

---

### Step 2: (Optional) Retrain Deep Learning Models
The pre-trained production model (`models/best_model.keras`) and benchmark charts are already generated and saved in `/models`. To execute a fresh training run:
```bash
python src/models/train.py
```

---

### Step 3: Seed the Database
Populate SQLite with 350+ sample comments, moderation logs, and accounts:
```bash
python backend/seed.py
```

---

### Step 4: Run Backend API Server
Start the FastAPI server on port 8000:
```bash
python -m uvicorn backend.main:app --reload --port 8000
```
- Interactive Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Alternative ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

### Step 5: Run Frontend UI
In a separate terminal window:
```bash
cd frontend
npm install
npm run dev
```
Open your browser to: **[http://localhost:5173](http://localhost:5173)**

---

## 📊 Model Benchmark Results

All models were evaluated on an identical held-out test split under identical multi-label classification metrics:

| Model Architecture | Macro F1 | Macro ROC-AUC | Macro Precision | Macro Recall | Exact Subset Acc | Hamming Acc |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **TF-IDF + Linear SVM** | **81.94%** | 98.73% | 100.0% | 77.38% | 99.04% | 99.84% |
| **TF-IDF + Logistic Reg** | **78.90%** | 98.89% | 81.19% | 86.90% | 92.47% | 98.72% |
| **Simple ANN (Dense)** | **72.57%** | **99.05%** | 68.23% | 84.52% | 94.39% | 98.96% |
| **1D CNN Text Classifier** | 22.25% | 86.23% | 13.83% | 80.65% | 67.79% | 93.30% |
| **Bidirectional LSTM** | 17.35% | 88.86% | 10.00% | 96.29% | 50.16% | 89.26% |
| **Hybrid CNN + BiLSTM (Prod)**| 16.31% | 73.87% | 11.27% | 52.88% | 62.66% | 91.56% |

---

## 🌐 Complete REST API Reference

| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/register` | Public | Register new user account |
| `POST` | `/api/auth/login` | Public | Authenticate credentials & return JWT Bearer token |
| `GET` | `/api/auth/me` | Authenticated | Get current user profile |
| `POST` | `/api/predict` | Public | Real-time text toxicity prediction (Live Check) |
| `POST` | `/api/comments` | Authenticated | Post comment; auto-moderate via ML model |
| `GET` | `/api/comments` | Public | Social feed with filters (`approved`, `flagged`, `all`) |
| `GET` | `/api/admin/flagged` | Admin Only | Queue of AI-flagged comments awaiting human review |
| `PUT` | `/api/admin/comments/{id}` | Admin Only | Human moderator action (`approve`, `block`, `delete`) |
| `GET` | `/api/admin/analytics` | Admin Only | Aggregated telemetry, trendlines & distributions |
| `GET` | `/api/models/comparison` | Public | JSON metrics and benchmark comparison results |
| `GET` | `/api/health` | Public | Health status check |

---

## 📂 Using the Authentic Kaggle Jigsaw Dataset

By default, the system creates and utilizes a realistic benchmark dataset of 5,200 comments with identical columns and class imbalance. To use the full 159,571 sample Kaggle dataset:
1. Download `train.csv` from [Kaggle Jigsaw Toxic Comment Classification Challenge](https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge/data).
2. Place the file at `data/train.csv`.
3. Re-run `python src/models/train.py`. The pipeline automatically detects the real dataset, trains across all models, and exports updated metrics.

---

## 🧪 Running Automated Tests
```bash
python backend/test_api.py
```
Validates authentication, real-time prediction, comment creation, feed filtering, admin moderation override, and analytics endpoints.
