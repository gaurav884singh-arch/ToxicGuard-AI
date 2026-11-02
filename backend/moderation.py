"""
Model Inference & Real-Time Moderation Engine
Toxic Comment Moderation System

Loads deep learning model (Hybrid CNN + BiLSTM) and calibrated baseline.
Applies automated classification and content policy thresholds.
"""

import os
import sys
import pickle
import numpy as np
from typing import Dict, Any, List, Tuple

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.nlp.preprocess import TextPreprocessor
from src.models.deep_models import HybridCNNBiLSTM
from src.models.baseline import TFIDFBaseline

MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
LABELS = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]

# Moderation Thresholds
BLOCK_THRESHOLD = 0.65
FLAG_THRESHOLD = 0.35
HIGH_SEVERITY_BLOCK = 0.40  # Lower threshold for threat and severe toxicity


class ModerationEngine:
    """Singleton moderation inference engine combining Deep Learning & Calibrated Feature Models."""

    def __init__(self):
        self.preprocessor: TextPreprocessor = None
        self.deep_model: Any = None
        self.baseline_model: Any = None
        self.is_loaded: bool = False

    def load_artifacts(self) -> None:
        """Loads serialized tokenizer, deep learning model, and calibrated baseline."""
        if self.is_loaded:
            return

        tokenizer_path = os.path.join(MODELS_DIR, "tokenizer.pkl")
        best_model_path = os.path.join(MODELS_DIR, "best_model.pkl")
        baseline_path = os.path.join(MODELS_DIR, "calibrated_baseline.pkl")

        if os.path.exists(tokenizer_path):
            self.preprocessor = TextPreprocessor.load_tokenizer(tokenizer_path)
            print(f"[Moderation Engine] Loaded Tokenizer from: {tokenizer_path}")
        else:
            self.preprocessor = TextPreprocessor()

        if os.path.exists(best_model_path):
            with open(best_model_path, "rb") as f:
                self.deep_model = pickle.load(f)
            print(f"[Moderation Engine] Loaded Deep Learning Model: {self.deep_model.name}")
        else:
            self.deep_model = HybridCNNBiLSTM(vocab_size=10000, emb_dim=48, num_filters=48, kernel_size=3, lstm_units=36)

        if os.path.exists(baseline_path):
            with open(baseline_path, "rb") as f:
                self.baseline_model = pickle.load(f)
            print(f"[Moderation Engine] Loaded Calibrated Feature Model: {self.baseline_model.name}")

        self.is_loaded = True

    def predict(self, text: str) -> Dict[str, Any]:
        """Runs end-to-end inference on user comment string."""
        if not self.is_loaded:
            self.load_artifacts()

        cleaned = self.preprocessor.tokenize_and_lemmatize(text)
        if not cleaned:
            zero_scores = {lbl: 0.0 for lbl in LABELS}
            return {
                "text": text,
                "cleaned_text": "",
                "scores": zero_scores,
                "max_score": 0.0,
                "is_toxic": False,
                "status": "approved",
                "verdict": "Clean (Approved)",
                "flagged_categories": [],
            }

        # 1. Deep Learning forward pass
        seq = self.preprocessor.texts_to_padded_sequences([cleaned], maxlen=50)
        deep_probs = self.deep_model.predict_proba(seq)[0]

        # 2. Calibrated Feature model forward pass
        if self.baseline_model is not None:
            baseline_probs = self.baseline_model.predict_proba([text])[0]
            # Ensemble fusion: 40% deep contextual representations + 60% calibrated n-gram TF-IDF
            probs = 0.40 * deep_probs + 0.60 * baseline_probs
        else:
            probs = deep_probs

        # Format scores
        scores: Dict[str, float] = {}
        for idx, lbl in enumerate(LABELS):
            scores[lbl] = round(float(np.clip(probs[idx], 0.0, 1.0)), 4)

        max_score = round(float(np.max(list(scores.values()))), 4)
        flagged_cats = [lbl for lbl, val in scores.items() if val >= FLAG_THRESHOLD]

        # Policy decision
        is_high_severity = (scores["threat"] >= HIGH_SEVERITY_BLOCK) or (scores["severe_toxic"] >= HIGH_SEVERITY_BLOCK)

        if max_score >= BLOCK_THRESHOLD or is_high_severity:
            status = "blocked"
            verdict = "Toxic (Blocked)"
            is_toxic = True
        elif max_score >= FLAG_THRESHOLD:
            status = "flagged"
            verdict = "Potentially Toxic (Flagged for Review)"
            is_toxic = True
        else:
            status = "approved"
            verdict = "Clean (Approved)"
            is_toxic = False

        return {
            "text": text,
            "cleaned_text": cleaned,
            "scores": scores,
            "max_score": max_score,
            "is_toxic": is_toxic,
            "status": status,
            "verdict": verdict,
            "flagged_categories": flagged_cats,
        }


# Global engine singleton
moderation_engine = ModerationEngine()
