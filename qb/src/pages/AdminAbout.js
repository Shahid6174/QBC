import React from "react";

const AdminAbout = () => {
  return (
    <div className="container-fluid px-4 mt-4">
      {/* App Introduction Section */}
      <section>
        <h2 className="text-primary">📚 About QBC App</h2>

        <div className="card my-4 shadow-sm">
          <div className="card-body">
            <p>
              <strong>QBC (Quiz-Based Competency)</strong> is an AI-powered learning platform designed to strengthen users' grasp on various subjects through interactive quizzes. It supports smart exam preparation with well-organized, structured assessments that are both subject-wise and chapter-wise.
            </p>
          </div>
        </div>
      </section>

      {/* Key Features Section */}
      <section>
        <div className="card my-4 shadow-sm">
          <div className="card-header bg-light text-primary">
            <h4 className="mb-0">🚀 Key Features</h4>
          </div>
          <div className="card-body">
            <ul className="mb-0">
              <li><strong>📘 Subject-Wise Quizzes:</strong> Build strong fundamentals by focusing on subject-specific questions.</li>
              <li><strong>📗 Chapter-Wise Quizzes:</strong> Deep-dive into chapters to solidify conceptual understanding.</li>
              <li><strong>🔍 Question-ID Search:</strong> Instantly search and review specific questions by their ID.</li>
              <li><strong>📄 Cheat Sheet:</strong> Quick revision guides curated for every chapter/topic.</li>
              <li><strong>📈 Performance Analytics:</strong> Track your accuracy, speed, and topic-wise scores over time.</li>
              <li><strong>📊 Real-Time Progress:</strong> Monitor growth and compare performance with peers.</li>
            </ul>
          </div>
        </div>
      </section>

      {/* Why QBC Section */}
      <section>
        <div className="card my-4 shadow-sm">
          <div className="card-header bg-light text-primary">
            <h4 className="mb-0">🎯 Why Choose QBC?</h4>
          </div>
          <div className="card-body">
            <p>
              QBC offers a more intuitive and effective learning experience by converting complex subjects into short, engaging quizzes. It empowers learners to self-assess, revise faster, and grow smarter.
            </p>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section>
        <div className="card my-4 shadow-sm">
          <div className="card-header bg-light text-primary">
            <h4 className="mb-0">📬 Contact Us</h4>
          </div>
          <div className="card-body">
            <p>
              For queries, support, or feedback, feel free to reach out at:{" "}
              <a
                href="mailto:qbc_admin@fastmail.com"
                className="text-decoration-none"
                rel="noopener noreferrer"
              >
                qbc_admin@fastmail.com
              </a>
            </p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default AdminAbout;
