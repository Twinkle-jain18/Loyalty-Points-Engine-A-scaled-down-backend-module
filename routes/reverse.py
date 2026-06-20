from flask import Blueprint, request, jsonify
from database import db
from models import Event, Ledger

reverse_bp = Blueprint('reverse', __name__)

@reverse_bp.route('/reverse', methods=['POST'])
def reverse_event():
    data = request.get_json()
    if not data or 'event_id' not in data:
        return jsonify({"error": "Missing event_id"}), 400
        
    event_id = data['event_id']
    
    event = Event.query.filter_by(event_id=event_id).first()
    if not event:
        return jsonify({"error": "Event not found"}), 404
        
    if event.status == 'reversed':
        return jsonify({"error": "Event already reversed"}), 400
        
    # Create compensating ledger entry
    compensating_entry = Ledger(
        user_id=event.user_id,
        points=-event.points_awarded,
        entry_type='reversal',
        reference_event_id=event_id
    )
    db.session.add(compensating_entry)
    
    # Mark event as reversed
    event.status = 'reversed'
    
    db.session.commit()
    
    return jsonify({
        "message": "Event reversed successfully",
        "points_deducted": event.points_awarded
    }), 200
