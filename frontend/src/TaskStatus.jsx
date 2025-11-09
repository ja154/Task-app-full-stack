import React from "react";

const TaskStats = ({ stats }) => {
  return (
    <div className="stats-container">
      <div className="stat-card">
        <div className="stat-value">{stats.total || 0}</div>
        <div className="stat-label">Total Tasks</div>
      </div>
      
      <div className="stat-card pending">
        <div className="stat-value">{stats.pending || 0}</div>
        <div className="stat-label">Pending</div>
      </div>
      
      <div className="stat-card completed">
        <div className="stat-value">{stats.completed || 0}</div>
        <div className="stat-label">Completed</div>
      </div>
      
      <div className="stat-card high-priority">
        <div className="stat-value">{stats.high_priority_pending || 0}</div>
        <div className="stat-label">High Priority</div>
      </div>
    </div>
  );
};

export default TaskStats;