from database import db
from datetime import datetime, timezone

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.String(100), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    points_awarded = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='processed') # processed, reversed

class Ledger(db.Model):
    __tablename__ = 'ledger'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    entry_type = db.Column(db.String(20), nullable=False) # credit, debit, reversal
    reference_event_id = db.Column(db.String(100), nullable=True) # links to event_id or None for redemption
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class Reward(db.Model):
    __tablename__ = 'reward'
    id = db.Column(db.Integer, primary_key=True)
    reward_name = db.Column(db.String(100), nullable=False)
    points_required = db.Column(db.Integer, nullable=False)
