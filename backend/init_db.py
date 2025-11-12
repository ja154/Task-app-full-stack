"""Initialize the database without starting the Flask server.

Run this from the `backend/` folder (or with Python path adjusted):

  source venv/bin/activate
  python init_db.py

This will call `db.create_all()` under the application context and
create the SQLite file specified by `SQLALCHEMY_DATABASE_URI`.
"""
from config import app, db
from models import User, Task


def init_db():
    """Create the database tables."""
    print("Initializing the database...")
    with app.app_context():
        db.create_all()
    print("Database has been initialized successfully.")


if __name__ == "__main__":
    init_db()
