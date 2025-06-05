const AdminAbout = () => {
  return (
    <div className="container-fluid px-4 mt-4">
      <h2 className="text-primary">About QBC App</h2>

      <div className="card my-4 shadow-sm">
        <div className="card-body">
          <p>
            <strong>QBC (Quiz-Based Competency)</strong> is a smart learning platform designed to help users strengthen their understanding of various subjects through structured quizzes. It enables effective exam preparation by organizing quizzes <strong>subject-wise and chapter-wise</strong> for better learning outcomes.
          </p>
        </div>
      </div>

      <div className="card my-4 shadow-sm">
        <div className="card-header bg-light text-primary">
          <h4 className="mb-0">Key Features</h4>
        </div>
        <div className="card-body">
          <ul>
            <li><strong>Subject-Wise Quizzes:</strong> Practice questions categorized by subjects to build a strong foundation.</li>
            <li><strong>Chapter-Wise Quizzes:</strong> Focus on individual chapters to master concepts step by step.</li>
            <li><strong>Question-ID Wise Search:</strong> Quickly locate and review specific questions.</li>
            <li><strong>Cheat Sheet:</strong> A curated collection of key concepts for quick revision.</li>
            <li><strong>Performance Analytics:</strong> Get insights into strengths and areas for improvement.</li>
            <li><strong>Real-Time Tracking:</strong> Monitor progress and compete with peers.</li>
          </ul>
        </div>
      </div>

      <div className="card my-4 shadow-sm">
        <div className="card-header bg-light text-primary">
          <h4 className="mb-0">Why QBC?</h4>
        </div>
        <div className="card-body">
          <p>QBC is designed to provide an interactive and efficient way of learning by breaking down complex topics into structured quizzes, making self-assessment easier and more effective.</p>
        </div>
      </div>

      <div className="card my-4 shadow-sm">
        <div className="card-header bg-light text-primary">
          <h4 className="mb-0">Contact Us</h4>
        </div>
        <div className="card-body">
          <p>
            For support or feedback, reach us at:{" "}
            <a href="mailto:qbc_admin@fastmail.com">qbc_admin@fastmail.com</a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default AdminAbout;
