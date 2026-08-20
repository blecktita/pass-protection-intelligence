"""
Pydantic request/response models, one pair per use case. 
Field names match the FEATURE_COLS / cox_features used when each model was trained (see the corresponding
notebook's "Prepare Model Input" step) — the API accepts exactly what the model saw.
"""
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# D — player_role
# ---------------------------------------------------------------------------
class PlayerRoleRequest(BaseModel):
    speed_mean: float
    speed_max: float
    speed_std: float
    accel_mean: float
    accel_max: float
    distance_covered: float
    displacement: float
    orientation_std: float
    dir_std: float
    o_dir_delta_mean: float
    window_duration_s: float


class PlayerRoleResponse(BaseModel):
    predicted_role: str
    probabilities: dict[str, float]


# ---------------------------------------------------------------------------
# A — pressure_allowed
# ---------------------------------------------------------------------------
class PressureAllowedRequest(BaseModel):
    pff_backFieldBlock: float
    separation_at_snap: float
    separation_min: float
    closing_velocity: float
    blocker_speed_mean: float
    blocker_speed_max: float
    blocker_accel_mean: float
    rusher_speed_mean: float
    rusher_speed_max: float
    rusher_accel_mean: float
    window_duration_s: float
    pff_positionLinedUp: str
    pff_blockType: str


class PressureAllowedResponse(BaseModel):
    pressure_allowed: bool
    probability: float = Field(description="Raw predicted probability of pressure being allowed")
    threshold_used: float = Field(description="Decision threshold tuned on the held-out test set")


# ---------------------------------------------------------------------------
# B — pressure_generated
# ---------------------------------------------------------------------------
class PressureGeneratedRequest(BaseModel):
    rusher_speed_mean: float
    rusher_speed_max: float
    rusher_accel_mean: float
    rusher_accel_max: float
    rusher_orient_std: float
    rusher_displacement: float
    nearest_dist_min: float
    nearest_dist_mean: float
    nearest_closing_vel: float
    window_duration_s: float
    pff_positionLinedUp: str


class PressureGeneratedResponse(BaseModel):
    pressure_generated: bool
    probability: float = Field(description="Raw predicted probability of the rusher generating pressure")
    threshold_used: float = Field(description="Decision threshold tuned on the held-out test set")


# ---------------------------------------------------------------------------
# C — block_type
# ---------------------------------------------------------------------------
class BlockTypeRequest(BaseModel):
    speed_mean: float
    speed_max: float
    speed_std: float
    accel_mean: float
    accel_max: float
    distance_covered: float
    forward_disp: float
    lateral_disp: float
    net_displacement: float
    orientation_std: float
    dir_std: float
    pff_backFieldBlock: float
    window_duration_s: float


class BlockTypeResponse(BaseModel):
    predicted_block_type: str
    probabilities: dict[str, float]


# ---------------------------------------------------------------------------
# E — time_to_pressure
# ---------------------------------------------------------------------------
class TimeToPressureRequest(BaseModel):
    separation_at_snap: float
    separation_min: float
    closing_velocity: float
    blocker_speed_mean: float
    blocker_accel_mean: float
    rusher_speed_mean: float
    rusher_speed_max: float
    rusher_accel_mean: float
    pff_backFieldBlock: float
    pff_blockType: str


class TimeToPressureResponse(BaseModel):
    partial_hazard: float = Field(description="Relative risk score — higher means faster predicted failure")
    predicted_median_survival_s: float | None = Field(
        description="Model's predicted median survival time in seconds, if estimable for this input"
    )
    interpretation: str


# ---------------------------------------------------------------------------
# Shared
# ---------------------------------------------------------------------------
class HealthResponse(BaseModel):
    status: str
    models_loaded: list[str]


class ValidationErrorDetail(BaseModel):
    field: str
    message: str
    valid_values: list[str] | None = None
