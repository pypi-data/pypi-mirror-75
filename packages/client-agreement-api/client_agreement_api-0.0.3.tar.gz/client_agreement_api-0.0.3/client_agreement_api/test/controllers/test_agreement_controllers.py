BASE_API_URL = "/api"
AGREEMENT_RESOURCE_PATH = BASE_API_URL + "/agreement"


def test_get_agreement_endpoint(client, agreement_object, db_session):
    response = client.get(AGREEMENT_RESOURCE_PATH, content_type='application/json')
    assert response.status_code == 200
    assert all(response.json[0].get(key) == agreement_object[key] for key in agreement_object.keys())
    assert len(response.json) == 1


def test_add_agreement_endpoint(client, agreement_object, db_session):
    user_id = agreement_object.get("user")
    expected = {'agreement_status': False, 'user_id': user_id}
    response = client.post(AGREEMENT_RESOURCE_PATH, json={
        'user_id': user_id, "agreement_status": False
    })
    assert response.status_code == 201
    assert all(response.json.get(key) == value for key, value in expected.items())
