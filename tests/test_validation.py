"""Cross-cutting validation behavior: malformed payloads and unseen categoricals should
return clean 422s, never a raw 500.
"""


def test_malformed_json_body(client):
    response = client.post("/predict/player-role", content="not json", headers={"Content-Type": "application/json"})
    assert response.status_code == 422


def test_wrong_type_field(client, block_type_payload):
    block_type_payload["speed_mean"] = "not a number"
    response = client.post("/predict/block-type", json=block_type_payload)
    assert response.status_code == 422


def test_unseen_block_type_on_pressure_allowed(client, pressure_allowed_payload):
    pressure_allowed_payload["pff_blockType"] = "NOT_A_REAL_TECHNIQUE"
    response = client.post("/predict/pressure-allowed", json=pressure_allowed_payload)
    assert response.status_code == 422
    detail = response.json()["detail"]
    assert detail["field"] == "pff_blockType"
    assert "NOT_A_REAL_TECHNIQUE" in detail["message"]
    assert isinstance(detail["valid_values"], list) and len(detail["valid_values"]) > 0
