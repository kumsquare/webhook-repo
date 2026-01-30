from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from app.extensions import init_extensions
from app.webhook.routes import webhook
import os

# Creating our flask app
def create_app():
    load_dotenv()

    app = Flask(__name__)

    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    
    CORS(app)
    
    init_extensions(app)
    # registering all the blueprints
    app.register_blueprint(webhook)
    
    return app
