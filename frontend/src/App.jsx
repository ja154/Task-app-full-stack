import { useState, useEffect } from "react";
import "./App.css";
import AuthForm from "./AuthForm";
import TaskList from "./TaskList";
import TaskForm from "./TaskForm";
import TaskStats from "./TaskStatus";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [user, setUser] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentTask, setCurrentTask] = useState({});
  const [filter, setFilter] = useState("all");
  const [stats, setStats] = useState({});

  useEffect(() => {
    if (token) {
      fetchCurrentUser();
      fetchTasks();
      fetchStats();
    }
  }, [token]);

  const fetchCurrentUser = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/me", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setUser(data.user);
      } else {
        handleLogout();
      }
    } catch (error) {
      console.error("Error fetching user:", error);
      handleLogout();
    }
  };

  const fetchTasks = async (filterParam = filter) => {
    try {
      let url = "http://127.0.0.1:5000/tasks";
      if (filterParam !== "all") {
        url += `?completed=${filterParam === "completed"}`;
      }
      
      const response = await fetch(url, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setTasks(data.tasks);
      } else {
        console.error("Failed to fetch tasks");
      }
    } catch (error) {
      console.error("Error fetching tasks:", error);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/tasks/stats", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setStats(data);
      } else {
        console.error("Failed to fetch stats");
      }
    } catch (error) {
      console.error("Error fetching stats:", error);
    }
  };

  const handleLogin = (newToken, userData) => {
    localStorage.setItem("token", newToken);
    setToken(newToken);
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setUser(null);
    setTasks([]);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setCurrentTask({});
  };

  const openCreateModal = () => {
    if (!isModalOpen) setIsModalOpen(true);
  };

  const openEditModal = (task) => {
    if (isModalOpen) return;
    setCurrentTask(task);
    setIsModalOpen(true);
  };

  const onUpdate = () => {
    closeModal();
    fetchTasks();
    fetchStats();
  };

  const handleFilterChange = (newFilter) => {
    setFilter(newFilter);
    fetchTasks(newFilter);
  };

  if (!token) {
    return <AuthForm onLogin={handleLogin} />;
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-content">
          <h1>Task Manager</h1>
          <div className="user-info">
            <span>Welcome, {user?.username}!</span>
            <button onClick={handleLogout} className="btn-logout">
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="main-content">
        <TaskStats stats={stats} />

        <div className="task-controls">
          <button onClick={openCreateModal} className="btn-create">
            + New Task
          </button>
          <div className="filter-buttons">
            <button
              className={filter === "all" ? "active" : ""}
              onClick={() => handleFilterChange("all")}
            >
              All
            </button>
            <button
              className={filter === "pending" ? "active" : ""}
              onClick={() => handleFilterChange("pending")}
            >
              Pending
            </button>
            <button
              className={filter === "completed" ? "active" : ""}
              onClick={() => handleFilterChange("completed")}
            >
              Completed
            </button>
          </div>
        </div>

        <TaskList
          tasks={tasks}
          updateTask={openEditModal}
          updateCallback={onUpdate}
          token={token}
        />

        {isModalOpen && (
          <div className="modal">
            <div className="modal-content">
              <span className="close" onClick={closeModal}>
                &times;
              </span>
              <TaskForm
                existingTask={currentTask}
                updateCallback={onUpdate}
                token={token}
              />
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;