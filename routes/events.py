from flask import Blueprint, request, jsonify
from database import db
from models import Event, Ledger
from rules import calculate_points
from config import Config
from datetime import datetime

events_bp = Blueprint('events', __name__)

@events_bp.route('/events', methods=['POST'])
def ingest_event():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON payload"}), 400
        
    required_fields = ['event_id', 'user_id', 'event_type', 'amount', 'timestamp']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
            
    event_id = data['event_id']
    
    # Check for valid event_type
    if data['event_type'] not in Config.RULES_BASE:
        return jsonify({"error": "Invalid event_type"}), 400

    # Idempotency check
    existing_event = Event.query.filter_by(event_id=event_id).first()
    if existing_event:
        # Idempotent response
        return jsonify({
            "message": "Event already processed",
            "points_awarded": existing_event.points_awarded
        }), 200
        
    # Calculate points
    try:
        dt = datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))
    except ValueError:
        return jsonify({"error": "Invalid timestamp format"}), 400
        
    points = calculate_points(data['event_type'], data['timestamp'])
    
    # Store event
    new_event = Event(
        event_id=event_id,
        user_id=data['user_id'],
        event_type=data['event_type'],
        amount=float(data['amount']),
        timestamp=dt,
        points_awarded=points,
        status='processed'
    )
    db.session.add(new_event)
    
    # Create ledger credit entry
    ledger_entry = Ledger(
        user_id=data['user_id'],
        points=points,  # positive value
        entry_type='credit',
        reference_event_id=event_id
    )
    db.session.add(ledger_entry)
    
    db.session.commit()
    
    return jsonify({
        "message": "Event processed successfully",
        "points_awarded": points
    }), 201
