def test_predict_pressure_allowed(client, pressure_allowed_payload):
    response = client.post("/predict/pressure-allowed", json=pressure_allowed_payload)
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body["pressure_allowed"], bool)
    assert 0.0 <= body["probability"] <= 1.0
    assert (body["probability"] >= body["threshold_used"]) == body["pressure_allowed"]


def test_predict_pressure_allowed_unseen_position(client, pressure_allowed_payload):
    pressure_allowed_payload["pff_positionLinedUp"] = "NOT_A_REAL_POSITION"
    response = client.post("/predict/pressure-allowed", json=pressure_allowed_payload)
    assert response.status_code == 422
    detail = response.json()["detail"]
    assert detail["field"] == "pff_positionLinedUp"
    assert "valid_values" in detail
