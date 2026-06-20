from flask import Blueprint, jsonify
from models import Ledger
from database import db
from sqlalchemy import func

rewards_bp = Blueprint('rewards', __name__)

@rewards_bp.route('/balance/<user_id>', methods=['GET'])
def get_balance(user_id):
    # Calculate user balance by summing ledger points
    result = db.session.query(func.sum(Ledger.points)).filter(Ledger.user_id == user_id).scalar()
    balance = result if result else 0
    
    return jsonify({
        "user_id": user_id,
        "balance": int(balance)
    }), 200

@rewards_bp.route('/ledger/<user_id>', methods=['GET'])
def get_ledger(user_id):
    entries = Ledger.query.filter_by(user_id=user_id).order_by(Ledger.created_at.desc()).all()
    history = []
    for entry in entries:
        history.append({
            "id": entry.id,
            "points": entry.points,
            "entry_type": entry.entry_type,
            "reference_event_id": entry.reference_event_id,
            "created_at": entry.created_at.isoformat() if entry.created_at else None
        })
    
    return jsonify({
        "user_id": user_id,
        "history": history
    }), 200
