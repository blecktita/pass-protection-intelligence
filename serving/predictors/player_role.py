"""D — player_role predictor: HGBT classifier over 11 self-movement features."""
import numpy as np

from serving.registry import player_role_label_encoder, player_role_model
from serving.schemas import PlayerRoleRequest, PlayerRoleResponse

FEATURE_COLS = [
    "speed_mean", "speed_max", "speed_std",
    "accel_mean", "accel_max",
    "distance_covered", "displacement",
    "orientation_std", "dir_std", "o_dir_delta_mean",
    "window_duration_s",
]


def predict(request: PlayerRoleRequest) -> PlayerRoleResponse:
    X = np.array([[getattr(request, col) for col in FEATURE_COLS]])
    proba = player_role_model.predict_proba(X)[0]
    class_names = player_role_label_encoder.classes_
    predicted_idx = int(np.argmax(proba))

    return PlayerRoleResponse(
        predicted_role=class_names[predicted_idx],
        probabilities={cls: float(p) for cls, p in zip(class_names, proba)},
    )
