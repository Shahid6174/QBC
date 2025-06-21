<h1 align="center">🌟QBC - Quiz Based Challenge🌟</h1>

<p align="center">
  <img src="website/static/images/QBC_logo.png" alt="QBC Logo" height="188" />
</p>
<h2>⭐Overview</h2>
<p>QBC (Quiz-Based Challenge) is a Web App designed to help users strengthen their understanding of various subjects through structured quizzes. It enables effective exam preparation by organizing quizzes subject-wise and chapter-wise for better learning outcomes.Here Admins can upload the Quizzes and the users can give the Quizzes and get their scores too</p>

<h2>⭐Features</h2>

<h3>For Users</h3>
<ul>
  <li><strong>Subject-Wise Quizzes</strong>: Practice questions categorized by subjects to build a strong foundation.</li>
  <li><strong>Chapter-Wise Quizzes</strong>: Focus on individual chapters to master concepts step by step.</li>
  <li><strong>Performance Analytics</strong>: Get insights about strengths and areas for improvement.</li>
  <li><strong>Real-Time Tracking</strong>: Monitor progress with details.</li>
  <li><strong>Anti Cheat Quiz Environment</strong>: Anti-cheating measures including full-screen mode enforcement and tab-switching detection.</li>
</ul>

<h3>For Administrators</h3>
<ul>
  <li><strong>Complete Content Management</strong>: Create and manage subjects, chapters, quizzes, and questions.</li>
  <li><strong>Quiz Publishing Control</strong>: Decide when quizzes are available to users.</li>
  <li><strong>Comprehensive Analytics</strong>: Monitor student performance, subject popularity, and qualification distribution.</li>
  <li><strong>User Management</strong>: Track user verification and activity.</li>
</ul>

<h2>⭐Technical Stack</h2>
<ul>
  <li><strong>Backend</strong>: Python Flask</li>
  <li><strong>Database</strong>: SQLAlchemy with SQLite</li>
  <li><strong>Authentication</strong>: Flask-Login</li>
  <li><strong>Email Services</strong>: Flask-Mailman</li>
  <li><strong>Frontend</strong>: Bootstrap 5, HTML, CSS, JavaScript</li>
  <li><strong>Charts</strong>: Chart.js for analytics visualization</li>
</ul>

<h2>⭐Installation and Setup</h2>

For detailed installation instructions and usage guide, please check the [Installation & Usage Guide](docs/installation.md).

Below is a quick setup summary:

1. Clone the repository and set up the environment:

```bash
git clone https://github.com/Shahid6174/QBC.git
cd QBC
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install poetry
poetry install --no-root
```

2. Configure your environment:

   - Create a `.env` file from `.env.example`
   - Set up Gmail app password for email functionality
   - Initialize the database

3. Run the application:

```bash
python app.py
```

Access the application at: `http://127.0.0.1:5000`

<h2>⭐Databases</h2>
<ul>
  <li><strong>User</strong>: Stores user information, authentication details, and verification status</li>
  <li><strong>Subject</strong>: Represents a subject area with multiple chapters.</li>
  <li><strong>Chapter</strong>: Represents a chapter within a subject with multiple quizzes</li>
  <li><strong>Quiz</strong>: Contains questions and settings for a specific quiz</li>
  <li><strong>Question</strong>: Stores question text, options, and correct answer</li>
  <li><strong>Score</strong>: Shows User Quizz Score Analysis in Proper Diagrams</li>
</ul>

<h2>⭐ Usage Guide</h2>

<h3>🧾 Admin Guide</h3>
<ul>
  <li>Login with Admin Credentials so that they can add Tests.</li>
  <li>Create new subjects with descriptions and qualification levels.</li>
  <li>View and delete existing subjects.</li>
  <li>Manage Subjects and Chapters.</li>
  <li>Create quizzes for specific chapters.</li>
  <li>Set time duration and remarks.</li>
</ul>

<h3>🧾 User Guide</h3>
<ul>
  <li>Sign up with email and password and verify your email.</li>
  <li>Browse available quizzes based on your qualification.</li>
  <li>Start a quiz and answer questions within the time limit.</li>
  <li>Submit answers for evaluation.</li>
</ul>

<h2>✨ Some Features of This App</h2>
<ul>
  <li>Add multiple-choice questions to quizzes.</li>
  <li>Edit and delete questions.</li>
  <li>Set correct answers.</li>
  <li>View comprehensive statistics about users, subjects, and performance.</li>
  <li>Monitor qualification distribution and subject performance.</li>
</ul>

<h1>📱Project Screenshots</h1>
<h2>User Module</h2>

<h3>User Dashboard</h3>

![image](https://github.com/user-attachments/assets/49e883e3-61ab-44fc-b674-91d886c36c0c)

<h3>User Analytics</h3>

![image](https://github.com/user-attachments/assets/e2633113-0b0f-42ca-b739-3d99cc504720)

<h3>User Quiz Mode</h3>

![image](https://github.com/user-attachments/assets/efcb9cee-529f-4a46-aa63-9f2f80b274ce)

<h2>Admin Module</h2>
<h3>Admin Dashboard</h3>

![image](https://github.com/user-attachments/assets/4eaa6ddb-41e8-49a2-b470-111dab580d13)

<h3>Admin Analytics</h3>

![image](https://github.com/user-attachments/assets/e216f10d-7701-43ad-8f31-45cb4c6918c1)

<h3>Admin Subjects Panel</h3>

![image](https://github.com/user-attachments/assets/524afd31-bf70-472e-bfe8-19015ac7e8ae)

<h3>Subject's Quizzes Page</h3>

![image](https://github.com/user-attachments/assets/08fc819e-5e9a-49b0-9e76-2c3a5ae4599f)

<h3>Quiz Editor</h3>

![image](https://github.com/user-attachments/assets/3370ff8f-b273-47b3-925b-d32e90eca157)
