from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, jsonify
from sqlalchemy import func
import json
from . import db
from .models import Subject, Chapter, Quiz, Question, Score, User
from .decorators import admin_required, user_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date

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

#user about page
@views.route("/user-about")
@login_required
def user_about():
    return render_template("user/about.html")

#admin about page
@views.route("/admin-about")
@login_required
@admin_required
def admin_about():
    return render_template("admin/about.html")

@views.route("/admin")
@login_required
@admin_required
def admin_dashboard():
    subjects = Subject.query.all()
    return render_template("admin/dashboard.html", subjects=subjects)

@views.route("/admin/delete_subject/<int:subject_id>", methods=["POST"])
@login_required
@admin_required
def delete_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    try:
        db.session.delete(subject)
        db.session.commit()
        flash("Subject deleted successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting subject: {str(e)}", "error")
    return redirect(url_for("views.admin_dashboard"))

@views.route("/admin/delete_chapter/<int:chapter_id>", methods=["POST"])
@login_required
@admin_required
def delete_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    subject_id = chapter.subject_id
    try:
        db.session.delete(chapter)
        db.session.commit()
        flash("Chapter deleted successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting chapter: {str(e)}", "error")
    return redirect(url_for("views.view_chapters", subject_id=subject_id))

@views.route("/admin/add_subject", methods=["GET", "POST"])
@login_required
@admin_required
def add_subject():
    if request.method == "POST":
        name = request.form.get("name", "").strip().lower()
        description = request.form.get("description", "").strip()
        qualification = request.form.get("qualification", "").strip()

        if Subject.query.filter(db.func.lower(Subject.name) == name).first():
            flash("Subject already exists!", "error")
        else:
            try:
                new_subject = Subject(name=name, description=description, qualification=qualification)
                db.session.add(new_subject)
                db.session.commit()
                flash("Subject added successfully!", "success")
            except Exception as e:
                db.session.rollback()
                flash(f"Error adding subject: {str(e)}", "error")

        return redirect(url_for("views.admin_dashboard"))

    return render_template("subjects_chapters/add_subject.html")

@views.route("/admin/chapters/<int:subject_id>")
@login_required
@admin_required
def view_chapters(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    
    return render_template("subjects_chapters/view_chapters.html", subject=subject, chapters=chapters)

@views.route("/admin/add_chapter/<int:subject_id>", methods=["GET", "POST"])
@login_required
@admin_required
def add_chapter(subject_id):
    subject = Subject.query.get_or_404(subject_id)

    if request.method == "POST":
        name = request.form.get("name").strip()
        description = request.form.get("description").strip()

        try:
            new_chapter = Chapter(name=name, description=description, subject_id=subject.id)
            db.session.add(new_chapter)
            db.session.commit()
            flash("Chapter added successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding chapter: {str(e)}", "error")
        return redirect(url_for("views.view_chapters", subject_id=subject.id)) 

    return render_template("subjects_chapters/add_chapter.html", subject=subject)

@views.route("/admin/quiz/<int:quiz_id>", methods=["GET", "POST"])
@login_required
@admin_required
def view_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz.id).all()

    if request.method == "POST":
        question_text = request.form.get("question_text")
        option_a = request.form.get("option_a")
        option_b = request.form.get("option_b")
        option_c = request.form.get("option_c")
        option_d = request.form.get("option_d")
        correct_option = request.form.get("correct_option")

        try:
            new_question = Question(
                quiz_id=quiz.id,
                question_text=question_text,
                option_a=option_a,
                option_b=option_b,
                option_c=option_c,
                option_d=option_d,
                correct_option=correct_option,
            )
            db.session.add(new_question)
            db.session.commit()
            flash("Question added successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding question: {str(e)}", "error")
        return redirect(url_for("views.view_quiz", quiz_id=quiz.id))

    return render_template("quizzes/view_quiz.html", quiz=quiz, questions=questions)

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
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding quiz: {str(e)}", "error")

    return render_template("quizzes/add_quiz.html", chapter=chapter)

