from config import app, db
from models import User, Task

def initialize_database():
    """Creates the database tables."""
    print("Initializing the database...")
    with app.app_context():
        db.create_all()
    print("Database has been initialized successfully.")

if __name__ == '__main__':
    initialize_database()
