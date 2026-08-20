def test_predict_time_to_pressure(client, time_to_pressure_payload):
    response = client.post("/predict/time-to-pressure", json=time_to_pressure_payload)
    assert response.status_code == 200
    body = response.json()
    assert body["partial_hazard"] > 0
    assert isinstance(body["interpretation"], str) and body["interpretation"]


def test_predict_time_to_pressure_baseline_block_type(client, time_to_pressure_payload):
    # "CL" is the implicit reference category (dropped by drop_first at training time) —
    # it must encode to all-zero dummies rather than error.
    time_to_pressure_payload["pff_blockType"] = "CL"
    response = client.post("/predict/time-to-pressure", json=time_to_pressure_payload)
    assert response.status_code == 200


def test_predict_time_to_pressure_unknown_block_type_falls_back_to_other(client, time_to_pressure_payload):
    # Unlike the classifiers' LabelEncoder-backed fields, block type here is grouped into
    # OTHER rather than rejected — any string is a valid input.
    time_to_pressure_payload["pff_blockType"] = "SOME_NEW_TECHNIQUE"
    response = client.post("/predict/time-to-pressure", json=time_to_pressure_payload)
    assert response.status_code == 200