@views.route("/admin/view_quizzes/<int:chapter_id>")
@login_required
@admin_required
def view_quizzes(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    quizzes = Quiz.query.filter_by(chapter_id=chapter.id).all()
    return render_template("quizzes/view_quizzes.html", chapter=chapter, quizzes=quizzes)

@views.route("/admin/delete_quiz/<int:quiz_id>", methods=["POST"])
@login_required
@admin_required
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    chapter_id = quiz.chapter_id
    try:
        db.session.delete(quiz)
        db.session.commit()
        flash("Quiz deleted successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting quiz: {str(e)}", "error")
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
        try:
            db.session.commit()
            flash("Question updated successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating question: {str(e)}", "error")
        return redirect(url_for("views.view_quiz", quiz_id=quiz.id))

    return render_template("quizzes/edit_question.html", quiz=quiz, question=question)

@views.route("/admin/delete_question/<int:question_id>", methods=["POST"])
@login_required
@admin_required
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    quiz_id = question.quiz_id
    try:
        db.session.delete(question)
        db.session.commit()
        flash("Question deleted successfully!", "danger")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting question: {str(e)}", "error")
    return redirect(url_for("views.view_quiz", quiz_id=quiz_id))

@views.route("/admin/analytics")
@login_required
@admin_required
def admin_analytics():
    return render_template('admin/analytics.html')

@views.route('/admin/analytics/data')
@login_required
@admin_required
def admin_analytics_data():
    total_students = User.query.filter_by(is_admin=False).count()
    
    total_subjects = Subject.query.count()
    total_quizzes = Quiz.query.count()
    active_quizzes = Quiz.query.filter_by(published=True).count()

    subject_performance = db.session.query(
        Subject.name, func.coalesce(func.avg(Score.total_score), 0)
    ).select_from(Score)\
    .join(Quiz, Quiz.id == Score.quiz_id)\
    .join(Chapter, Chapter.id == Quiz.chapter_id)\
    .join(Subject, Subject.id == Chapter.subject_id)\
    .join(User, User.id == Score.user_id)\
    .filter(User.is_admin == False) \
    .group_by(Subject.id, Subject.name)\
    .all()

    subject_performance_data = [
        {"subject": subject, "avg_score": round(avg_score, 2)}
        for subject, avg_score in subject_performance
    ]

    qualification_distribution = db.session.query(
        User.qualification, func.count(User.id)
    ).filter(User.is_admin == False).group_by(User.qualification).all()

    qualification_distribution_data = [
        {"qualification": qualification, "count": count}
        for qualification, count in qualification_distribution
    ]

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
    try:
        quiz.published = not quiz.published
        db.session.commit()
        flash(f"Quiz {'published' if quiz.published else 'unpublished'} successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error toggling quiz publish status: {str(e)}", "error")
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
        .filter(Quiz.published == True)
        .group_by(Quiz.id, Chapter.name, Subject.name)
        .all()
    )

    return render_template("user/dashboard.html", quizzes=quizzes)


@views.route("/user/quiz/<int:quiz_id>", methods=["GET"])
@login_required
@user_required
def start_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)

    previous_attempt = Score.query.filter_by(user_id=current_user.id, quiz_id=quiz_id).first()
    if previous_attempt:
        flash("You have already attempted this quiz. Multiple attempts are not allowed. Please contact the admin if you believe this is an error.", "warning")
        return redirect(url_for("views.user_dashboard"))

    questions = Question.query.filter_by(quiz_id=quiz.id).all()

    for question in questions:
        question.options = question.get_options()

    flash("⚠️ Before you start, ensure a stable internet connection and avoid switching tabs. Any violations may auto-submit your quiz.", "error")

    return render_template("quizzes/quiz_page.html", quiz=quiz, questions=questions)


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
    return render_template('user/analytics.html')

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
        
        user_answers[q.id] = selected_option
    
    try:
        score = Score(user_id=current_user.id, quiz_id=int(quiz_id), total_score=correct_answers, answers=json.dumps(user_answers))
        db.session.add(score)
        db.session.commit()
        flash("Quiz submitted successfully! View your performance.", "success")
        return redirect(url_for("views.view_performance", quiz_id=quiz_id))
    except Exception as e:
        db.session.rollback()
        flash(f"Error submitting quiz: {str(e)}", "error")
        return redirect(url_for("views.user_dashboard"))

@views.route("/user/quiz/performance/<int:quiz_id>")
@login_required
@user_required
def view_performance(quiz_id):
    score = Score.query.filter_by(user_id=current_user.id, quiz_id=quiz_id).order_by(Score.time_stamp_of_attempt.desc()).first()
    if not score:
        flash("No performance data available for this quiz.", "warning")
        return redirect(url_for("views.user_dashboard"))
    
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    try:
        user_answers = json.loads(score.answers) if score.answers else {}
    except json.JSONDecodeError:
        user_answers = {}
    
    return render_template("user/performance.html", questions=questions, user_answers=user_answers, score=score)

@views.route("/profile")
@login_required
def profile():
    return render_template("user/profile.html", user=current_user)

