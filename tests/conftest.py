"""Shared fixtures: a TestClient over the FastAPI app, and one realistic valid payload
per use case (values chosen from the feature ranges seen in each notebook's EDA/
describe() output — see docs/UseCases.md).
"""
import pytest
from fastapi.testclient import TestClient

from serving.main import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def player_role_payload() -> dict:
    return {
        "speed_mean": 2.6, "speed_max": 4.5, "speed_std": 1.4,
        "accel_mean": 1.9, "accel_max": 3.7,
        "distance_covered": 8.9, "displacement": 7.6,
        "orientation_std": 42.5, "dir_std": 45.9,
        "o_dir_delta_mean": 77.9, "window_duration_s": 3.2,
    }


@pytest.fixture
def pressure_allowed_payload() -> dict:
    return {
        "pff_backFieldBlock": 0.0,
        "separation_at_snap": 1.5, "separation_min": 0.83, "closing_velocity": 0.42,
        "blocker_speed_mean": 1.8, "blocker_speed_max": 3.2, "blocker_accel_mean": 1.4,
        "rusher_speed_mean": 2.9, "rusher_speed_max": 3.9, "rusher_accel_mean": 2.0,
        "window_duration_s": 3.2,
        "pff_positionLinedUp": "LT",
        "pff_blockType": "PP",
    }


@pytest.fixture
def pressure_generated_payload() -> dict:
    return {
        "rusher_speed_mean": 2.9, "rusher_speed_max": 4.5,
        "rusher_accel_mean": 2.0, "rusher_accel_max": 3.8,
        "rusher_orient_std": 40.0, "rusher_displacement": 7.5,
        "nearest_dist_min": 1.0, "nearest_dist_mean": 2.0, "nearest_closing_vel": 0.3,
        "window_duration_s": 3.2,
        "pff_positionLinedUp": "LE",
    }


@pytest.fixture
def block_type_payload() -> dict:
    return {
        "speed_mean": 1.8, "speed_max": 2.9, "speed_std": 0.8,
        "accel_mean": 1.3, "accel_max": 2.6,
        "distance_covered": 6.0, "forward_disp": 0.1, "lateral_disp": 0.0,
        "net_displacement": 4.9, "orientation_std": 46.0, "dir_std": 46.6,
        "pff_backFieldBlock": 0.0, "window_duration_s": 3.3,
    }


@pytest.fixture
def time_to_pressure_payload() -> dict:
    return {
        "separation_at_snap": 1.5, "separation_min": 0.83, "closing_velocity": 0.42,
        "blocker_speed_mean": 1.8, "blocker_accel_mean": 1.4,
        "rusher_speed_mean": 2.9, "rusher_speed_max": 3.9, "rusher_accel_mean": 2.0,
        "pff_backFieldBlock": 0.0,
        "pff_blockType": "PP",
    }
