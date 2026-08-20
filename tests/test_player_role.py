def test_predict_player_role(client, player_role_payload):
    response = client.post("/predict/player-role", json=player_role_payload)
    assert response.status_code == 200
    body = response.json()
    assert body["predicted_role"] in body["probabilities"]
    assert abs(sum(body["probabilities"].values()) - 1.0) < 1e-4


def test_predict_player_role_missing_field(client, player_role_payload):
    del player_role_payload["speed_mean"]
    response = client.post("/predict/player-role", json=player_role_payload)
    assert response.status_code == 422
