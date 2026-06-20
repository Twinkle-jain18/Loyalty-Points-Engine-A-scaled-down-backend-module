import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///loyalty.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Base Rules
    RULES_BASE = {
        'deposit': 10,
        'purchase': 5,
        'referral': 50,
        'withdrawal': 0
    }
    
    # Bonus and Caps
    RULES_WEEKEND_MULTIPLIER = 2
    RULES_MAX_POINTS_PER_EVENT = 100
