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

1. Clone the repository:
```
git clone https://github.com/Shahid6174/QBC.git
cd QBC
```

## 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

## 3. Install rest of the dependencies using poetry

```bash
pip install poetry
poetry install --no-root
```
## 4. Update .env variables

1.Create file .env
2.Copy Contents of .env.example to .env
3.Replace environment variables with your own credentials

## Run the Application

```bash
flask run
```

4. Configure email settings:
Open `website/__init__.py` and update the email configuration:
```python
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = ADMIN_EMAIL
    app.config['MAIL_PASSWORD'] = ADMIN_PASSWORD
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

```
Also Modify the function create_database so that you can add your own admin.
```python
def create_database(app):
    ......
            # Check if admin user already exists
            admin_user = User.query.filter_by(email="admin_qbc@gmail.com").first()
            if not admin_user:
                print("Creating default admin user...")
                admin = User(
                    email="qbc_admin@gmail.com",                       # also Modify the Email According to Your Choice
                    password=generate_password_hash("admin@123"),         #add Credentials that You want
                    full_name="Admin QBC",
                    is_admin=True,
                    is_verified=True
                )
                db.session.add(admin)
                db.session.commit()
                print("Admin user created!")
```

<div>
	<h1>Important Steps to Follow for the Above Functions Mail username Updation</h1>
		<li>1.Open the Link "https://myaccount.google.com/apppasswords" </li>
		<li>2.Login with your Email there</li>
		<li>3.Type Your App name and Mark Create App.</li>
		<li>4.Copy that code that appears on screen and add it as a MAIL_PASSWORD in .env file</li>
</div>


## 6. Configure db files
Run:
```
export FLASK_APP=website:create_app
flask db init
flask db migrate -m "study plans"
flask db upgrade
```

## 7. Run the application:
```bash
python app.py
```

## 8. Now, open link: `http://127.0.0.1:5000`


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



