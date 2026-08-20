"""shared helpers for the predictor modules."""
from fastapi import HTTPException
from sklearn.preprocessing import LabelEncoder


def safe_label_transform(encoder: LabelEncoder, value: str, field_name: str) -> int:
    """LabelEncoder.transform raises ValueError on an unseen category — turn that into
    a clean 422 with the valid values listed, instead of a raw 500.
    """
    try:
        return int(encoder.transform([value])[0])
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail={
                "field": field_name,
                "message": f"Unrecognized value {value!r} for {field_name!r}.",
                "valid_values": sorted(encoder.classes_.tolist()),
            },
        )
