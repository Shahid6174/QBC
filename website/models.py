from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime, date # Import date for consistency with dob field

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    qualification = db.Column(db.String(150))
    dob = db.Column(db.Date)
    is_admin = db.Column(db.Boolean, default=False) 
    is_verified = db.Column(db.Boolean, default=False)
    verification_code = db.Column(db.String(6), nullable=True)
    quizzes_attempted = db.relationship('Score', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    qualification = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    chapters = db.relationship('Chapter', backref='subject', lazy=True, cascade="all, delete-orphan")
    
    def __init__(self, name, qualification, description=""):
        self.name = name.lower()
        self.description = description
        self.qualification = qualification

    def __repr__(self):
        return f'<Subject {self.name}>'

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    quizzes = db.relationship('Quiz', backref='chapter', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Chapter {self.name}>'

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    date_of_quiz = db.Column(db.DateTime, default=func.now())
    time_duration = db.Column(db.Integer, nullable=False)
    remarks = db.Column(db.Text)
    questions = db.relationship('Question', backref='quiz', lazy=True, cascade="all, delete-orphan")
    scores = db.relationship('Score', backref='quiz', lazy=True, cascade="all, delete-orphan")
    published = db.Column(db.Boolean, default=False)  # New column for publish/unpublish

    def toggle_publish(self):
        # Removed db.session.commit() - commit should be handled in the view/service layer
        self.published = not self.published
    
    def __repr__(self):
        return f'<Quiz {self.id} - Chapter {self.chapter_id}>'

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_text = db.Column(db.String(500), nullable=False)
    option_a = db.Column(db.String(200), nullable=False)
    option_b = db.Column(db.String(200), nullable=False)
    option_c = db.Column(db.String(200), nullable=False)
    option_d = db.Column(db.String(200), nullable=False)
    correct_option = db.Column(db.String(1), nullable=False)  # Stores 'A', 'B', 'C', or 'D'
    
    def get_options(self):
        return {
            "A": self.option_a,
            "B": self.option_b,
            "C": self.option_c,
            "D": self.option_d
        }
    
    def __repr__(self):
        return f'<Question {self.id} - Quiz {self.quiz_id}>'

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    time_stamp_of_attempt = db.Column(db.DateTime, default=func.now())
    total_score = db.Column(db.Integer, nullable=False)
    answers = db.Column(db.Text, nullable=False) # Stores JSON string of user answers

    def __repr__(self):
        return f'<Score User:{self.user_id} Quiz:{self.quiz_id} Score:{self.total_score}>'

# --- New Models for Study Plans/Learning Paths ---

class StudyPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # Admin user who created it
    is_public = db.Column(db.Boolean, default=True) # Can any user enroll?
    # qualification_id = db.Column(db.String(50), nullable=True) # If plans are tied to specific levels, match User.qualification
    # Removed qualification_id as it might overcomplicate initial implementation without clear use case.
    # Can be added later if needed.

    # Relationships
    chapters = db.relationship('StudyPlanChapter', backref='study_plan', lazy=True, order_by='StudyPlanChapter.order', cascade="all, delete-orphan")
    user_progress = db.relationship('UserStudyPlanProgress', backref='study_plan', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<StudyPlan {self.name}>'

class StudyPlanChapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    study_plan_id = db.Column(db.Integer, db.ForeignKey('study_plan.id'), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    order = db.Column(db.Integer, nullable=False) # Order of the chapter within the study plan

    # Relationships
    chapter = db.relationship('Chapter', backref='study_plan_chapters', lazy=True)

    __table_args__ = (db.UniqueConstraint('study_plan_id', 'chapter_id', name='_study_plan_chapter_uc'),)

    def __repr__(self):
        return f'<StudyPlanChapter {self.study_plan_id} - Chapter:{self.chapter_id} Order:{self.order}>'

class UserStudyPlanProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    study_plan_id = db.Column(db.Integer, db.ForeignKey('study_plan.id'), nullable=False)
    
    # Track the current position within the plan
    # This will store the ID of the StudyPlanChapter the user is currently on or last completed
    current_study_plan_chapter_id = db.Column(db.Integer, db.ForeignKey('study_plan_chapter.id'), nullable=True)

    # Track overall progress
    completed_chapters_count = db.Column(db.Integer, default=0)
    total_quizzes_completed_in_plan = db.Column(db.Integer, default=0)
    
    status = db.Column(db.String(50), default='Not Started', nullable=False) # e.g., 'Not Started', 'In Progress', 'Completed'
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    completion_date = db.Column(db.DateTime, nullable=True)

    # Relationships
    user = db.relationship('User', backref='user_study_plan_progress', lazy=True) # Changed backref to avoid conflict with quizzes_attempted
    current_study_plan_chapter = db.relationship('StudyPlanChapter', foreign_keys=[current_study_plan_chapter_id], lazy=True)

    __table_args__ = (db.UniqueConstraint('user_id', 'study_plan_id', name='_user_study_plan_progress_uc'),)

    def __repr__(self):
        return f'<UserProgress User:{self.user_id} Plan:{self.study_plan_id} Status:{self.status}>'

