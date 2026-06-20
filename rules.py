from config import Config
from datetime import datetime

def calculate_points(event_type: str, timestamp_str: str) -> int:
    """
    Calculate points based on rules:
    - Base points by event_type
    - Weekend multiplier (2x)
    - Max 100 points per event
    """
    base_points = Config.RULES_BASE.get(event_type, 0)
    
    # Check weekend (Saturday=5, Sunday=6)
    try:
        # Expected format: 2026-06-20T10:00:00Z
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        is_weekend = dt.weekday() in [5, 6]
    except ValueError:
        is_weekend = False

    points = base_points
    if is_weekend:
        points *= Config.RULES_WEEKEND_MULTIPLIER
        
    if points > Config.RULES_MAX_POINTS_PER_EVENT:
        points = Config.RULES_MAX_POINTS_PER_EVENT
        
    return points
