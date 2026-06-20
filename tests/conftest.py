import pytest
import sys
import os

# Ensure the app directory is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from database import db
from models import Reward

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

@pytest.fixture
def app():
    app = create_app(TestConfig)
    
    with app.app_context():
        db.create_all()
        # Seed rewards
        rewards = [
            Reward(id=1, reward_name="Coffee Coupon", points_required=50),
            Reward(id=2, reward_name="Movie Ticket", points_required=100),
            Reward(id=3, reward_name="Gift Card", points_required=200)
        ]
        db.session.bulk_save_objects(rewards)
        db.session.commit()
        
        yield app
        
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_database(app):
    with app.app_context():
        yield db
