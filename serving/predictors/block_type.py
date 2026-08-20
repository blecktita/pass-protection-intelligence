"""C — block_type predictor: HGBT multiclass classifier over blocker-only movement
features (no rusher data — see docs/UseCases.md for why).
"""
import numpy as np

from serving.registry import block_type_label_encoder, block_type_model
from serving.schemas import BlockTypeRequest, BlockTypeResponse

FEATURE_COLS = [
    "speed_mean", "speed_max", "speed_std",
    "accel_mean", "accel_max",
    "distance_covered", "forward_disp", "lateral_disp", "net_displacement",
    "orientation_std", "dir_std",
    "pff_backFieldBlock",
    "window_duration_s",
]


def predict(request: BlockTypeRequest) -> BlockTypeResponse:
    X = np.array([[getattr(request, col) for col in FEATURE_COLS]])
    proba = block_type_model.predict_proba(X)[0]
    class_names = block_type_label_encoder.classes_
    predicted_idx = int(np.argmax(proba))

    return BlockTypeResponse(
        predicted_block_type=class_names[predicted_idx],
        probabilities={cls: float(p) for cls, p in zip(class_names, proba)},
    )
