from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)

def test_chat_basic():
    payload = {
        "message": "Looking for a 4 bedroom with pool in Dubai Festival City",
        "session_id": "u1",
        "context": {"lead_status":"new"}
    }
    r = client.post("/chat", json=payload)
    assert r.status_code == 200
    j = r.json()
    assert "citations" in j and j["citations"]
    assert any(img["path"].endswith(".webp") for img in j["images"])
    assert j["lead_signals"]["intent"] in ["low","medium","high"]
