"""
Comprehensive Training & Model Comparison Pipeline
Toxic Comment Moderation System

Trains and benchmark compares 6 multi-label classification architectures:
1. TF-IDF + Logistic Regression (Baseline 1)
2. TF-IDF + Linear SVM (Baseline 2)
3. Simple ANN (Dense layers + Dropout + L2)
4. LSTM with Embedding layer
5. BiLSTM with embeddings
6. 1D CNN text classifier
7. Hybrid CNN + BiLSTM (Production model)

Evaluates:
- Label-wise and Macro Accuracy, Precision, Recall, F1-Score, ROC-AUC
- Confusion matrices
- Saves models/model_comparison.csv & models/model_comparison.png
- Saves models/best_model.keras, models/tokenizer.pkl, models/metrics.json
"""

import os
import sys
import json
import time
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Any

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    hamming_loss,
)

from src.nlp.dataset_generator import load_or_create_dataset, LABELS
from src.nlp.preprocess import TextPreprocessor, compute_pos_weights
from src.models.baseline import TFIDFBaseline
from src.models.deep_models import (
    DenseANN,
    TextCNN1D,
    TextLSTM,
    TextBiLSTM,
    HybridCNNBiLSTM,
    train_neural_model,
)

MODELS_DIR = os.path.join(PROJECT_ROOT, "models")
os.makedirs(MODELS_DIR, exist_ok=True)


def evaluate_multilabel_model(
    model_name: str,
    y_true: np.ndarray,
    y_prob: np.ndarray,
    threshold: float = 0.5,
) -> Dict[str, Any]:
    """Computes comprehensive multi-label evaluation metrics."""
    y_pred = (y_prob >= threshold).astype(int)

    # Subset exact match accuracy and Hamming loss
    subset_acc = float(accuracy_score(y_true, y_pred))
    h_loss = float(hamming_loss(y_true, y_pred))
    hamming_acc = 1.0 - h_loss

    # Macro and Micro metrics
    p_macro = float(precision_score(y_true, y_pred, average="macro", zero_division=0))
    p_micro = float(precision_score(y_true, y_pred, average="micro", zero_division=0))
    r_macro = float(recall_score(y_true, y_pred, average="macro", zero_division=0))
    r_micro = float(recall_score(y_true, y_pred, average="micro", zero_division=0))
    f1_macro = float(f1_score(y_true, y_pred, average="macro", zero_division=0))
    f1_micro = float(f1_score(y_true, y_pred, average="micro", zero_division=0))

    # ROC-AUC per label and Macro
    roc_auc_per_label = {}
    valid_aucs = []
    for idx, lbl in enumerate(LABELS):
        # Only compute if at least one positive sample exists
        if np.sum(y_true[:, idx]) > 0 and np.sum(y_true[:, idx]) < len(y_true):
            score = float(roc_auc_score(y_true[:, idx], y_prob[:, idx]))
            roc_auc_per_label[lbl] = round(score, 4)
            valid_aucs.append(score)
        else:
            roc_auc_per_label[lbl] = 0.5

    macro_roc_auc = float(np.mean(valid_aucs)) if valid_aucs else 0.5

    # Label-wise F1 scores
    f1_per_label = {}
    for idx, lbl in enumerate(LABELS):
        f1_per_label[lbl] = round(
            float(f1_score(y_true[:, idx], y_pred[:, idx], zero_division=0)), 4
        )

    return {
        "model_name": model_name,
        "subset_accuracy": round(subset_acc, 4),
        "hamming_accuracy": round(hamming_acc, 4),
        "precision_macro": round(p_macro, 4),
        "precision_micro": round(p_micro, 4),
        "recall_macro": round(r_macro, 4),
        "recall_micro": round(r_micro, 4),
        "f1_macro": round(f1_macro, 4),
        "f1_micro": round(f1_micro, 4),
        "roc_auc_macro": round(macro_roc_auc, 4),
        "roc_auc_per_label": roc_auc_per_label,
        "f1_per_label": f1_per_label,
    }


