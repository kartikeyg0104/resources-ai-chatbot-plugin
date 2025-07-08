"""Integration Tests for the chatbot."""

def test_create_session(client):
    response = client.post("/sessions")
    assert response.status_code == 201
    data = response.json()
    assert "session_id" in data
    assert isinstance(data["session_id"], str)
    assert response.headers["Location"] == f"/sessions/{data['session_id']}/message"


def test_reply_to_nonexistent_session(client):
    payload = {"message": "Hello"}
    response = client.post("/sessions/nonexistent-session/message", json=payload)

    assert response.status_code == 404
    assert response.json() == {"detail": "Session not found."}


def test_delete_existing_session(client):
    create_resp = client.post("/sessions")
    session_id = create_resp.json()["session_id"]

    response = client.delete(f"/sessions/{session_id}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Session {session_id} deleted."}


def test_delete_nonexistent_session(client):
    response = client.delete("/sessions/invalid-session")
    assert response.status_code == 404
    assert response.json() == {"detail": "Session not found."}


def test_reply_after_session_deleted(client):
    create_resp = client.post("/sessions")
    session_id = create_resp.json()["session_id"]

    client.delete(f"/sessions/{session_id}")

    payload = {"message": "Is anyone there?"}
    response = client.post(f"/sessions/{session_id}/message", json=payload)

    assert response.status_code == 404
    assert response.json() == {"detail": "Session not found."}


def test_reply_with_empty_message(client):
    create_resp = client.post("/sessions")
    session_id = create_resp.json()["session_id"]

    payload = {"message": "   "}
    response = client.post(f"/sessions/{session_id}/message", json=payload)

    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any("Message cannot be empty." in e["msg"] for e in errors)
