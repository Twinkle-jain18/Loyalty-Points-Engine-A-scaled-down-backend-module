from flask import Flask
from config import Config
from database import db

# Import blueprints
from routes.events import events_bp
from routes.rewards import rewards_bp
from routes.redeem import redeem_bp
from routes.reverse import reverse_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    
    app.register_blueprint(events_bp)
    app.register_blueprint(rewards_bp)
    app.register_blueprint(redeem_bp)
    app.register_blueprint(reverse_bp)
    
    # Database initialization command
    @app.cli.command("init-db")
    def init_db():
        """Initialize the database and seed rewards."""
        db.create_all()
        from models import Reward
        
        if not Reward.query.first():
            rewards = [
                Reward(reward_name="Coffee Coupon", points_required=50),
                Reward(reward_name="Movie Ticket", points_required=100),
                Reward(reward_name="Gift Card", points_required=200)
            ]
            db.session.bulk_save_objects(rewards)
            db.session.commit()
            print("Database initialized and rewards seeded.")
        else:
            print("Database already initialized.")
            
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
