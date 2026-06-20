def test_redemption_success(client):
    # Give user 100 points
    client.post('/events', json={
        "event_id": "evt_201",
        "user_id": "user_200",
        "event_type": "referral",
        "amount": 0,
        "timestamp": "2026-06-20T10:00:00Z" # Saturday: min(50 * 2, 100) = 100
    })
    
    response = client.post('/redeem', json={
        "user_id": "user_200",
        "reward_id": 1 # 50 points
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['new_balance'] == 50
    assert data['reward'] == 'Coffee Coupon'
    
def test_redemption_insufficient_balance(client):
    # Give user 10 points
    client.post('/events', json={
        "event_id": "evt_301",
        "user_id": "user_300",
        "event_type": "deposit",
        "amount": 100,
        "timestamp": "2026-06-22T10:00:00Z" # Monday: 10
    })
    
    response = client.post('/redeem', json={
        "user_id": "user_300",
        "reward_id": 2 # 100 points
    })
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Insufficient points'
    assert data['balance'] == 10
