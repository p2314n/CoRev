
import os                                # Used for handling file and directory paths
from flask import Flask                  # Import the Flask web framework
from flask_pymongo import PyMongo        # Import PyMongo for MongoDB integration

mongo = PyMongo()                        # Create a PyMongo instance (not yet connected)

def create_app():
    # Create and configure the Flask app
    app = Flask(
        __name__,
        # Set correct paths for templates and static files
        template_folder=os.path.join(os.path.dirname(__file__), "..", "templates"),
        static_folder=os.path.join(os.path.dirname(__file__), "..", "static")
    )

    app.secret_key = "your_secret_key"   # Secret key for session and flash message security

    # Configure the MongoDB connection (local MongoDB running on port 27017)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/rating"

    # Initialize PyMongo with the Flask app
    mongo.init_app(app)

    # Import all route blueprints (each file manages a specific part of the app)
    from .register_route import register_bp
    from .dashboard_route import dashboard_bp
    from .subject_route import subject_bp
    from .login_route import login_bp
    from routes.logout_route import logout_bp

    # Register blueprints so their routes are added to the app
    app.register_blueprint(register_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(subject_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(logout_bp)

    # Return the fully configured app instance
    return app