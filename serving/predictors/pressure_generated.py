"""B — pressure_generated predictor: HGBT binary classifier over the rusher and their
nearest blocker. Decision uses the threshold tuned on the held-out test set (saved in
metrics_report.json), not a default 0.5.
"""
import numpy as np

from serving.registry import (
    pressure_generated_metrics,
    pressure_generated_model,
    pressure_generated_position_encoder,
)
from serving.schemas import PressureGeneratedRequest, PressureGeneratedResponse
from serving.utils import safe_label_transform

NUM_COLS = [
    "rusher_speed_mean", "rusher_speed_max",
    "rusher_accel_mean", "rusher_accel_max",
    "rusher_orient_std", "rusher_displacement",
    "nearest_dist_min", "nearest_dist_mean",
    "nearest_closing_vel",
    "window_duration_s",
]

THRESHOLD = pressure_generated_metrics["best_threshold"]


def predict(request: PressureGeneratedRequest) -> PressureGeneratedResponse:
    row = [getattr(request, col) for col in NUM_COLS]
    row.append(safe_label_transform(
        pressure_generated_position_encoder, request.pff_positionLinedUp, "pff_positionLinedUp"
    ))

    X = np.array([row])
    probability = float(pressure_generated_model.predict_proba(X)[0, 1])

    return PressureGeneratedResponse(
        pressure_generated=probability >= THRESHOLD,
        probability=probability,
        threshold_used=THRESHOLD,
    )
