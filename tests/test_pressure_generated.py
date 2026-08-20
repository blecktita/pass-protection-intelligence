def test_predict_pressure_generated(client, pressure_generated_payload):
    response = client.post("/predict/pressure-generated", json=pressure_generated_payload)
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body["pressure_generated"], bool)
    assert 0.0 <= body["probability"] <= 1.0


def test_predict_pressure_generated_unseen_position(client, pressure_generated_payload):
    pressure_generated_payload["pff_positionLinedUp"] = "NOT_A_REAL_POSITION"
    response = client.post("/predict/pressure-generated", json=pressure_generated_payload)
    assert response.status_code == 422
    detail = response.json()["detail"]
    assert detail["field"] == "pff_positionLinedUp"
    assert "valid_values" in detail