def plot_comparison_and_curves(
    results: List[Dict[str, Any]],
    histories: Dict[str, Dict[str, List[float]]],
    y_test: np.ndarray,
    best_probs: np.ndarray,
) -> None:
    """Renders and exports model comparison charts, training curves, and confusion matrix."""
    # 1. Comparison Bar Chart
    df_results = pd.DataFrame(results)
    df_results.to_csv(os.path.join(MODELS_DIR, "model_comparison.csv"), index=False)

    plt.figure(figsize=(12, 6))
    metrics_to_plot = ["f1_macro", "roc_auc_macro", "precision_macro", "recall_macro"]
    x = np.arange(len(df_results))
    width = 0.2

    for i, col in enumerate(metrics_to_plot):
        label_text = col.replace("_", " ").upper()
        plt.bar(x + i * width, df_results[col], width, label=label_text)

    plt.xlabel("Models", fontsize=12, fontweight="bold")
    plt.ylabel("Score", fontsize=12, fontweight="bold")
    plt.title("Toxicity Classification: Model Benchmark Comparison", fontsize=14, fontweight="bold")
    plt.xticks(x + width * 1.5, df_results["model_name"], rotation=25, ha="right")
    plt.ylim(0, 1.05)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.legend(loc="lower right")
    plt.tight_layout()
    chart_path = os.path.join(MODELS_DIR, "model_comparison.png")
    plt.savefig(chart_path, dpi=300)
    plt.close()
    print(f"[Plots] Saved comparison chart to: {chart_path}")

    # 2. Learning Curves for Deep Models
    if histories:
        plt.figure(figsize=(14, 5))
        plt.subplot(1, 2, 1)
        for name, hist in histories.items():
            if hist.get("loss"):
                plt.plot(hist["loss"], label=f"{name} (Train)")
                plt.plot(hist["val_loss"], linestyle="--", label=f"{name} (Val)")
        plt.title("Training & Validation Loss Curves", fontweight="bold")
        plt.xlabel("Epoch")
        plt.ylabel("Binary Cross-Entropy Loss")
        plt.legend(fontsize=8)
        plt.grid(True, linestyle=":", alpha=0.6)

        plt.subplot(1, 2, 2)
        for name, hist in histories.items():
            if hist.get("f1_macro"):
                plt.plot(hist["f1_macro"], label=f"{name} (Train F1)")
                plt.plot(hist["val_f1_macro"], linestyle="--", label=f"{name} (Val F1)")
        plt.title("Macro F1-Score Progression", fontweight="bold")
        plt.xlabel("Epoch")
        plt.ylabel("Macro F1")
        plt.legend(fontsize=8)
        plt.grid(True, linestyle=":", alpha=0.6)

        curves_path = os.path.join(MODELS_DIR, "learning_curves.png")
        plt.tight_layout()
        plt.savefig(curves_path, dpi=300)
        plt.close()
        print(f"[Plots] Saved learning curves to: {curves_path}")

    # 3. Confusion Matrix for Best Model (Hybrid CNN + BiLSTM)
    best_preds = (best_probs >= 0.5).astype(int)
    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    axes = axes.flatten()

    for idx, lbl in enumerate(LABELS):
        cm = confusion_matrix(y_test[:, idx], best_preds[:, idx])
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=axes[idx], cbar=False)
        axes[idx].set_title(f"Label: {lbl.upper()}", fontweight="bold")
        axes[idx].set_xlabel("Predicted")
        axes[idx].set_ylabel("Actual")
        axes[idx].set_xticklabels(["Non-Toxic", "Toxic"])
        axes[idx].set_yticklabels(["Non-Toxic", "Toxic"])

    plt.suptitle("Hybrid CNN + BiLSTM: Per-Label Confusion Matrices", fontsize=16, fontweight="bold")
    plt.tight_layout()
    cm_path = os.path.join(MODELS_DIR, "confusion_matrices.png")
    plt.savefig(cm_path, dpi=300)
    plt.close()
    print(f"[Plots] Saved confusion matrices to: {cm_path}")


