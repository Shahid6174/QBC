# QBC (Quiz Based Challenge) - Installation & Usage Guide

This comprehensive guide will walk you through setting up and using the QBC application on your local machine. QBC is a web application designed to help users strengthen their understanding of various subjects through structured quizzes.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [Project Structure](#project-structure)
6. [Features Overview](#features-overview)
7. [User Guide](#user-guide)
8. [Admin Guide](#admin-guide)
9. [Common Issues & Troubleshooting](#common-issues--troubleshooting)

## Prerequisites

Before starting the installation, ensure you have the following installed on your system:

- Python 3.8 or higher
- pip (Python package installer)
- Git
- A Gmail account (for email verification functionality)

## Installation

## 1. Clone the Repository

```bash
git clone https://github.com/Shahid6174/QBC.git
cd QBC
```

## 2. Create a Virtual Environment

This isolates the project dependencies from your global Python installation:

```bash
python -m venv venv
```

Activate the virtual environment:

- **Linux/macOS**:

  ```bash
  source venv/bin/activate
  ```

- **Windows**:
  ```bash
  venv\Scripts\activate
  ```

You should see `(venv)` at the beginning of your command prompt, indicating that the virtual environment is active.

## 3. Install Dependencies

You can install dependencies using either Poetry (recommended) or pip:

#### Using Poetry (Recommended):

```bash
pip install poetry
poetry install --no-root
```

#### Using pip (Alternative):

```bash
pip install -r requirements.txt
```

## 4. Configuration

### 4.1 Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Open the `.env` file and update the following variables:

```
SECRET_KEY=your_secret_key_here
ADMIN_EMAIL=your_gmail_address@gmail.com
ADMIN_PASSWORD=your_app_password_here
```

### 4.2 Setting Up Gmail App Password

For the email verification functionality to work, you need to:

1. Go to [Google Account App Passwords](https://myaccount.google.com/apppasswords)
2. Sign in with your Gmail account
3. Select "App" and choose "Other (Custom name)"
4. Enter "QBC" as the app name and click "Create"
5. Copy the 16-character password that appears
6. Paste this password as the value for `ADMIN_PASSWORD` in your `.env` file

### 4.3 Email Configuration

Open `website/__init__.py` and ensure the email configuration matches your settings:

```python
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = ADMIN_EMAIL
app.config['MAIL_PASSWORD'] = ADMIN_PASSWORD
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
```

### 4.4 Admin Account Setup

By default, an admin account is created with:

- Email: qbc_admin@gmail.com
- Password: admin@123

To customize the admin account, modify the `create_database` function in `website/__init__.py` before running the application:

```python
def create_database(app):
    # ...existing code...
    # Check if admin user already exists
    admin_user = User.query.filter_by(email="admin_qbc@gmail.com").first()
    if not admin_user:
        print("Creating default admin user...")
        admin = User(
            email="qbc_admin@gmail.com",                       # Modify the Email According to Your Choice
            password=generate_password_hash("admin@123"),      # Add Credentials that You want
            full_name="Admin QBC",
            is_admin=True,
            is_verified=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created!")
    # ...existing code...
```

### 4.5 Database Setup

Initialize the database:

```bash
export FLASK_APP=website:create_app
flask db init
flask db migrate -m "study plans"
flask db upgrade
```

## 5. Running the Application

### 5.1 Development Mode

```bash
python app.py
```

The application will be accessible at `http://127.0.0.1:5000`

Alternatively, you can use Flask's built-in development server:

```bash
flask run
```

### 5.2 Production Mode (using Gunicorn)

For production deployment, it's recommended to use Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 "website:create_app()"
```

## Project Structure

The QBC project follows a modular structure:

- `website/` - Main application package

  - `__init__.py` - Application factory and configuration
  - `auth.py` - Authentication routes and logic
  - `models.py` - Database models
  - `views.py` - Main application routes
  - `decorators.py` - Custom Flask decorators
  - `templates/` - HTML templates
  - `static/` - Static assets (CSS, JS, images)

- `app.py` - Application entry point
- `docs/` - Documentation files
- `instance/` - Instance-specific data (database file)

## Features Overview

### User Features

- **Subject-Wise Quizzes**: Practice questions categorized by subjects
- **Chapter-Wise Quizzes**: Focus on individual chapters
- **Performance Analytics**: Get insights about strengths and improvement areas
- **Real-Time Tracking**: Monitor progress with detailed statistics
- **Anti-Cheat Quiz Environment**: Measures to prevent cheating

### Admin Features

- **Content Management**: Create and manage subjects, chapters, quizzes, and questions
- **Quiz Publishing Control**: Control when quizzes are available
- **Comprehensive Analytics**: Monitor student performance and subject popularity
- **User Management**: Track user verification and activity

## User Guide

### Registration & Login

1. Open the application in your browser at `http://127.0.0.1:5000`
2. Click "Sign Up" to create a new account
3. Verify your email by clicking the link sent to your inbox
4. Log in with your credentials

### Taking Quizzes

1. Browse available subjects and chapters
2. Select a quiz to attempt
3. Read the instructions and start the quiz
4. Answer questions within the time limit
5. Submit your answers for evaluation
6. View your results and performance analytics

## Admin Guide

### Accessing Admin Panel

1. Log in with admin credentials
2. You'll be automatically redirected to the admin dashboard

### Managing Content

1. **Adding Subjects**:

   - Go to Subjects section
   - Click "Add Subject"
   - Fill in the subject details and save

2. **Adding Chapters**:

   - Select a subject
   - Click "Add Chapter"
   - Enter chapter details and save

3. **Creating Quizzes**:
   - Go to a specific chapter
   - Click "Add Quiz"
   - Set quiz parameters (time limit, description)
   - Add questions with multiple-choice options
   - Set correct answers
   - Publish the quiz

### Monitoring Analytics

1. Navigate to the Analytics section
2. View comprehensive statistics about:
   - User performance
   - Subject popularity
   - Quiz completion rates
   - Qualification distribution

## Common Issues & Troubleshooting

### Email Verification Not Working

**Issue**: Verification emails are not being sent or received.

**Solution**:

1. Check that your Gmail app password is correct in the `.env` file
2. Ensure less secure app access is enabled in your Google account
3. Verify that your internet connection is stable

### Database Errors

**Issue**: "No such table" errors when accessing certain features.

**Solution**:

1. Make sure you've run the database migration commands
2. Check that the `instance` directory contains the `qbc.db` file
3. If the database is corrupted, delete the file and re-run migrations

### Authentication Issues

**Issue**: Unable to log in despite correct credentials.

**Solution**:

1. Check if your account email is verified
2. Reset your password if necessary
3. Clear browser cookies and cache

### Application Not Starting

**Issue**: Error when running `python app.py`

**Solution**:

1. Ensure your virtual environment is activated
2. Verify all dependencies are installed
3. Check for syntax errors in your `.env` file
4. Make sure no other application is using port 5000

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/getting-started/introduction/)

---

For more detailed information or to report issues, please visit the [GitHub repository](https://github.com/Shahid6174/QBC).
