import { useEffect, useState } from "react";

const AdminAnalytics = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("/admin/analytics/data")
      .then((res) => res.json())
      .then((json) => {
        setData(json);
        loadCharts(json);
      })
      .catch((err) => console.error("Error fetching analytics data:", err));
  }, []);

  const loadCharts = (data) => {
    const Chart = window.Chart;

    new Chart(document.getElementById("subjectPerformanceChart"), {
      type: "bar",
      data: {
        labels: data.subject_performance.map((item) => item.subject),
        datasets: [
          {
            label: "Average Score",
            data: data.subject_performance.map((item) => item.avg_score),
            backgroundColor: "rgba(54, 162, 235, 0.5)",
          },
        ],
      },
      options: { maintainAspectRatio: false },
    });

    new Chart(document.getElementById("qualificationDistributionChart"), {
      type: "pie",
      data: {
        labels: data.qualification_distribution.map((item) => item.qualification),
        datasets: [
          {
            data: data.qualification_distribution.map((item) => item.count),
            backgroundColor: ["#ff6384", "#36a2eb", "#ffce56", "#4bc0c0", "#9966ff"],
          },
        ],
      },
      options: { maintainAspectRatio: false },
    });

    new Chart(document.getElementById("performanceDistributionChart"), {
      type: "bar",
      data: {
        labels: data.performance_distribution.map((item) => item.score),
        datasets: [
          {
            label: "Students Count",
            data: data.performance_distribution.map((item) => item.count),
            backgroundColor: "rgba(255, 99, 132, 0.5)",
          },
        ],
      },
      options: { maintainAspectRatio: false },
    });
  };

  return (
    <div className="container mt-4">
      <h2>Admin Analytics</h2>

      <div className="row">
        <div className="col-md-3">
          <div className="card text-white bg-primary mb-3">
            <div className="card-body">
              <h5 className="card-title">Total Students</h5>
              <p className="card-text">{data?.total_students || 0}</p>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card text-white bg-success mb-3">
            <div className="card-body">
              <h5 className="card-title">Total Subjects</h5>
              <p className="card-text">{data?.total_subjects || 0}</p>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card text-white bg-warning mb-3">
            <div className="card-body">
              <h5 className="card-title">Total Quizzes</h5>
              <p className="card-text">{data?.total_quizzes || 0}</p>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card text-white bg-danger mb-3">
            <div className="card-body">
              <h5 className="card-title">Active Quizzes</h5>
              <p className="card-text">{data?.active_quizzes || 0}</p>
            </div>
          </div>
        </div>
      </div>

      <div className="row">
        <div className="col-md-4">
          <h5>Subject Performance (Avg. Score per Subject)</h5>
          <canvas id="subjectPerformanceChart" style={{ maxHeight: "250px" }}></canvas>
        </div>
        <div className="col-md-4">
          <h5>Qualification Distribution of Students</h5>
          <canvas id="qualificationDistributionChart" style={{ maxHeight: "250px" }}></canvas>
        </div>
        <div className="col-md-4">
          <h5>Score Distribution Among Students</h5>
          <canvas id="performanceDistributionChart" style={{ maxHeight: "250px" }}></canvas>
        </div>
      </div>

      <h3 className="mt-5">User Performance Analytics</h3>
      <table className="table mt-4">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Qualification</th>
            <th>Average Score</th>
            <th>Quiz Attempts</th>
          </tr>
        </thead>
        <tbody>
          {data?.user_performance?.map((user, idx) => (
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

export default AdminAnalytics;
