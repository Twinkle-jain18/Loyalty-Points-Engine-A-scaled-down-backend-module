import json

def test_event_ingestion(client):
    payload = {
        "event_id": "evt_001",
        "user_id": "user_001",
        "event_type": "deposit",
        "amount": 1000,
        "timestamp": "2026-06-20T10:00:00Z" # 2026-06-20 is a Saturday
    }
    response = client.post('/events', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['points_awarded'] == 20  # Base 10 * 2 (weekend multiplier)
    
def test_event_idempotency(client):
    payload = {
        "event_id": "evt_002",
        "user_id": "user_001",
        "event_type": "purchase",
        "amount": 100,
        "timestamp": "2026-06-22T10:00:00Z" # Monday -> base points 5
    }
    response1 = client.post('/events', json=payload)
    assert response1.status_code == 201
    assert response1.get_json()['points_awarded'] == 5
    
    response2 = client.post('/events', json=payload)
    assert response2.status_code == 200
    assert response2.get_json()['message'] == "Event already processed"
    assert response2.get_json()['points_awarded'] == 5

def test_balance_calculation(client):
    # Deposit (Saturday = 20)
    client.post('/events', json={
        "event_id": "evt_101",
        "user_id": "user_100",
        "event_type": "deposit",
        "amount": 100,
        "timestamp": "2026-06-20T10:00:00Z"
    })
    # Referral (Monday = 50)
    client.post('/events', json={
        "event_id": "evt_102",
        "user_id": "user_100",
        "event_type": "referral",
        "amount": 0,
        "timestamp": "2026-06-22T10:00:00Z"
    })
    
    response = client.get('/balance/user_100')
    assert response.status_code == 200
    assert response.get_json()['balance'] == 70
