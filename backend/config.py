from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import os
from datetime import timedelta
from dotenv import load_dotenv, find_dotenv

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Load environment variables from a .env file.
# Use find_dotenv() so a `.env` at the project root (or any parent dir) is
# discovered automatically even when running the server from `backend/`.
load_dotenv(find_dotenv())

# Database configuration
# Prefer a DATABASE_URL env var (for production). Fall back to a file in the
# `instance/` folder for local development. Keeping the DB inside `instance/`
# makes it easy to ignore from source control.
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
	"DATABASE_URL", "sqlite:///instance/taskmanager.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# JWT configuration
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "your-secret-key-change-in-production")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
