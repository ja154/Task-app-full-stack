from flask import request, jsonify
from config import app, db, bcrypt, jwt
from models import User, Task
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
import re

# Validation helpers
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Password must be at least 8 characters with 1 uppercase, 1 lowercase, and 1 number"""
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    return True


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    print(f"Looking up user with identity: {identity}")
    user = User.query.get(identity)
    if user is None:
        print(f"User with identity {identity} not found in the database.")
    else:
        print(f"User with identity {identity} found: {user.username}")
    return user


# ============ AUTH ROUTES ============

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    
    # Validation
    if not username or not email or not password:
        return jsonify({"message": "Username, email, and password are required"}), 400
    
    if len(username) < 3:
        return jsonify({"message": "Username must be at least 3 characters"}), 400
    
    if not validate_email(email):
        return jsonify({"message": "Invalid email format"}), 400
    
    if not validate_password(password):
        return jsonify({"message": "Password must be at least 8 characters with uppercase, lowercase, and number"}), 400
    
    # Check if user exists
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already registered"}), 400
    
    # Create user
    try:
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        
        # Create access token
        access_token = create_access_token(identity=str(new_user.id))
        
        return jsonify({
            "message": "User registered successfully",
            "access_token": access_token,
            "user": new_user.to_json()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400
    
    # Find user by username or email
    user = User.query.filter((User.username == username) | (User.email == username)).first()
    
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"message": "Invalid username or password"}), 401
    
    # Create access token
    access_token = create_access_token(identity=str(user.id))
    
    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "user": user.to_json()
    }), 200


@app.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    return jsonify({"user": user.to_json()}), 200


# ============ TASK ROUTES ============

@app.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    
    # Query parameters for filtering
    completed = request.args.get("completed")
    priority = request.args.get("priority")
    
    query = Task.query.filter_by(user_id=user_id)
    
    if completed is not None:
        completed_bool = completed.lower() == "true"
        query = query.filter_by(completed=completed_bool)
    
    if priority:
        query = query.filter_by(priority=priority)
    
    tasks = query.order_by(Task.created_at.desc()).all()
    
    return jsonify({"tasks": [task.to_json() for task in tasks]}), 200


@app.route("/tasks/<int:task_id>", methods=["GET"])
@jwt_required()
def get_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    
    if not task:
        return jsonify({"message": "Task not found"}), 404
    
    return jsonify({"task": task.to_json()}), 200


@app.route("/tasks", methods=["POST"])
@jwt_required()
def create_task():
    user_id = get_jwt_identity()
    data = request.json
    
    title = data.get("title")
    description = data.get("description", "")
    priority = data.get("priority", "medium")
    due_date_str = data.get("due_date")
    
    # Validation
    if not title:
        return jsonify({"message": "Task title is required"}), 400
    
    if priority not in ["low", "medium", "high"]:
        return jsonify({"message": "Priority must be low, medium, or high"}), 400
    
    # Parse due date
    due_date = None
    if due_date_str:
        try:
            due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
        except ValueError:
            return jsonify({"message": "Invalid date format"}), 400
    
    try:
        new_task = Task(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            user_id=user_id
        )
        db.session.add(new_task)
        db.session.commit()
        
        return jsonify({
            "message": "Task created successfully",
            "task": new_task.to_json()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


@app.route("/tasks/<int:task_id>", methods=["PATCH"])
@jwt_required()
def update_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    
    if not task:
        return jsonify({"message": "Task not found"}), 404
    
    data = request.json
    
    # Update fields
    if "title" in data:
        if not data["title"]:
            return jsonify({"message": "Task title cannot be empty"}), 400
        task.title = data["title"]
    
    if "description" in data:
        task.description = data["description"]
    
    if "completed" in data:
        task.completed = data["completed"]
    
    if "priority" in data:
        if data["priority"] not in ["low", "medium", "high"]:
            return jsonify({"message": "Priority must be low, medium, or high"}), 400
        task.priority = data["priority"]
    
    if "due_date" in data:
        if data["due_date"]:
            try:
                task.due_date = datetime.fromisoformat(data["due_date"].replace('Z', '+00:00'))
            except ValueError:
                return jsonify({"message": "Invalid date format"}), 400
        else:
            task.due_date = None
    
    try:
        db.session.commit()
        return jsonify({
            "message": "Task updated successfully",
            "task": task.to_json()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    
    if not task:
        return jsonify({"message": "Task not found"}), 404
    
    try:
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


@app.route("/tasks/<int:task_id>/toggle", methods=["PATCH"])
@jwt_required()
def toggle_task_completion(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    
    if not task:
        return jsonify({"message": "Task not found"}), 404
    
    task.completed = not task.completed
    
    try:
        db.session.commit()
        return jsonify({
            "message": "Task status toggled",
            "task": task.to_json()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


# ============ STATS ROUTE ============

@app.route("/tasks/stats", methods=["GET"])
@jwt_required()
def get_task_stats():
    user_id = get_jwt_identity()
    
    total_tasks = Task.query.filter_by(user_id=user_id).count()
    completed_tasks = Task.query.filter_by(user_id=user_id, completed=True).count()
    pending_tasks = total_tasks - completed_tasks
    
    high_priority = Task.query.filter_by(user_id=user_id, priority="high", completed=False).count()
    
    return jsonify({
        "total": total_tasks,
        "completed": completed_tasks,
        "pending": pending_tasks,
        "high_priority_pending": high_priority
    }), 200


# ============ APP INITIALIZATION ============

if __name__ == "__main__":
    app.run(debug=True, port=5000)