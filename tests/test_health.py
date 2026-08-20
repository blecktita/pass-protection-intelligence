def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert set(body["models_loaded"]) == {
        "player_role", "pressure_allowed", "pressure_generated",
        "block_type", "time_to_pressure",
    }
