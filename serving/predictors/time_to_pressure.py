"""E — time_to_pressure predictor: Cox Proportional Hazards model.

Reproduces, at inference time, the same covariate construction the notebook uses when
fitting: numeric cox_features as-is, plus a one-hot dummy for a collapsed block-type
category (top 5 types + OTHER, one — CL — dropped as the implicit baseline). Rather
than hardcoding which dummy columns exist, this reindexes to `cph.params_.index` — the
exact covariate set and order the fitted model expects — so an unseen/baseline block
type naturally encodes to all-zero dummies instead of needing special-casing.
"""
import math

import pandas as pd

from serving.registry import cox_model
from serving.schemas import TimeToPressureRequest, TimeToPressureResponse

COX_FEATURES = [
    "separation_at_snap",
    "separation_min",
    "closing_velocity",
    "blocker_speed_mean",
    "blocker_accel_mean",
    "rusher_speed_mean",
    "rusher_speed_max",
    "rusher_accel_mean",
    "pff_backFieldBlock",
]
TOP_BLOCK_TYPES = ["PP", "PA", "PT", "SW", "CL"]


def predict(request: TimeToPressureRequest) -> TimeToPressureResponse:
    row = {col: getattr(request, col) for col in COX_FEATURES}
    block_type_simple = request.pff_blockType if request.pff_blockType in TOP_BLOCK_TYPES else "OTHER"
    row[f"bt_{block_type_simple}"] = 1

    df = pd.DataFrame([row]).reindex(columns=cox_model.params_.index, fill_value=0)

    partial_hazard = float(cox_model.predict_partial_hazard(df).iloc[0])

    predicted_median: float | None
    try:
        median = float(cox_model.predict_median(df).iloc[0])
        predicted_median = None if math.isnan(median) or math.isinf(median) else median
    except Exception:
        predicted_median = None

    risk_word = "elevated" if partial_hazard > 1.0 else "reduced"
    interpretation = (
        f"This block's predicted failure risk is {partial_hazard:.2f}x the average "
        f"block in the training data ({risk_word} risk)."
    )

    return TimeToPressureResponse(
        partial_hazard=partial_hazard,
        predicted_median_survival_s=predicted_median,
        interpretation=interpretation,
    )
