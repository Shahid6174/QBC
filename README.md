<h1 align="center">🌟 QBC - Quiz Based Challenge 🌟</h1>

<p align="center">
  <img src="website/static/images/QBC_logo.png" alt="QBC Logo" height="188" />
</p>

---

## ⭐ Overview

**QBC (Quiz-Based Challenge)** is a web app designed to boost learning through structured, subject- and chapter-wise quizzes. It enables effective preparation with analytics, an anti-cheat environment, and both admin and user features.

---

## ⭐ Features

### 👨‍🎓 For Users

- **Subject-Wise Quizzes** – Practice by subjects to strengthen your base.
- **Chapter-Wise Quizzes** – Focused learning on individual chapters.
- **Performance Analytics** – Know your strengths and weak spots.
- **Real-Time Tracking** – Monitor your quiz journey.
- **Anti-Cheat Environment** – Fullscreen mode and tab-switch detection.

### 🛠️ For Administrators

- **Content Management** – Create/manage subjects, chapters, quizzes, and questions.
- **Quiz Publishing Controls** – Decide availability timings.
- **Student Analytics** – Monitor student performance and trends.
- **User Management** – Track user verification and activity.

---

## 🧰 Tech Stack

- **Backend**: Python Flask  
- **Database**: SQLAlchemy + SQLite  
- **Authentication**: Flask-Login  
- **Email**: Flask-Mailman  
- **Frontend**: Bootstrap 5, HTML, CSS, JS  
- **Analytics**: Chart.js  

---

## 🚀 Getting Started

### 1. Clone the Repository

git clone https://github.com/Shahid6174/QBC.git
cd QBC


### 2. Create and Activate Virtual Environment

python -m venv venv
# Activate on Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate


### 3. Install Dependencies using poetry

pip install poetry
poetry install --no-root


### 4. Update .env variables

1. Create file .env
2. cp .env.example .env
3. Update the variables in .env:
SECRET_KEY='your_secret_key'
ADMIN_EMAIL='your_admin_email'
ADMIN_PASSWORD='your_admin_password'
SQLITE_DB='qbc.db'

---

## 📧 Email Setup (Optional)
To avoid issues:

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = ADMIN_EMAIL
app.config['MAIL_PASSWORD'] = ADMIN_PASSWORD
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

---

## 🔐 Setup App Password for Gmail
Go to: App Passwords

Log in → Choose "Mail" as app → Get app password.

Add it in your .env as MAIL_PASSWORD.

---

## 👨‍💻 Create Default Admin User
In create_database(app) method:

admin = User(
    email="your_email",
    password=generate_password_hash("your_password"),
    full_name="Admin QBC",
    is_admin=True,
    is_verified=True
)

---

## 🧱 Database Setup

export FLASK_APP=website:create_app  # On Windows: set FLASK_APP=website:create_app
flask db init
flask db migrate -m "initial migration"
flask db upgrade

---

## Run the Application

python app.py

Then visit: http://127.0.0.1:5000

<h2>📊 Database Models</h2>
<ul>
  <li><strong>User</strong>: Stores user information, authentication details, and verification status</li>
  <li><strong>Subject</strong>: Represents a subject area with multiple chapters.</li>
  <li><strong>Chapter</strong>: Represents a chapter within a subject with multiple quizzes</li>
  <li><strong>Quiz</strong>: Contains questions and settings for a specific quiz</li>
  <li><strong>Question</strong>: Stores question text, options, and correct answer</li>
  <li><strong>Score</strong>: Shows User Quizz Score Analysis in Proper Diagrams</li>
</ul>

<h2>🧾 Usage Guide</h2>

<h3>Admin:</h3>
<ul>
  <li>Login with Admin Credentials so that they can add Tests.</li>
  <li>Create new subjects with descriptions and qualification levels.</li>
  <li>View and delete existing subjects.</li>
  <li>Manage Subjects and Chapters.</li>
  <li>Create quizzes for specific chapters.</li>
  <li>Set time duration and remarks.</li>
</ul>

<h3>User:</h3>
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

## 🧠 Contributing

1. Fork the repo

2. Create a new branch:

git checkout -b your-name-feature

3. Make your changes, commit:

4. git commit -m "Added feature xyz"

5. Push & create a Pull Request 🚀

## ⭐ Future Add-Ons

<pre>🎯 1. Leaderboard
Show top scorers per subject/quiz using a sortable table.

🧠 2. Timed Quizzes
Add countdown timer on quiz page. Auto-submit on timeout using JavaScript.

🎲 3. Question Shuffling
Randomize order of questions and options per user using Python + JS.

📩 4. Send Score via Email
Once quiz is submitted, send their result via email using Flask-Mailman (optional toggle).

💬 5. Discussion or Feedback for Each Quiz
Let users comment or give feedback after a quiz.</pre>


