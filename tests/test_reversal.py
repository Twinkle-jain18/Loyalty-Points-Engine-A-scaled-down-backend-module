def test_event_reversal(client):
    # Deposit (Monday = 10)
    client.post('/events', json={
        "event_id": "evt_401",
        "user_id": "user_400",
        "event_type": "deposit",
        "amount": 100,
        "timestamp": "2026-06-22T10:00:00Z"
    })
    
    bal_response = client.get('/balance/user_400')
    assert bal_response.get_json()['balance'] == 10
    
    rev_response = client.post('/reverse', json={
        "event_id": "evt_401"
    })
    assert rev_response.status_code == 200
    assert rev_response.get_json()['points_deducted'] == 10
    
    bal_response2 = client.get('/balance/user_400')
    assert bal_response2.get_json()['balance'] == 0

def test_double_reversal_prevention(client):
    client.post('/events', json={
        "event_id": "evt_501",
        "user_id": "user_500",
        "event_type": "deposit",
        "amount": 100,
        "timestamp": "2026-06-22T10:00:00Z"
    })
    
    client.post('/reverse', json={"event_id": "evt_501"})
    
    rev_response = client.post('/reverse', json={"event_id": "evt_501"})
    assert rev_response.status_code == 400
    assert rev_response.get_json()['error'] == 'Event already reversed'