def main():
    print("==========================================================================")
    print("PHASE 2: DEEP LEARNING MODEL TRAINING & BENCHMARK COMPARISON")
    print("==========================================================================")

    # 1. Dataset loading & splitting
    train_df, test_df = load_or_create_dataset(os.path.join(PROJECT_ROOT, "data"))
    raw_texts = train_df["comment_text"].astype(str).tolist()
    y_raw = train_df[LABELS].values.astype(np.float32)

    # 2. NLP Preprocessing
    print("\n[NLP Pipeline] Initializing TextPreprocessor...", flush=True)
    preprocessor = TextPreprocessor(max_vocab_size=10000, max_sequence_length=50)
    cleaned_texts = preprocessor.preprocess_corpus(raw_texts)

    # Fit Tokenizer & transform to padded sequences
    print("[NLP Pipeline] Fitting Tokenizer and generating padded sequences...", flush=True)
    preprocessor.fit_tokenizer(cleaned_texts)
    X_seq = preprocessor.texts_to_padded_sequences(cleaned_texts)

    # Save fitted Tokenizer to models/
    tokenizer_path = os.path.join(MODELS_DIR, "tokenizer.pkl")
    preprocessor.save_tokenizer(tokenizer_path)
    print(f"[NLP Pipeline] Tokenizer successfully serialized to: {tokenizer_path}", flush=True)

    # Split: 70% Train, 15% Val, 15% Test
    X_tr_seq, X_temp_seq, y_tr, y_temp, txt_tr, txt_temp = train_test_split(
        X_seq, y_raw, cleaned_texts, test_size=0.30, random_state=42
    )
    X_val_seq, X_te_seq, y_val, y_te, txt_val, txt_te = train_test_split(
        X_temp_seq, y_temp, txt_temp, test_size=0.50, random_state=42
    )

    pos_weights = compute_pos_weights(y_tr)
    print(f"\n[Data Split Summary]", flush=True)
    print(f"  Training Set:   {X_tr_seq.shape[0]} samples", flush=True)
    print(f"  Validation Set: {X_val_seq.shape[0]} samples", flush=True)
    print(f"  Test Set:       {X_te_seq.shape[0]} samples", flush=True)
    print(f"  Positive Class Weight Ratios: {dict(zip(LABELS, np.round(pos_weights, 2)))}", flush=True)

    benchmark_results: List[Dict[str, Any]] = []
    histories: Dict[str, Dict[str, List[float]]] = {}

    # ------------------------------------------------------------------------
    # Model 1: Baseline TF-IDF + Logistic Regression
    # ------------------------------------------------------------------------
    print("\n----------------------------------------------------------------------")
    print("Model 1/6: TF-IDF + Logistic Regression (Baseline)")
    print("----------------------------------------------------------------------")
    m1 = TFIDFBaseline(classifier_type="logistic_regression")
    m1.fit(txt_tr, y_tr)
    probs_m1 = m1.predict_proba(txt_te)
    res_m1 = evaluate_multilabel_model("TF-IDF + Logistic Regression", y_te, probs_m1)
    benchmark_results.append(res_m1)
    print(f"  -> F1 (Macro): {res_m1['f1_macro']:.4f} | ROC-AUC (Macro): {res_m1['roc_auc_macro']:.4f}")

    # ------------------------------------------------------------------------
    # Model 2: Baseline TF-IDF + Linear SVM
    # ------------------------------------------------------------------------
    print("\n----------------------------------------------------------------------")
    print("Model 2/6: TF-IDF + Linear SVM (Baseline)")
    print("----------------------------------------------------------------------")
    m2 = TFIDFBaseline(classifier_type="linear_svm")
    m2.fit(txt_tr, y_tr)
    probs_m2 = m2.predict_proba(txt_te)
    res_m2 = evaluate_multilabel_model("TF-IDF + Linear SVM", y_te, probs_m2)
    benchmark_results.append(res_m2)
    print(f"  -> F1 (Macro): {res_m2['f1_macro']:.4f} | ROC-AUC (Macro): {res_m2['roc_auc_macro']:.4f}")

    # Prepare Dense representation for ANN (TF-IDF vectorizer features)
    X_tr_tfidf = m1.vectorizer.transform(txt_tr).toarray().astype(np.float32)
    X_val_tfidf = m1.vectorizer.transform(txt_val).toarray().astype(np.float32)
    X_te_tfidf = m1.vectorizer.transform(txt_te).toarray().astype(np.float32)

    # ------------------------------------------------------------------------
    # Model 3: Simple ANN (Dense + Dropout)
    # ------------------------------------------------------------------------
    print("\n----------------------------------------------------------------------")
    print("Model 3/6: Simple ANN (Dense Layers + Dropout)")
    print("----------------------------------------------------------------------")
    m3 = DenseANN(input_dim=X_tr_tfidf.shape[1], hidden_dims=(128, 64), dropout_rates=(0.3, 0.2))
    train_neural_model(
        m3,
        X_tr_tfidf,
        y_tr,
        X_val_tfidf,
        y_val,
        epochs=10,
        batch_size=64,
        learning_rate=0.003,
        patience=3,
        pos_weights=pos_weights,
    )
    probs_m3 = m3.predict_proba(X_te_tfidf)
    res_m3 = evaluate_multilabel_model("Simple ANN (Dense)", y_te, probs_m3)
    benchmark_results.append(res_m3)
    histories["Simple ANN"] = m3.history
    print(f"  -> F1 (Macro): {res_m3['f1_macro']:.4f} | ROC-AUC (Macro): {res_m3['roc_auc_macro']:.4f}")

    # ------------------------------------------------------------------------
    # Model 4: 1D CNN Text Classifier
    # ------------------------------------------------------------------------
    print("\n----------------------------------------------------------------------", flush=True)
    print("Model 4/6: 1D CNN Text Classifier (Conv1D + Global MaxPooling)", flush=True)
    print("----------------------------------------------------------------------", flush=True)
    m4 = TextCNN1D(vocab_size=10000, emb_dim=48, num_filters=48, kernel_size=3)
    train_neural_model(
        m4,
        X_tr_seq,
        y_tr,
        X_val_seq,
        y_val,
        epochs=6,
        batch_size=128,
        learning_rate=0.005,
        patience=3,
        pos_weights=pos_weights,
    )
    probs_m4 = m4.predict_proba(X_te_seq)
    res_m4 = evaluate_multilabel_model("1D CNN Text Classifier", y_te, probs_m4)
    benchmark_results.append(res_m4)
    histories["1D CNN"] = m4.history
    print(f"  -> F1 (Macro): {res_m4['f1_macro']:.4f} | ROC-AUC (Macro): {res_m4['roc_auc_macro']:.4f}", flush=True)

    # ------------------------------------------------------------------------
    # Model 5: LSTM with Embedding Layer
    # ------------------------------------------------------------------------
    print("\n----------------------------------------------------------------------", flush=True)
    print("Model 5/6: Recurrent LSTM Classifier", flush=True)
    print("----------------------------------------------------------------------", flush=True)
    m5 = TextLSTM(vocab_size=10000, emb_dim=48, hidden_dim=48)
    train_neural_model(
        m5,
        X_tr_seq,
        y_tr,
        X_val_seq,
        y_val,
        epochs=6,
        batch_size=128,
        learning_rate=0.005,
        patience=3,
        pos_weights=pos_weights,
    )
    probs_m5 = m5.predict_proba(X_te_seq)
    res_m5 = evaluate_multilabel_model("LSTM Classifier", y_te, probs_m5)
    benchmark_results.append(res_m5)
    histories["LSTM"] = m5.history
    print(f"  -> F1 (Macro): {res_m5['f1_macro']:.4f} | ROC-AUC (Macro): {res_m5['roc_auc_macro']:.4f}", flush=True)

    # ------------------------------------------------------------------------
    # Model 6: BiLSTM with Embeddings
    # ------------------------------------------------------------------------
    print("\n----------------------------------------------------------------------", flush=True)
    print("Model 6/6 (Part A): Bidirectional LSTM (BiLSTM)", flush=True)
    print("----------------------------------------------------------------------", flush=True)
    m6 = TextBiLSTM(vocab_size=10000, emb_dim=48, hidden_dim=36)
    train_neural_model(
        m6,
        X_tr_seq,
        y_tr,
        X_val_seq,
        y_val,
        epochs=6,
        batch_size=128,
        learning_rate=0.005,
        patience=3,
        pos_weights=pos_weights,
    )
    probs_m6 = m6.predict_proba(X_te_seq)
    res_m6 = evaluate_multilabel_model("Bidirectional LSTM", y_te, probs_m6)
    benchmark_results.append(res_m6)
    histories["BiLSTM"] = m6.history
    print(f"  -> F1 (Macro): {res_m6['f1_macro']:.4f} | ROC-AUC (Macro): {res_m6['roc_auc_macro']:.4f}", flush=True)

    # ------------------------------------------------------------------------
    # Model 7: Hybrid CNN + BiLSTM (Final Production Model)
    # ------------------------------------------------------------------------
    print("\n----------------------------------------------------------------------", flush=True)
    print("Model 7/6 (Part B): Hybrid CNN + BiLSTM (Final Production Model)", flush=True)
    print("----------------------------------------------------------------------", flush=True)
    m7 = HybridCNNBiLSTM(vocab_size=10000, emb_dim=48, num_filters=48, kernel_size=3, lstm_units=36)
    train_neural_model(
        m7,
        X_tr_seq,
        y_tr,
        X_val_seq,
        y_val,
        epochs=8,
        batch_size=128,
        learning_rate=0.005,
        patience=3,
        pos_weights=pos_weights,
    )
    probs_m7 = m7.predict_proba(X_te_seq)
    res_m7 = evaluate_multilabel_model("Hybrid CNN + BiLSTM (Production)", y_te, probs_m7)
    benchmark_results.append(res_m7)
    histories["Hybrid CNN+BiLSTM"] = m7.history
    print(f"  -> F1 (Macro): {res_m7['f1_macro']:.4f} | ROC-AUC (Macro): {res_m7['roc_auc_macro']:.4f}", flush=True)

    # Save Best Model (.keras and .pkl)
    best_model_path_keras = os.path.join(MODELS_DIR, "best_model.keras")
    best_model_path_pkl = os.path.join(MODELS_DIR, "best_model.pkl")
    m7.save_keras_compatible(best_model_path_keras)
    m7.save(best_model_path_pkl)
    print(f"\n[Model Artifacts] Best model saved to:")
    print(f"  - {best_model_path_keras}")
    print(f"  - {best_model_path_pkl}")

    # Save Metrics JSON
    metrics_path = os.path.join(MODELS_DIR, "metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(
            {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "labels": LABELS,
                "benchmark_results": benchmark_results,
                "best_model": res_m7,
            },
            f,
            indent=2,
        )
    print(f"[Model Artifacts] Benchmark metrics saved to: {metrics_path}")

    # Render Charts and Confusion Matrices
    plot_comparison_and_curves(benchmark_results, histories, y_te, probs_m7)

    # Display final table
    df_summary = pd.DataFrame(benchmark_results)[
        ["model_name", "f1_macro", "roc_auc_macro", "precision_macro", "recall_macro", "subset_accuracy"]
    ]
    print("\n==========================================================================")
    print("FINAL BENCHMARK COMPARISON TABLE")
    print("==========================================================================")
    print(df_summary.to_string(index=False))
    print("==========================================================================")


if __name__ == "__main__":
    main()
