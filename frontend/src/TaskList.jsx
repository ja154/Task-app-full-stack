import React from "react";

const TaskList = ({ tasks, updateTask, updateCallback, token }) => {
  const onDelete = async (id) => {
    if (!confirm("Are you sure you want to delete this task?")) return;

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/tasks/${id}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      
      if (response.ok) {
        updateCallback();
      } else {
        alert("Failed to delete task");
      }
    } catch (error) {
      alert("Error: " + error.message);
    }
  };

  const onToggle = async (id) => {
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/tasks/${id}/toggle`,
        {
          method: "PATCH",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      
      if (response.ok) {
        updateCallback();
      }
    } catch (error) {
      alert("Error: " + error.message);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return "No due date";
    const date = new Date(dateString);
    return date.toLocaleDateString();
  };

  const getPriorityClass = (priority) => {
    return `priority priority-${priority}`;
  };

  if (tasks.length === 0) {
    return (
      <div className="empty-state">
        <p>No tasks found. Create your first task!</p>
      </div>
    );
  }

  return (
    <div className="task-list">
      {tasks.map((task) => (
        <div
          key={task.id}
          className={`task-card ${task.completed ? "completed" : ""}`}
        >
          <div className="task-header">
            <div className="task-title-section">
              <input
                type="checkbox"
                checked={task.completed}
                onChange={() => onToggle(task.id)}
                className="task-checkbox"
              />
              <h3 className={task.completed ? "line-through" : ""}>
                {task.title}
              </h3>
            </div>
            <span className={getPriorityClass(task.priority)}>
              {task.priority}
            </span>
          </div>

          {task.description && (
            <p className="task-description">{task.description}</p>
          )}

          <div className="task-footer">
            <span className="task-date">
              📅 {formatDate(task.due_date)}
            </span>
            <div className="task-actions">
              <button
                onClick={() => updateTask(task)}
                className="btn-edit"
                disabled={task.completed}
              >
                Edit
              </button>
              <button
                onClick={() => onDelete(task.id)}
                className="btn-delete"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default TaskList;