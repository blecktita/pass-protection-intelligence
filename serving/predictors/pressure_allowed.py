"""A — pressure_allowed predictor: HGBT binary classifier over blocker/rusher matchup
features. Decision uses the threshold tuned on the held-out test set in the notebook
(saved in metrics_report.json), not a default 0.5 — this dataset is ~6.6% positive.
"""
import numpy as np

from serving.registry import (
    pressure_allowed_encoders,
    pressure_allowed_metrics,
    pressure_allowed_model,
)
from serving.schemas import PressureAllowedRequest, PressureAllowedResponse
from serving.utils import safe_label_transform

NUM_COLS = [
    "pff_backFieldBlock",
    "separation_at_snap",
    "separation_min",
    "closing_velocity",
    "blocker_speed_mean", "blocker_speed_max", "blocker_accel_mean",
    "rusher_speed_mean", "rusher_speed_max", "rusher_accel_mean",
    "window_duration_s",
]
CAT_COLS = ["pff_positionLinedUp", "pff_blockType"]

THRESHOLD = pressure_allowed_metrics["best_threshold"]


def predict(request: PressureAllowedRequest) -> PressureAllowedResponse:
    row = [getattr(request, col) for col in NUM_COLS]
    for col in CAT_COLS:
        encoder = pressure_allowed_encoders[col]
        row.append(safe_label_transform(encoder, getattr(request, col), col))

    X = np.array([row])
    probability = float(pressure_allowed_model.predict_proba(X)[0, 1])

    return PressureAllowedResponse(
        pressure_allowed=probability >= THRESHOLD,
        probability=probability,
        threshold_used=THRESHOLD,
    )
