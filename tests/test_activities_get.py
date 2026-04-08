def test_get_activities_returns_success(client):
    response = client.get("/activities")

    assert response.status_code == 200


def test_get_activities_returns_all_expected_activities(client):
    response = client.get("/activities")
    body = response.json()

    assert len(body) == 9
    assert "Chess Club" in body
    assert "Programming Class" in body


def test_get_activities_has_expected_activity_schema(client):
    response = client.get("/activities")
    body = response.json()

    chess = body["Chess Club"]

    assert set(chess.keys()) == {
        "description",
        "schedule",
        "max_participants",
        "participants",
    }
    assert isinstance(chess["description"], str)
    assert isinstance(chess["schedule"], str)
    assert isinstance(chess["max_participants"], int)
    assert isinstance(chess["participants"], list)
