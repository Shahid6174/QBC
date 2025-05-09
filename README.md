<h1>QBC - Quiz Based Competency</h1>

<p align="center">
  <img src="website/static/images/QBC_logo.png" alt="QBC Logo" />
</p>
<h2>Overview</h2>
<p>QBC (Quiz-Based Competency) is a comprehensive web application designed to help users strengthen their understanding of various subjects through structured quizzes. It enables effective exam preparation by organizing quizzes subject-wise and chapter-wise for better learning outcomes.</p>

## Features

### For Users
- **Subject-Wise Quizzes**: Practice questions categorized by subjects to build a strong foundation
- **Chapter-Wise Quizzes**: Focus on individual chapters to master concepts step by step
- **Performance Analytics**: Get insights into strengths and areas for improvement
- **Real-Time Tracking**: Monitor progress with detailed performance metrics
- **Secure Quiz Environment**: Anti-cheating measures including full-screen mode enforcement and tab-switching detection

### For Administrators
- **Complete Content Management**: Create and manage subjects, chapters, quizzes, and questions
- **Quiz Publishing Control**: Decide when quizzes are available to users
- **Comprehensive Analytics**: Monitor student performance, subject popularity, and qualification distribution
- **User Management**: Track user verification and activity

## Technical Stack

- **Backend**: Python Flask
- **Database**: SQLAlchemy with SQLite
- **Authentication**: Flask-Login
- **Email Services**: Flask-Mailman
- **Frontend**: Bootstrap 5, HTML, CSS, JavaScript
- **Charts**: Chart.js for analytics visualization

## Installation and Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Installation Steps

1. Clone the repository:
```
git clone [https://github.com/yourusername/QBC.git](https://github.com/Shahid6174/QBC.git)
cd QBC
```

```plaintext

2. Create and activate a virtual environment:
```

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

```plaintext

3. Install dependencies:
```

pip install -r requirements.txt

```plaintext

4. Configure email settings:
Open `website/__init__.py` and update the email configuration:
```python
app.config['MAIL_SERVER'] = 'your_mail_server'
app.config['MAIL_PORT'] = your_mail_port
app.config['MAIL_USERNAME'] = 'your_email'
app.config['MAIL_PASSWORD'] = 'your_password'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
```

5. Run the application:

```plaintext
python app.py
```


6. Access the application at `http://127.0.0.1:5000`


## Project Structure

```
QBC/
├── app.py                  # Application entry point
├── instance/               # Database files
├── website/                # Main application package
│   ├── **init**.py         # Application factory and configuration
│   ├── auth.py             # Authentication routes
│   ├── decorators.py       # Custom decorators for route protection
│   ├── models.py           # Database models
│   ├── views.py            # Main application routes
│   ├── static/             # Static files (CSS, JS, images)
│   └── templates/          # HTML templates
│       ├── admin_*.html    # Admin interface templates
│       ├── user_*.html     # User interface templates
│       └── *.html          # Shared templates
└── README.md               # Project documentation
```

## Database Models

- **User**: Stores user information, authentication details, and verification status
- **Subject**: Represents a subject area with multiple chapters
- **Chapter**: Represents a chapter within a subject with multiple quizzes
- **Quiz**: Contains questions and settings for a specific quiz
- **Question**: Stores question text, options, and correct answer
- **Score**: Records user quiz attempts and performance


## Usage Guide

### Admin Guide

1. **Login**: Use the admin credentials to access the admin dashboard

1. Default admin: [qbc_admin@fastmail.com](mailto:qbc_admin@fastmail.com) / admin@123



2. **Subject Management**:

1. Create new subjects with descriptions and qualification levels
2. View and delete existing subjects



3. **Chapter Management**:

1. Add chapters to subjects
2. View and delete chapters



4. **Quiz Management**:

1. Create quizzes for specific chapters
2. Set time duration and remarks
3. Publish/unpublish quizzes to control user access



5. **Question Management**:

1. Add multiple-choice questions to quizzes
2. Edit and delete questions
3. Set correct answers



6. **Analytics**:

1. View comprehensive statistics about users, subjects, and performance
2. Monitor qualification distribution and subject performance





### User Guide

1. **Registration and Verification**:

1. Sign up with email, personal details, and qualification
2. Verify email using the verification code sent to your email



2. **Login**:

1. Access the user dashboard with verified credentials



3. **Taking Quizzes**:

1. Browse available quizzes based on your qualification
2. Start a quiz and answer questions within the time limit
3. Submit answers for evaluation



4. **Performance Review**:

1. View your score immediately after quiz completion
2. Access detailed performance analytics
3. Track progress over time with visual charts





## Security Features

- **Email Verification**: Ensures valid user registration
- **Password Hashing**: Secures user passwords in the database
- **Role-Based Access Control**: Separates admin and user functionalities
- **Quiz Security Measures**:

- Full-screen enforcement during quizzes
- Tab-switching detection
- Time limit enforcement
- Prevention of multiple attempts





## Development and Customization

### Adding New Features

1. **New Question Types**:

1. Modify the Question model in `models.py`
2. Update the quiz templates to support new question formats



2. **Additional Analytics**:

1. Extend the analytics routes in `views.py`
2. Add new chart visualizations in the templates





### Customizing Appearance

1. **Theme Colors**:

1. Modify the CSS in the template files
2. Update the Bootstrap theme variables



2. **Layout Changes**:

1. Edit the base templates (`admin_base.html` and `user_base.html`)





## Future Enhancements

- **Advanced Question Types**: Support for image-based questions, coding challenges
- **Discussion Forums**: Allow users to discuss questions and solutions
- **Leaderboards**: Implement competitive elements with rankings
- **Mobile App**: Develop a companion mobile application
- **Content Import/Export**: Support for importing questions from CSV/Excel
- **AI-Powered Recommendations**: Suggest quizzes based on user performance


## Troubleshooting

### Common Issues

1. **Email Verification Not Working**:

1. Check email configuration in `__init__.py`
2. Ensure your email provider allows SMTP access



2. **Database Errors**:

1. Delete the database file in the instance folder and restart the application
2. Run database migrations if schema changes are made



3. **Quiz Submission Issues**:

1. Check browser compatibility (modern browsers recommended)
2. Ensure stable internet connection during quiz attempts





## Contact and Support

For support or feedback, reach us at: [qbc_admin@fastmail.com](mailto:qbc_admin@fastmail.com)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
