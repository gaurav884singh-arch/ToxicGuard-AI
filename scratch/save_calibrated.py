import os
import sys
import numpy as np

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.models.baseline import TFIDFBaseline
from src.nlp.dataset_generator import load_or_create_dataset, LABELS

df, _ = load_or_create_dataset("data")
baseline = TFIDFBaseline("logistic_regression")
baseline.fit(df["comment_text"].tolist(), df[LABELS].values)
save_path = os.path.join(PROJECT_ROOT, "models", "calibrated_baseline.pkl")
baseline.save(save_path)
print(f"Saved calibrated baseline to: {save_path}")