@views.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        dob_str = request.form.get("dob")
        qualification = request.form.get("qualification")
        password = request.form.get("password")

        current_user.full_name = full_name
        
        if dob_str:
            try:
                current_user.dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
            except ValueError:
                flash("Invalid date format for Date of Birth. Please use YYYY-MM-DD.", "error")
                return redirect(url_for("views.edit_profile"))
        else:
            current_user.dob = None

        current_user.qualification = qualification

        if password:
            # Removed method='sha256'
            current_user.password = generate_password_hash(password)

        try:
            db.session.commit()
            flash("Profile updated successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred while updating profile: {str(e)}", "danger")

        return redirect(url_for("views.profile"))

    return render_template("user/edit_profile.html", user=current_user)

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
        
        if len(new_pwd) < 8:
            flash('New password must be at least 8 characters long', 'error')
            return redirect(url_for('views.change_password'))

        try:
            # Removed method='sha256'
            current_user.password = generate_password_hash(new_pwd)
            db.session.commit()
            flash('Password updated successfully', 'success')
            return redirect(url_for('views.profile'))
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred while changing password: {str(e)}", "danger")
            return redirect(url_for('views.change_password'))


    return render_template("user/change_password.html")

@views.route("/admin/profile")
@login_required
@admin_required
def admin_profile():
    return render_template("admin/profile.html", admin=current_user)

@views.route("/admin/profile/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_admin_profile():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()

        current_user.full_name = name
        current_user.email = email

        try:
            db.session.commit()
            flash("Profile updated successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred while updating admin profile: {str(e)}", "danger")

        return redirect(url_for("views.admin_profile"))

    return render_template("admin/edit_admin_profile.html", admin=current_user)

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
        
        if len(new_pwd) < 8:
            flash('New password must be at least 8 characters long', 'error')
            return redirect(url_for('views.admin_change_password'))

        try:
            # Removed method='sha256'
            current_user.password = generate_password_hash(new_pwd)
            db.session.commit()
            flash('Password updated successfully', 'success')
            return redirect(url_for('views.admin_profile'))
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred while changing admin password: {str(e)}", "danger")
            return redirect(url_for('views.admin_change_password'))

    return render_template('admin_change_password.html')

# Leaderboard route
@views.route('/leaderboard')
@login_required
def leaderboard():
    """
    Displays the global leaderboard based on total scores.
    Users are ranked by their sum of scores across all quizzes.
    Ties are handled by SQLAlchemy's default ordering (usually by primary key if no other order is specified).
    """
    # Query to get total score and total quiz attempts for each user
    # We use a left join to include users who might not have any scores yet.
    # Group by user ID and order by total_score in descending order.
    leaderboard_data = db.session.query(
        User.id,
        User.full_name,
        User.email,
        func.sum(Score.total_score).label('total_score'), # Use total_score from Score model
        func.count(Score.quiz_id).label('quiz_attempts')
    ).outerjoin(Score, User.id == Score.user_id)\
    .group_by(User.id, User.full_name, User.email)\
    .order_by(func.sum(Score.total_score).desc(), User.full_name.asc())\
    .all()

    # Determine the current user's rank and details
    current_user_rank_info = None
    if current_user.is_authenticated:
        for index, entry in enumerate(leaderboard_data):
            if entry.id == current_user.id:
                current_user_rank_info = {
                    'rank': index + 1,
                    'total_score': entry.total_score if entry.total_score is not None else 0,
                    'quiz_attempts': entry.quiz_attempts if entry.quiz_attempts is not None else 0
                }
                break
        # If current user is not in the leaderboard_data (e.g., no scores yet),
        # initialize their info with 0s.
        if current_user_rank_info is None:
             current_user_rank_info = {
                'rank': 'N/A',
                'total_score': 0,
                'quiz_attempts': 0
            }

    return render_template(
        "leaderboard.html",
        leaderboard_data=leaderboard_data,
        current_user_rank_info=current_user_rank_info,
        user=current_user
    )


# Helper function (if you want to fetch user's rank from anywhere else)
def get_user_rank(user_id):
    """
    Helper function to get a specific user's rank and score.
    Returns a dictionary with rank, total_score, quiz_attempts or None if not found.
    """
    leaderboard_data = db.session.query(
        User.id,
        func.sum(Score.total_score).label('total_score'),
        func.count(Score.quiz_id).label('quiz_attempts')
    ).outerjoin(Score, User.id == Score.user_id)\
    .group_by(User.id)\
    .order_by(func.sum(Score.total_score).desc())\
    .all()

    for index, entry in enumerate(leaderboard_data):
        if entry.id == user_id:
            return {
                'rank': index + 1,
                'total_score': entry.total_score if entry.total_score is not None else 0,
                'quiz_attempts': entry.quiz_attempts if entry.quiz_attempts is not None else 0
            }
    return None

