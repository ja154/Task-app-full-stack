import { useState } from "react";

const TaskForm = ({ existingTask = {}, updateCallback, token }) => {
  const [title, setTitle] = useState(existingTask.title || "");
  const [description, setDescription] = useState(existingTask.description || "");
  const [priority, setPriority] = useState(existingTask.priority || "medium");
  const [dueDate, setDueDate] = useState(
    existingTask.due_date ? existingTask.due_date.split("T")[0] : ""
  );
  const [loading, setLoading] = useState(false);

  const updating = Object.entries(existingTask).length !== 0;

  const onSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const data = {
      title,
      description,
      priority,
      due_date: dueDate ? new Date(dueDate).toISOString() : null,
    };

    const url = updating
      ? `http://127.0.0.1:5000/tasks/${existingTask.id}`
      : "http://127.0.0.1:5000/tasks";

    const options = {
      method: updating ? "PATCH" : "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(data),
    };

    try {
      const response = await fetch(url, options);
      const result = await response.json();

      if (response.ok) {
        updateCallback();
      } else {
        alert(result.message || "Operation failed");
      }
    } catch (error) {
      alert("Error: " + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={onSubmit} className="task-form">
      <h3>{updating ? "Edit Task" : "Create New Task"}</h3>

      <div className="form-group">
        <label htmlFor="title">Title *</label>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
          disabled={loading}
          placeholder="Enter task title"
        />
      </div>

      <div className="form-group">
        <label htmlFor="description">Description</label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          disabled={loading}
          placeholder="Enter task description (optional)"
          rows="4"
        />
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="priority">Priority</label>
          <select
            id="priority"
            value={priority}
            onChange={(e) => setPriority(e.target.value)}
            disabled={loading}
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="dueDate">Due Date</label>
          <input
            type="date"
            id="dueDate"
            value={dueDate}
            onChange={(e) => setDueDate(e.target.value)}
            disabled={loading}
          />
        </div>
      </div>

      <button type="submit" className="btn-submit" disabled={loading}>
        {loading ? "Saving..." : updating ? "Update Task" : "Create Task"}
      </button>
    </form>
  );
};

export default TaskForm;