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
# Read DATABASE_URL from environment (or .env). If it's a SQLite URL that
# references a relative file (e.g. sqlite:///instance/taskmanager.db) convert
# it to an absolute path based on the repository root so it resolves
# consistently whether you run commands from the project root or the
# `backend/` folder.
raw_db_url = os.environ.get("DATABASE_URL", "sqlite:///instance/taskmanager.db")

def _resolve_sqlite_url(url: str) -> str:
	"""Convert relative sqlite URLs to absolute file paths.

	Examples:
	  sqlite:///instance/taskmanager.db -> sqlite:////abs/path/to/instance/taskmanager.db
	  sqlite:////already/absolute/path.db -> unchanged
	"""
	if not url.startswith("sqlite:///"):
		return url

	# If it already has 4 slashes (sqlite:////), treat it as absolute already.
	if url.startswith("sqlite:////"):
		return url

	# url starts with sqlite:/// and the path portion is relative. Resolve it
	# against the repository root (one directory up from this `backend/` file).
	rel_path = url[len("sqlite:///"):]
	backend_dir = os.path.dirname(__file__)
	repo_root = os.path.abspath(os.path.join(backend_dir, ".."))
	abs_path = os.path.abspath(os.path.join(repo_root, rel_path))

	# Ensure the directory exists so SQLite can create the file.
	parent_dir = os.path.dirname(abs_path)
	try:
		os.makedirs(parent_dir, exist_ok=True)
	except Exception:
		# If directory creation fails, return original URL and let the
		# application raise the appropriate error later.
		return url

	# Prepend three slashes; since abs_path starts with '/', this becomes
	# sqlite:////absolute/path which is the correct absolute-file URI form.
	return "sqlite:///" + abs_path


app.config["SQLALCHEMY_DATABASE_URI"] = _resolve_sqlite_url(raw_db_url)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# JWT configuration
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "your-secret-key-change-in-production")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
