from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, jsonify
from sqlalchemy import func
import json
from . import db
from .models import Subject, Chapter, Quiz, Question, Score, User
from .decorators import admin_required, user_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

views = Blueprint("views", __name__)

@views.route("/", methods=["GET"])
def landing_page():
    return render_template("landing_page.html", user=current_user)

@views.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    if current_user.is_admin:
        return redirect(url_for("views.admin_dashboard"))
    return redirect(url_for("views.user_dashboard"))

#user admin page
@views.route("/user-about")
@login_required
def user_about():
    return render_template("user_about.html")

#admin about page
@views.route("/admin-about")
@login_required
@admin_required
def admin_about():
    return render_template("admin_about.html")

@views.route("/admin")
@login_required
@admin_required
def admin_dashboard():
    subjects = Subject.query.all()
    return render_template("admin_dashboard.html", subjects=subjects)

@views.route("/admin/delete_subject/<int:subject_id>", methods=["POST"])
@login_required
@admin_required
def delete_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    db.session.delete(subject)
    db.session.commit()
    flash("Subject deleted successfully.", "success")
    return redirect(url_for("views.admin_dashboard"))

@views.route("/admin/delete_chapter/<int:chapter_id>", methods=["POST"])
@login_required
@admin_required
def delete_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    subject_id = chapter.subject_id  # Save subject_id before deletion
    db.session.delete(chapter)
    db.session.commit()
    flash("Chapter deleted successfully.", "success")
    return redirect(url_for("views.view_chapters", subject_id=subject_id))

@views.route("/admin/add_subject", methods=["GET", "POST"])
@login_required
@admin_required
def add_subject():
    if request.method == "POST":
        name = request.form.get("name", "").strip().lower()  # Convert to lowercase
        description = request.form.get("description", "").strip()
        qualification = request.form.get("qualification", "").strip()

        # Check for case-insensitive duplicate
        if Subject.query.filter(db.func.lower(Subject.name) == name).first():
            flash("Subject already exists!", "error")
        else:
            new_subject = Subject(name=name, description=description, qualification=qualification)
            db.session.add(new_subject)
            db.session.commit()
            flash("Subject added successfully!", "success")

        return redirect(url_for("views.admin_dashboard"))

    return render_template("add_subject.html")

@views.route("/admin/chapters/<int:subject_id>")
@login_required
@admin_required
def view_chapters(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    
    return render_template("view_chapters.html", subject=subject, chapters=chapters)

@views.route("/admin/add_chapter/<int:subject_id>", methods=["GET", "POST"])
@login_required
@admin_required
def add_chapter(subject_id):
    subject = Subject.query.get_or_404(subject_id)

    if request.method == "POST":
        name = request.form.get("name").strip()
        description = request.form.get("description").strip()

        new_chapter = Chapter(name=name, description=description, subject_id=subject.id)
        db.session.add(new_chapter)
        db.session.commit()
        flash("Chapter added successfully!", "success")
        return redirect(url_for("views.view_chapters", subject_id=subject.id))  

    return render_template("add_chapter.html", subject=subject)

@views.route("/admin/quiz/<int:quiz_id>", methods=["GET", "POST"])
@login_required
@admin_required
def view_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz.id).all()

    if request.method == "POST":
        question_text = request.form.get("question_text")  # Ensure this matches the model field name
        option_a = request.form.get("option_a")
        option_b = request.form.get("option_b")
        option_c = request.form.get("option_c")
        option_d = request.form.get("option_d")
        correct_option = request.form.get("correct_option")

        new_question = Question(
            quiz_id=quiz.id,
            question_text=question_text,  # Use the correct column name
            option_a=option_a,
            option_b=option_b,
            option_c=option_c,
            option_d=option_d,
            correct_option=correct_option,
        )
        db.session.add(new_question)
        db.session.commit()
        flash("Question added successfully!", "success")
        return redirect(url_for("views.view_quiz", quiz_id=quiz.id))

    return render_template("view_quiz.html", quiz=quiz, questions=questions)

