from fastapi.testclient import TestClient
from api.main import app

def test_action_economy():
    client = TestClient(app)
    resp = client.post('/ask', json={'question': 'What are ways to increase action economy?'})
    assert resp.status_code == 200
    data = resp.json()
    assert 'answer' in data
    assert len(data.get('citations', [])) >= 2
    assert 'Cram' in data['answer'] or 'Wired Reflexes' in data['answer']
