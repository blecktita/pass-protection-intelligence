"""Loads all trained artifacts once at import time and exposes them as module-level
singletons.
"""
import json
from pathlib import Path

import joblib

ROOT = Path(__file__).resolve().parent.parent
ARTIFACTS = ROOT / "artifacts"


def _load_metrics(use_case: str) -> dict:
    with open(ARTIFACTS / use_case / "metrics_report.json") as f:
        return json.load(f)


# player_role
_PLAYER_ROLE_DIR = ARTIFACTS / "player_role"
player_role_model = joblib.load(_PLAYER_ROLE_DIR / "model.joblib")
player_role_label_encoder = joblib.load(_PLAYER_ROLE_DIR / "label_encoder.joblib")
player_role_metrics = _load_metrics("player_role")

# pressure_allowed
_PRESSURE_ALLOWED_DIR = ARTIFACTS / "pressure_allowed"
pressure_allowed_model = joblib.load(_PRESSURE_ALLOWED_DIR / "model.joblib")
pressure_allowed_encoders = joblib.load(_PRESSURE_ALLOWED_DIR / "encoders.joblib")
pressure_allowed_metrics = _load_metrics("pressure_allowed")

# pressure_generated
_PRESSURE_GENERATED_DIR = ARTIFACTS / "pressure_generated"
pressure_generated_model = joblib.load(_PRESSURE_GENERATED_DIR / "model.joblib")
pressure_generated_position_encoder = joblib.load(_PRESSURE_GENERATED_DIR / "position_encoder.joblib")
pressure_generated_metrics = _load_metrics("pressure_generated")

# block_type
_BLOCK_TYPE_DIR = ARTIFACTS / "block_type"
block_type_model = joblib.load(_BLOCK_TYPE_DIR / "model.joblib")
block_type_label_encoder = joblib.load(_BLOCK_TYPE_DIR / "label_encoder.joblib")
block_type_metrics = _load_metrics("block_type")

# time_to_pressure
_TIME_TO_PRESSURE_DIR = ARTIFACTS / "time_to_pressure"
cox_model = joblib.load(_TIME_TO_PRESSURE_DIR / "cox_model.joblib")
km_overall = joblib.load(_TIME_TO_PRESSURE_DIR / "km_overall.joblib")
time_to_pressure_metrics = _load_metrics("time_to_pressure")
