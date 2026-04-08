def test_signup_adds_participant_successfully(client):
    email = "new.student@mergington.edu"

    response = client.post("/activities/Chess%20Club/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}

    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]


def test_signup_returns_404_for_unknown_activity(client):
    response = client.post(
        "/activities/Unknown%20Activity/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_returns_400_for_duplicate_student(client):
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_increases_participant_count(client):
    before = client.get("/activities").json()["Basketball Team"]["participants"]
    before_count = len(before)

    client.post(
        "/activities/Basketball%20Team/signup",
        params={"email": "sam@mergington.edu"},
    )

    after = client.get("/activities").json()["Basketball Team"]["participants"]
    after_count = len(after)

    assert after_count == before_count + 1
