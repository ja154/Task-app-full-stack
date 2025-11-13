# Task Manager - Full Stack Application

A production-ready task management application built with **Flask (Python)** backend and **React (Vite)** frontend. Users can create accounts, manage tasks with CRUD operations, and track their productivity.

## 🚀 Features

### Authentication
- **User Registration** with secure password hashing (bcrypt)
- **JWT-based Authentication** with 24-hour token expiry
- **Login/Logout** functionality
- Password validation (min 8 chars, uppercase, lowercase, number)

### Task Management
- ✅ **Create Tasks** with title, description, priority, and due date
- 📝 **Update Tasks** - edit any task detail
- ✔️ **Toggle Completion** - mark tasks as done/undone
- 🗑️ **Delete Tasks** - remove unwanted tasks
- 🔍 **Filter Tasks** - view all, pending, or completed tasks
- 📊 **Task Statistics** - overview of total, pending, completed, and high-priority tasks

### Task Properties
- **Priority Levels**: Low, Medium, High
- **Due Dates**: Optional deadline tracking
- **Completion Status**: Track finished tasks
- **Timestamps**: Created and updated timestamps

## 📁 Project Structure

```
task-manager/
├── backend/
│   ├── config.py          # Flask app configuration
│   ├── models.py          # Database models (User, Task)
│   ├── main.py            # API routes and business logic
│   └── requirements.txt   # Python dependencies
│
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── AuthForm.jsx      # Login/Register component
    │   │   ├── TaskList.jsx      # Task display component
    │   │   ├── TaskForm.jsx      # Task create/edit form
    │   │   └── TaskStats.jsx     # Statistics dashboard
    │   ├── App.jsx               # Main application component
    │   ├── App.css               # Application styles
    │   ├── main.jsx              # React entry point
    │   └── index.css             # Global styles
    ├── index.html
    ├── package.json
    └── vite.config.js
```

## 🛠️ Technology Stack

### Backend
- **Flask** - Python web framework
- **SQLAlchemy** - ORM for database operations
- **Flask-JWT-Extended** - JWT authentication
- **Flask-Bcrypt** - Password hashing
- **Flask-CORS** - Cross-origin resource sharing
- **SQLite** - Database (easily switchable to PostgreSQL/MySQL)

### Frontend
- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Modern CSS** - Responsive design with flexbox/grid
- **Fetch API** - HTTP requests

## 📋 Prerequisites

- **Python 3.8+** installed
- **Node.js 16+** and npm installed
- Basic knowledge of REST APIs

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd task-manager
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize the database (run this once)
python init_db.py

# Run the Flask server
python main.py
```

The backend will start at `http://127.0.0.1:5000`

### 3. Frontend Setup

```bash
# Open a new terminal and navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will start at `http://localhost:5173`

## 🔐 Environment Variables (Optional)

For production, create a `.env` file in the backend directory:

```env
JWT_SECRET_KEY=your-super-secret-key-change-this
SQLALCHEMY_DATABASE_URI=sqlite:///taskmanager.db
```

## 📡 API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/register` | Register new user | No |
| POST | `/login` | Login user | No |
| GET | `/me` | Get current user | Yes |

### Task Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/tasks` | Get all user tasks | Yes |
| GET | `/tasks/<id>` | Get specific task | Yes |
| POST | `/tasks` | Create new task | Yes |
| PATCH | `/tasks/<id>` | Update task | Yes |
| DELETE | `/tasks/<id>` | Delete task | Yes |
| PATCH | `/tasks/<id>/toggle` | Toggle completion | Yes |
| GET | `/tasks/stats` | Get task statistics | Yes |

### Request/Response Examples

#### Register User
```json
POST /register
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123"
}

Response:
{
  "message": "User registered successfully",
  "access_token": "eyJ0eXAiOiJKV1...",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com"
  }
}
```

#### Create Task
```json
POST /tasks
Headers: { "Authorization": "Bearer <token>" }
{
  "title": "Complete project",
  "description": "Finish the task manager app",
  "priority": "high",
  "due_date": "2024-12-31T23:59:59"
}
```

## 🎨 Features Walkthrough

### 1. User Registration & Login
- Create an account with username, email, and secure password
- Login to receive JWT token stored in localStorage
- Automatic session management

### 2. Dashboard Overview
- View task statistics at a glance
- Quick access to create new tasks
- Filter tasks by status (All, Pending, Completed)

### 3. Task Management
- **Create**: Click "New Task" button to open form
- **Edit**: Click "Edit" button on any task card
- **Complete**: Check checkbox to mark as done
- **Delete**: Remove tasks with confirmation

