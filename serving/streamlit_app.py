"""Demo dashboard over the 5 Pass Protection Intelligence models.

Calls the same predictor functions FastAPI uses (in-process, no HTTP hop) so there's
one source of truth for prediction logic between the API and this UI.

Run with: streamlit run serving/streamlit_app.py
"""
import sys
from pathlib import Path

# `streamlit run` puts this script's own directory on sys.path, not the project
# root — so the `serving.*` absolute imports below only resolve if we add the
# root ourselves, regardless of which directory this was launched from.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import streamlit as st

from serving.predictors import block_type, player_role, pressure_allowed, pressure_generated, time_to_pressure
from serving.registry import (
    block_type_label_encoder,
    km_overall,
    player_role_label_encoder,
    pressure_allowed_encoders,
    pressure_generated_position_encoder,
)
from serving.schemas import (
    BlockTypeRequest,
    PlayerRoleRequest,
    PressureAllowedRequest,
    PressureGeneratedRequest,
    TimeToPressureRequest,
)

st.set_page_config(page_title="Pass Protection Intelligence", layout="centered")
st.title("Pass Protection Intelligence")
st.caption("Live predictions from the 5 trained models. See README.md for methodology.")

USE_CASE = st.sidebar.selectbox(
    "Use case",
    [
        "D — player_role",
        "A — pressure_allowed",
        "B — pressure_generated",
        "C — block_type",
        "E — time_to_pressure",
    ],
)


def number_form(fields: list[str], defaults: dict[str, float] | None = None) -> dict[str, float]:
    defaults = defaults or {}
    values = {}
    for field in fields:
        values[field] = st.number_input(field, value=float(defaults.get(field, 0.0)))
    return values


if USE_CASE == "D — player_role":
    st.subheader("Will movement alone tell us what role this player was performing?")
    values = number_form(player_role.FEATURE_COLS, {
        "speed_mean": 2.6, "speed_max": 4.5, "speed_std": 1.4,
        "accel_mean": 1.9, "accel_max": 3.7, "distance_covered": 8.9,
        "displacement": 7.6, "orientation_std": 42.5, "dir_std": 45.9,
        "o_dir_delta_mean": 77.9, "window_duration_s": 3.2,
    })
    if st.button("Predict role"):
        result = player_role.predict(PlayerRoleRequest(**values))
        st.success(f"Predicted role: **{result.predicted_role}**")
        st.bar_chart(pd.Series(result.probabilities, name="probability"))
    st.caption(f"Classes: {', '.join(player_role_label_encoder.classes_)}")

elif USE_CASE == "A — pressure_allowed":
    st.subheader("Will this blocker get beaten on this assignment?")
    values = number_form(pressure_allowed.NUM_COLS, {
        "pff_backFieldBlock": 0.0, "separation_at_snap": 1.5, "separation_min": 0.8,
        "closing_velocity": 0.3, "blocker_speed_mean": 1.8, "blocker_speed_max": 3.2,
        "blocker_accel_mean": 1.4, "rusher_speed_mean": 2.9, "rusher_speed_max": 4.5,
        "rusher_accel_mean": 2.0, "window_duration_s": 3.2,
    })
    position = st.selectbox("pff_positionLinedUp", sorted(pressure_allowed_encoders["pff_positionLinedUp"].classes_))
    block_type_val = st.selectbox("pff_blockType", sorted(pressure_allowed_encoders["pff_blockType"].classes_))
    if st.button("Predict"):
        result = pressure_allowed.predict(PressureAllowedRequest(
            **values, pff_positionLinedUp=position, pff_blockType=block_type_val,
        ))
        label = "PRESSURE ALLOWED" if result.pressure_allowed else "Clean block"
        st.success(f"{label}  (probability={result.probability:.3f}, threshold={result.threshold_used:.3f})")

elif USE_CASE == "B — pressure_generated":
    st.subheader("Will this pass rusher win the matchup?")
    values = number_form(pressure_generated.NUM_COLS, {
        "rusher_speed_mean": 2.9, "rusher_speed_max": 4.5, "rusher_accel_mean": 2.0,
        "rusher_accel_max": 3.8, "rusher_orient_std": 40.0, "rusher_displacement": 7.5,
        "nearest_dist_min": 1.0, "nearest_dist_mean": 2.0, "nearest_closing_vel": 0.3,
        "window_duration_s": 3.2,
    })
    position = st.selectbox("pff_positionLinedUp", sorted(pressure_generated_position_encoder.classes_))
    if st.button("Predict"):
        result = pressure_generated.predict(PressureGeneratedRequest(**values, pff_positionLinedUp=position))
        label = "PRESSURE GENERATED" if result.pressure_generated else "No pressure"
        st.success(f"{label}  (probability={result.probability:.3f}, threshold={result.threshold_used:.3f})")

elif USE_CASE == "C — block_type":
    st.subheader("Can blocking technique be read from the blocker's movement alone?")
    values = number_form(block_type.FEATURE_COLS, {
        "speed_mean": 1.8, "speed_max": 2.9, "speed_std": 0.8,
        "accel_mean": 1.3, "accel_max": 2.6, "distance_covered": 6.0,
        "forward_disp": 0.1, "lateral_disp": 0.0, "net_displacement": 4.9,
        "orientation_std": 46.0, "dir_std": 46.6, "pff_backFieldBlock": 0.0,
        "window_duration_s": 3.3,
    })
    if st.button("Predict block type"):
        result = block_type.predict(BlockTypeRequest(**values))
        st.success(f"Predicted block type: **{result.predicted_block_type}**")
        st.bar_chart(pd.Series(result.probabilities, name="probability"))
    st.caption(f"Classes: {', '.join(block_type_label_encoder.classes_)}")

else:  # E — time_to_pressure
    st.subheader("How long does this block last before it breaks?")
    values = number_form(time_to_pressure.COX_FEATURES, {
        "separation_at_snap": 1.5, "separation_min": 0.8, "closing_velocity": 0.3,
        "blocker_speed_mean": 1.8, "blocker_accel_mean": 1.4,
        "rusher_speed_mean": 2.9, "rusher_speed_max": 4.5, "rusher_accel_mean": 2.0,
        "pff_backFieldBlock": 0.0,
    })
    block_type_val = st.selectbox("pff_blockType", time_to_pressure.TOP_BLOCK_TYPES + ["OTHER"])
    if st.button("Predict survival"):
        result = time_to_pressure.predict(TimeToPressureRequest(**values, pff_blockType=block_type_val))
        st.success(result.interpretation)
        st.metric("Partial hazard", f"{result.partial_hazard:.2f}x")
        if result.predicted_median_survival_s is not None:
            st.metric("Predicted median survival", f"{result.predicted_median_survival_s:.2f}s")
        else:
            st.info("Median survival time isn't reachable for this input (predicted risk too low).")

    st.markdown("**Overall Kaplan-Meier survival curve** (population baseline, for context)")
    km_df = km_overall.survival_function_
    st.line_chart(km_df)
