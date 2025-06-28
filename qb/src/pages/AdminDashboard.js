import React, { useEffect, useState } from "react";
import Chart from "chart.js/auto";

const AdminDashboard = () => {
  const [analytics, setAnalytics] = useState(null);

  useEffect(() => {
    fetch("/admin/analytics/data")
      .then((res) => res.json())
      .then((data) => {
        setAnalytics(data);
        renderCharts(data);
      })
      .catch((err) => console.error("Error loading analytics:", err));
  }, []);

  const renderCharts = (data) => {
    const subjectCtx = document.getElementById("subjectPerformanceChart");
    const qualCtx = document.getElementById("qualificationDistributionChart");
    const perfCtx = document.getElementById("performanceDistributionChart");

    new Chart(subjectCtx, {
      type: "bar",
      data: {
        labels: data.subject_performance.map((s) => s.subject),
        datasets: [
          {
            label: "Average Score",
            data: data.subject_performance.map((s) => s.avg_score),
            backgroundColor: "rgba(54, 162, 235, 0.5)",
          },
        ],
      },
    });

    new Chart(qualCtx, {
      type: "pie",
      data: {
        labels: data.qualification_distribution.map((q) => q.qualification),
        datasets: [
          {
            data: data.qualification_distribution.map((q) => q.count),
            backgroundColor: ["#ff6384", "#36a2eb", "#ffce56"],
          },
        ],
      },
    });

    new Chart(perfCtx, {
      type: "bar",
      data: {
        labels: data.performance_distribution.map((p) => p.score),
        datasets: [
          {
            label: "Students Count",
            data: data.performance_distribution.map((p) => p.count),
            backgroundColor: "rgba(255, 99, 132, 0.5)",
          },
        ],
      },
    });
  };

  if (!analytics) return <p>Loading analytics...</p>;

  return (
    <div className="container mt-4">
      <h2>Admin Analytics</h2>

      <div className="row">
        <div className="col-md-3">
          <div className="card text-white bg-primary mb-3">
            <div className="card-body">
              <h5 className="card-title">Total Students</h5>
              <p className="card-text">{analytics.total_students}</p>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card text-white bg-success mb-3">
            <div className="card-body">
              <h5 className="card-title">Total Subjects</h5>
              <p className="card-text">{analytics.total_subjects}</p>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card text-white bg-warning mb-3">
            <div className="card-body">
              <h5 className="card-title">Total Quizzes</h5>
              <p className="card-text">{analytics.total_quizzes}</p>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card text-white bg-danger mb-3">
            <div className="card-body">
              <h5 className="card-title">Active Quizzes</h5>
              <p className="card-text">{analytics.active_quizzes}</p>
            </div>
          </div>
        </div>
      </div>

      <div className="row mt-4">
        <div className="col-md-4">
          <h5>Subject Performance</h5>
          <canvas id="subjectPerformanceChart"></canvas>
        </div>
        <div className="col-md-4">
          <h5>Qualification Distribution</h5>
          <canvas id="qualificationDistributionChart"></canvas>
        </div>
        <div className="col-md-4">
          <h5>Performance Distribution</h5>
          <canvas id="performanceDistributionChart"></canvas>
        </div>
      </div>

      <h3 className="mt-5">User Performance</h3>
      <table className="table table-bordered mt-3">
        <thead className="table-dark">
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Qualification</th>
            <th>Average Score</th>
            <th>Quiz Attempts</th>
          </tr>
        </thead>
        <tbody>
          {analytics.user_performance.map((user, idx) => (
            <tr key={idx}>
              <td>{user.name}</td>
              <td>{user.email}</td>
              <td>{user.qualification}</td>
              <td>{user.avg_score}</td>
              <td>{user.quiz_attempts}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AdminDashboard;