### 4. Task Filtering
- Filter by completion status
- Tasks are color-coded by priority
- Real-time updates on all actions

## 🔒 Security Features

1. **Password Hashing**: Bcrypt with automatic salt generation
2. **JWT Authentication**: Secure token-based auth with expiry
3. **Input Validation**: Server-side validation for all inputs
4. **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection
5. **CORS Configuration**: Controlled cross-origin requests

## 🎯 Best Practices Implemented

- **RESTful API Design**: Standard HTTP methods and status codes
- **Component Architecture**: Reusable React components
- **Error Handling**: Comprehensive error messages
- **Responsive Design**: Mobile-first CSS approach
- **Code Organization**: Separation of concerns (models, routes, components)
- **Database Relationships**: Proper foreign key constraints
- **User Experience**: Loading states, confirmations, error feedback

## 🐛 Troubleshooting

### Backend Issues

**Database not created:**
```bash
python -c "from config import app, db; app.app_context().push(); db.create_all()"
```

**CORS errors:**
Ensure Flask-CORS is installed and configured in `config.py`

### Frontend Issues

**Token errors:**
Clear localStorage: `localStorage.removeItem('token')`

**Port already in use:**
Change port in `vite.config.js` or kill the process

## 🚀 Production Deployment

### Frontend Deployment (Vercel)

The frontend is already configured in `vercel.json` for Vercel deployment.

1. **Connect your GitHub repo to Vercel**:
   - Go to vercel.com → Import Project → Select your GitHub repo
   - Vercel auto-detects `vercel.json` configuration

2. **Set Backend API URL** (Critical for mobile/external users):
   - In Vercel Dashboard → Project Settings → Environment Variables
   - Add: `VITE_API_URL=https://your-backend-url.com` (e.g., `https://task-api-production.herokuapp.com`)
   - Redeploy the frontend after adding the variable

3. **Frontend will now be live at**: `https://task-app-full-stack.vercel.app` (or your custom domain)

### Backend Deployment

Choose one of the following:

#### Option A: Deploy to Render (Recommended for SQLite-based projects)
1. Create account at render.com
2. Create a new Web Service → Connect GitHub repo
3. Set environment variables:
   - `JWT_SECRET_KEY=your-secret-key-here`
   - `DATABASE_URL=sqlite:///instance/taskmanager.db` (default, or switch to PostgreSQL)
4. Build Command: `cd backend && pip install -r requirements.txt && python init_db.py`
5. Start Command: `cd backend && python main.py`
6. Copy the Render URL and use it as `VITE_API_URL` in Vercel

#### Option B: Deploy to Heroku
1. Create account at heroku.com
2. Install Heroku CLI and run: `heroku login`
3. From project root: `heroku create task-api-production`
4. Add PostgreSQL addon: `heroku addons:create heroku-postgresql:hobby-dev`
5. Set environment: `heroku config:set JWT_SECRET_KEY=your-secret-key-here`
6. Create `Procfile` in root:
   ```
   web: cd backend && gunicorn config:app
   ```
7. Install gunicorn: `pip install gunicorn` (add to `backend/requirements.txt`)
8. Deploy: `git push heroku main`
9. Use Heroku URL as `VITE_API_URL` in Vercel

#### Option C: Deploy to Railway or Fly.io
- Similar process to Render; see their documentation for Flask apps
- Ensure DATABASE_URL environment variable is set

### Connecting Frontend to Backend

After deploying backend:
1. Copy your backend deployment URL (e.g., `https://task-api-production.herokuapp.com`)
2. In Vercel Dashboard → Settings → Environment Variables
3. Add `VITE_API_URL=<your-backend-url>`
4. Trigger a redeploy (Vercel → Deployments → Redeploy)
5. Mobile users can now register/login successfully

### Database Notes

- **SQLite** (current): Works for small projects; file-based, no setup needed. Not ideal for serverless.
- **PostgreSQL** (recommended for production):
  - Use Supabase, Railway, or Heroku Postgres
  - Update `DATABASE_URL` env var to PostgreSQL connection string
  - No code changes needed (SQLAlchemy handles both)

## 📝 Future Enhancements

- [ ] Task categories/tags
- [ ] Task sharing between users
- [ ] Email notifications for due dates
- [ ] Task search functionality
- [ ] Dark mode theme
- [ ] Export tasks to CSV/PDF
- [ ] Recurring tasks
- [ ] File attachments
- [ ] Task comments/notes

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Built with ❤️ for learning full-stack development

## 🙏 Acknowledgments

- Flask documentation
- React documentation
- JWT authentication best practices
- Modern CSS techniques

---

**Happy Task Managing! 🎉**