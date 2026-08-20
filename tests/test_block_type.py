def test_predict_block_type(client, block_type_payload):
    response = client.post("/predict/block-type", json=block_type_payload)
    assert response.status_code == 200
    body = response.json()
    assert body["predicted_block_type"] in body["probabilities"]
    assert abs(sum(body["probabilities"].values()) - 1.0) < 1e-4
