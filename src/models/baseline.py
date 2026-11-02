"""
Baseline Machine Learning Models for Multi-Label Toxicity Classification
Toxic Comment Moderation System

Models:
1. TF-IDF + Logistic Regression (One-Vs-Rest / MultiOutput)
2. TF-IDF + Linear Support Vector Classifier (LinearSVC with Calibrated probabilities)
"""

import os
import pickle
import numpy as np
from typing import Dict, Any, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.calibration import CalibratedClassifierCV

LABELS = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]


class TFIDFBaseline:
    """Wrapper for TF-IDF feature extraction and multi-label linear classifiers."""

    def __init__(
        self,
        classifier_type: str = "logistic_regression",
        max_features: int = 10000,
        ngram_range: Tuple[int, int] = (1, 2),
    ):
        self.classifier_type = classifier_type
        self.max_features = max_features
        self.ngram_range = ngram_range
        self.name = (
            "TF-IDF + Logistic Regression"
            if classifier_type == "logistic_regression"
            else "TF-IDF + Linear SVM"
        )

        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            sublinear_tf=True,
            strip_accents="unicode",
        )

        if classifier_type == "logistic_regression":
            base_estimator = LogisticRegression(
                C=2.0,
                max_iter=1000,
                class_weight="balanced",
                solver="lbfgs",
                random_state=42,
            )
            self.model = OneVsRestClassifier(base_estimator)
        elif classifier_type == "linear_svm":
            base_svc = LinearSVC(
                C=1.0,
                max_iter=2000,
                class_weight="balanced",
                random_state=42,
            )
            # CalibratedClassifierCV enables predict_proba for SVM
            calibrated = CalibratedClassifierCV(base_svc, cv=3)
            self.model = OneVsRestClassifier(calibrated)
        else:
            raise ValueError(f"Unsupported classifier type: {classifier_type}")

    def fit(self, texts: list, y: np.ndarray) -> "TFIDFBaseline":
        print(f"[{self.name}] Fitting TF-IDF Vectorizer...")
        X_tfidf = self.vectorizer.fit_transform(texts)
        print(f"[{self.name}] Training multi-label classifier...")
        self.model.fit(X_tfidf, y)
        return self

    def predict_proba(self, texts: list) -> np.ndarray:
        X_tfidf = self.vectorizer.transform(texts)
        return self.model.predict_proba(X_tfidf)

    def predict(self, texts: list, threshold: float = 0.5) -> np.ndarray:
        probs = self.predict_proba(texts)
        return (probs >= threshold).astype(int)

    def save(self, filepath: str) -> None:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, filepath: str) -> "TFIDFBaseline":
        with open(filepath, "rb") as f:
            return pickle.load(f)