@views.route("/admin/add_quiz/<int:chapter_id>", methods=["GET", "POST"])
@login_required
@admin_required
def add_quiz(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)

    if request.method == "POST":
        try:
            time_duration = int(request.form.get("time_duration"))
            remarks = request.form.get("remarks").strip()

            new_quiz = Quiz(chapter_id=chapter.id, time_duration=time_duration, remarks=remarks)
            db.session.add(new_quiz)
            db.session.commit()
            flash("Quiz added successfully!", "success")
            return redirect(url_for("views.view_quizzes", chapter_id=chapter.id))
        except ValueError:
            flash("Time duration must be a valid number!", "error")

    return render_template("add_quiz.html", chapter=chapter)

@views.route("/admin/view_quizzes/<int:chapter_id>")
@login_required
@admin_required
def view_quizzes(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    quizzes = Quiz.query.filter_by(chapter_id=chapter.id).all()
    return render_template("view_quizzes.html", chapter=chapter, quizzes=quizzes)

@views.route("/admin/delete_quiz/<int:quiz_id>", methods=["POST"])
@login_required
@admin_required
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    chapter_id = quiz.chapter_id  # Store chapter ID before deleting
    db.session.delete(quiz)
    db.session.commit()
    flash("Quiz deleted successfully.", "success")
    return redirect(url_for("views.view_quizzes", chapter_id=chapter_id))

@views.route("/admin/edit_question/<int:quiz_id>/<int:question_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_question(quiz_id, question_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    question = Question.query.get_or_404(question_id)

    if request.method == "POST":
        question.question_text = request.form["question_text"]
        question.option_a = request.form["option_a"]
        question.option_b = request.form["option_b"]
        question.option_c = request.form["option_c"]
        question.option_d = request.form["option_d"]
        question.correct_option = request.form["correct_option"]
        db.session.commit()
        flash("Question updated successfully!", "success")
        return redirect(url_for("views.view_quiz", quiz_id=quiz.id))

    return render_template("edit_question.html", quiz=quiz, question=question)

@views.route("/admin/delete_question/<int:question_id>", methods=["POST"])
@login_required
@admin_required
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    quiz_id = question.quiz_id  # Store quiz ID before deleting
    db.session.delete(question)
    db.session.commit()
    flash("Question deleted successfully!", "danger")
    return redirect(url_for("views.view_quiz", quiz_id=quiz_id))

@views.route("/admin/analytics")
@login_required
@admin_required
def admin_analytics():
    return render_template('admin_analytics.html')

@views.route('/admin/analytics/data')
@login_required  # If applicable
@admin_required
def admin_analytics_data():
        # Exclude admins from student count
    total_students = User.query.filter_by(is_admin=False).count()
    
    total_subjects = Subject.query.count()
    total_quizzes = Quiz.query.count()
    active_quizzes = Quiz.query.filter_by(published=True).count()

    # Subject Performance (Average Scores Per Subject, Excluding Admins)
    subject_performance = db.session.query(
        Subject.name, func.coalesce(func.avg(Score.total_score), 0)
    ).join(Chapter).join(Quiz).outerjoin(Score).join(User).filter(User.is_admin == False) \
    .group_by(Subject.id).all()

    # Convert to dictionary format
    subject_performance_data = [
        {"subject": subject, "avg_score": avg_score}
        for subject, avg_score in subject_performance
    ]

    # Qualification Distribution (Excluding Admins)
    qualification_distribution = db.session.query(
        User.qualification, func.count(User.id)
    ).filter(User.is_admin == False).group_by(User.qualification).all()

    qualification_distribution_data = [
        {"qualification": qualification, "count": count}
        for qualification, count in qualification_distribution
    ]

    # Performance Distribution (Excluding Admins)
    performance_distribution = db.session.query(
        Score.total_score, func.count(Score.id)
    ).join(User).filter(User.is_admin == False).group_by(Score.total_score).all()

    performance_distribution_data = [
        {"score": score, "count": count} for score, count in performance_distribution
    ]

    return jsonify({
        "total_students": total_students,
        "total_subjects": total_subjects,
        "total_quizzes": total_quizzes,
        "active_quizzes": active_quizzes,
        "subject_performance": subject_performance_data,
        "qualification_distribution": qualification_distribution_data,
        "performance_distribution": performance_distribution_data
    })

@admin_required
@login_required
@views.route('/admin/quiz/<int:quiz_id>/toggle_publish', methods=['POST'])
def toggle_publish(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    quiz.published = not quiz.published
    db.session.commit()
    return redirect(request.referrer)


@views.route("/user")
@login_required
@user_required
def user_dashboard():
    quizzes = (
        db.session.query(
            Quiz.id,
            Chapter.name.label("chapter_name"),
            Subject.name.label("subject_name"),
            db.func.count(Question.id).label("total_questions"),
            db.func.coalesce(
                db.session.query(Score.total_score)
                .filter(Score.user_id == current_user.id, Score.quiz_id == Quiz.id)
                .order_by(Score.time_stamp_of_attempt.desc())
                .limit(1)
                .scalar_subquery(),
                None
            ).label("latest_score")
        )
        .join(Chapter, Quiz.chapter_id == Chapter.id)
        .join(Subject, Chapter.subject_id == Subject.id)
        .outerjoin(Question, Question.quiz_id == Quiz.id)
        .filter(Quiz.published == True)  # Ensure only published quizzes are fetched
        .group_by(Quiz.id, Chapter.name, Subject.name)
        .all()
    )

    return render_template("user_dashboard.html", quizzes=quizzes)


@views.route("/user/quiz/<int:quiz_id>", methods=["GET"])
@login_required
@user_required
def start_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)

    # Check if the user has already attempted the quiz
    previous_attempt = Score.query.filter_by(user_id=current_user.id, quiz_id=quiz_id).first()
    if previous_attempt:
        flash("You have already attempted this quiz. Multiple attempts are not allowed. Ask admin - qbc_admin@fastmail.com", "warning")
        return redirect(url_for("views.user_dashboard"))

    questions = Question.query.filter_by(quiz_id=quiz.id).all()

    # Attach options to each question
    for question in questions:
        question.options = question.get_options()  # Ensure each question has an options dict

    # Flash a warning alert before quiz starts
    flash("⚠️ Before you start, ensure a stable internet connection and avoid switching tabs. Any violations may auto-submit your quiz.", "info")

    return render_template("quiz_page.html", quiz=quiz, questions=questions)




# @views.route("/user/quiz/submit", methods=["POST"])
# @login_required
# @user_required
# def submit_quiz():
#     quiz_id = request.form.get("quiz_id")  # Get quiz_id from form-data

#     if not quiz_id:  # Debugging issue
#         return jsonify({"success": False, "message": "Error: Quiz ID is missing!"}), 400

#     responses = {key.replace("question_", ""): value for key, value in request.form.items() if key.startswith("question_")}

#     # Fetch relevant questions
#     questions = Question.query.filter(Question.quiz_id == quiz_id, Question.id.in_(map(int, responses.keys()))).all()

#     correct_answers = sum(1 for q in questions if q.correct_option.upper() == responses.get(str(q.id), "").strip().upper())

#     # Store the score
#     score = Score(user_id=current_user.id, quiz_id=int(quiz_id), total_score=correct_answers)
#     db.session.add(score)
#     db.session.commit()

#     return jsonify({"success": True, "message": "Quiz submitted successfully!", "score": correct_answers})

@user_required
@views.route('/user/analytics')
@login_required
def user_analytics():
    return render_template('user_analytics.html')

@user_required
@views.route('/user/analytics/data')
@login_required
def user_analytics_data():
    user_id = current_user.id  # Fetch logged-in user ID

    # Total quizzes attempted by the user
    quizzes_attempted = Score.query.filter_by(user_id=user_id).count()

    # Average score of the user
    avg_score = db.session.query(db.func.avg(Score.total_score))\
        .filter_by(user_id=user_id).scalar() or 0

    # Performance per subject
    subject_performance = db.session.query(
        Subject.name, db.func.avg(Score.total_score)
    ).select_from(Score)\
     .join(Quiz, Quiz.id == Score.quiz_id)\
     .join(Subject, Subject.id == Quiz.id)\
     .filter(Score.user_id == user_id)\
     .group_by(Subject.name)\
     .all()

    # Convert subject performance data into JSON serializable format
    subject_performance_data = [
        {"subject": subject, "avg_score": round(avg_score, 2)}
        for subject, avg_score in subject_performance
    ]

    # Fetch last 5 quiz attempts with timestamps
    past_performance = Score.query.filter_by(user_id=user_id)\
        .order_by(Score.time_stamp_of_attempt.desc())\
        .limit(5)\
        .all()

    # Convert past performance data
    past_performance_data = [
        {"timestamp": p.time_stamp_of_attempt.strftime("%Y-%m-%d %H:%M:%S"), "score": p.total_score}
        for p in past_performance
    ]

    return jsonify({
        "quizzes_attempted": quizzes_attempted,
        "avg_score": round(avg_score, 2),
        "subject_performance": subject_performance_data,
        "past_performance": past_performance_data
    })



@views.route("/user/quiz/submit", methods=["POST"])
@login_required
@user_required
def submit_quiz():
    quiz_id = request.form.get("quiz_id")
    
    if not quiz_id:
        return jsonify({"success": False, "message": "Error: Quiz ID is missing!"}), 400
    
    responses = {
        key.replace("question_", ""): value 
        for key, value in request.form.items() if key.startswith("question_")
    }

    questions = Question.query.filter(Question.quiz_id == quiz_id, Question.id.in_(map(int, responses.keys()))).all()
    
    correct_answers = 0
    user_answers = {}
    
    for q in questions:
        selected_option = responses.get(str(q.id), "").strip().upper()
        correct_option = q.correct_option.upper()
        
        if selected_option == correct_option:
            correct_answers += 1
        
        user_answers[q.id] = selected_option  # Store user-selected answers
    
    score = Score(user_id=current_user.id, quiz_id=int(quiz_id), total_score=correct_answers, answers=json.dumps(user_answers))
    db.session.add(score)
    db.session.commit()
    
    flash("Quiz submitted successfully! View your performance.", "success")
    return redirect(url_for("views.view_performance", quiz_id=quiz_id))

@views.route("/user/quiz/performance/<int:quiz_id>")
@login_required
@user_required
def view_performance(quiz_id):
    score = Score.query.filter_by(user_id=current_user.id, quiz_id=quiz_id).order_by(Score.time_stamp_of_attempt.desc()).first()
    if not score:
        flash("No performance data available for this quiz.", "warning")
        return redirect(url_for("views.user_dashboard"))
    
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    # Ensure valid JSON parsing and handle empty string
    try:
        user_answers = json.loads(score.answers) if score.answers else {}
    except json.JSONDecodeError:
        user_answers = {}
    
    return render_template("performance.html", questions=questions, user_answers=user_answers, score=score)

@views.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)

@views.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        dob_str = request.form.get("dob")
        qualification = request.form.get("qualification")
        password = request.form.get("password")

        current_user.full_name = full_name
        # Convert it to a datetime.date object
        dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
        current_user.dob = dob
        current_user.qualification = qualification

        if password:
            current_user.password = generate_password_hash(password, method='sha256')

        try:
            db.session.commit()
            flash("Profile updated successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", "danger")

        return redirect(url_for("views.profile"))

    return render_template("edit_profile.html", user=current_user)

@views.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_pwd = request.form['current_password']
        new_pwd = request.form['new_password']
        confirm_pwd = request.form['confirm_password']

        if not check_password_hash(current_user.password, current_pwd):
            flash('Current password is incorrect', 'error')
            return redirect(url_for('views.change_password'))

        if new_pwd != confirm_pwd:
            flash('New passwords do not match', 'error')
            return redirect(url_for('views.change_password'))

        current_user.password = generate_password_hash(new_pwd)
        db.session.commit()
        flash('Password updated successfully', 'success')
        return redirect(url_for('views.profile', user_id=current_user.id))

    return render_template('change_password.html')

@views.route("/admin/profile")
@login_required
@admin_required
def admin_profile():
    return render_template("admin_profile.html", admin=current_user)

@views.route("/admin/profile/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_admin_profile():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()

        current_user.full_name = name
        current_user.email = email

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("views.admin_profile"))

    return render_template("edit_admin_profile.html", admin=current_user)

@views.route('/admin/change/password', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_change_password():
    if request.method == 'POST':
        current_pwd = request.form['current_password']
        new_pwd = request.form['new_password']
        confirm_pwd = request.form['confirm_password']

        if not check_password_hash(current_user.password, current_pwd):
            flash('Current password is incorrect', 'error')
            return redirect(url_for('views.admin_change_password'))

        if new_pwd != confirm_pwd:
            flash('New passwords do not match', 'error')
            return redirect(url_for('views.admin_change_password'))

        current_user.password = generate_password_hash(new_pwd)
        db.session.commit()
        flash('Password updated successfully', 'success')
        return redirect(url_for('views.admin_profile', user_id=current_user.id))

    return render_template('admin_change_password.html')