def test_unregister_removes_participant_successfully(client):
    email = "alex@mergington.edu"

    response = client.delete(
        "/activities/Basketball%20Team/participants",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from Basketball Team"}

    activities = client.get("/activities").json()
    assert email not in activities["Basketball Team"]["participants"]


def test_unregister_returns_404_for_unknown_activity(client):
    response = client.delete(
        "/activities/Unknown%20Activity/participants",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_for_unknown_participant(client):
    response = client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": "absent@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_unregister_decreases_participant_count(client):
    before = client.get("/activities").json()["Chess Club"]["participants"]
    before_count = len(before)

    client.delete(
        "/activities/Chess%20Club/participants",
        params={"email": "daniel@mergington.edu"},
    )

    after = client.get("/activities").json()["Chess Club"]["participants"]
    after_count = len(after)

    assert after_count == before_count - 1
