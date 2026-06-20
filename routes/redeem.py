from flask import Blueprint, request, jsonify
from database import db
from models import Ledger, Reward
from sqlalchemy import func

redeem_bp = Blueprint('redeem', __name__)

@redeem_bp.route('/redeem', methods=['POST'])
def redeem_points():
    data = request.get_json()
    if not data or 'user_id' not in data or 'reward_id' not in data:
        return jsonify({"error": "Missing user_id or reward_id"}), 400
        
    user_id = data['user_id']
    reward_id = data['reward_id']
    
    reward = Reward.query.get(reward_id)
    if not reward:
        return jsonify({"error": "Reward not found"}), 404
        
    # Calculate user balance
    result = db.session.query(func.sum(Ledger.points)).filter(Ledger.user_id == user_id).scalar()
    balance = result if result else 0
    
    if balance < reward.points_required:
        return jsonify({
            "error": "Insufficient points",
            "balance": int(balance),
            "required": reward.points_required
        }), 400
        
    # Create debit ledger entry
    debit_entry = Ledger(
        user_id=user_id,
        points=-reward.points_required,
        entry_type='debit',
        reference_event_id=None
    )
    db.session.add(debit_entry)
    db.session.commit()
    
    new_balance = balance - reward.points_required
    
    return jsonify({
        "message": "Redemption successful",
        "reward": reward.reward_name,
        "new_balance": int(new_balance)
    }), 200
