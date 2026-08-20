"""FastAPI service over the five trained Pass Protection Intelligence models.

Each endpoint accepts exactly the feature set its notebook trained on and returns
the same decision logic (including the tuned threshold, where applicable) — see
docs/UseCases.md and README.md §7 for what each model actually predicts and why.
"""
from fastapi import FastAPI

from serving.predictors import (
    block_type,
    player_role,
    pressure_allowed,
    pressure_generated,
    time_to_pressure,
)
from serving.schemas import (
    BlockTypeRequest,
    BlockTypeResponse,
    HealthResponse,
    PlayerRoleRequest,
    PlayerRoleResponse,
    PressureAllowedRequest,
    PressureAllowedResponse,
    PressureGeneratedRequest,
    PressureGeneratedResponse,
    TimeToPressureRequest,
    TimeToPressureResponse,
)

app = FastAPI(
    title="Pass Protection Intelligence API",
    description="Serves the 5 models documented in README.md — player_role, "
                 "pressure_allowed, pressure_generated, block_type, time_to_pressure.",
    version="1.0.0",
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        models_loaded=[
            "player_role", "pressure_allowed", "pressure_generated",
            "block_type", "time_to_pressure",
        ],
    )


@app.post("/predict/player-role", response_model=PlayerRoleResponse)
def predict_player_role(request: PlayerRoleRequest) -> PlayerRoleResponse:
    return player_role.predict(request)


@app.post("/predict/pressure-allowed", response_model=PressureAllowedResponse)
def predict_pressure_allowed(request: PressureAllowedRequest) -> PressureAllowedResponse:
    return pressure_allowed.predict(request)


@app.post("/predict/pressure-generated", response_model=PressureGeneratedResponse)
def predict_pressure_generated(request: PressureGeneratedRequest) -> PressureGeneratedResponse:
    return pressure_generated.predict(request)


@app.post("/predict/block-type", response_model=BlockTypeResponse)
def predict_block_type(request: BlockTypeRequest) -> BlockTypeResponse:
    return block_type.predict(request)


@app.post("/predict/time-to-pressure", response_model=TimeToPressureResponse)
def predict_time_to_pressure(request: TimeToPressureRequest) -> TimeToPressureResponse:
    return time_to_pressure.predict(request)
