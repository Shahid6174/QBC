from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import random
from flask_mailman import Mail, EmailMessage
from datetime import datetime
from .models import User
from flask_login import login_user, current_user   
from werkzeug.security import generate_password_hash, check_password_hash
from . import db  
import os

mail = Mail()

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user:
            if not user.is_verified:
                flash('Please verify your email before logging in.', category='error')
                return redirect(url_for('auth.verify_email', email=email))

            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.dashboard'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Email doesn\'t exist', category='error')

    return render_template('auth/login.html', user=current_user)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        full_name = request.form.get('full_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        qualification = request.form.get('qualification')
        dob = request.form.get('dob')
        dob = datetime.strptime(dob, "%Y-%m-%d").date()

        user = User.query.filter_by(email=email).first()
        if user:
            flash('User already exists', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
        elif len(full_name) < 2:
            flash('Full name must be greater than 2 characters', category='error')
        elif password2 != password1:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 8:
            flash('Passwords must be at least 8 characters', category='error')
        else:
            verification_code = generate_verification_code()
            new_user = User(
                email=email, 
                full_name=full_name,
                password=generate_password_hash(password1), 
                qualification = qualification,
                dob = dob,
                verification_code=verification_code
            )
            db.session.add(new_user)
            db.session.commit()

            msg = EmailMessage(
                subject='Email Verification',
                body=f'Your verification code is: {verification_code}',
                to=[email],
                from_email=os.environ.get('ADMIN_EMAIL')
            )
            msg.send()

            flash('Verification code sent! Please check your email.', category='success')
            return redirect(url_for('auth.verify_email', email=email))

    return render_template('auth/sign-up.html', user=current_user)

@auth.route('/verify-email', methods=['GET', 'POST'])
def verify_email():
    email = request.args.get('email')
    if request.method == 'POST':
        code = request.form.get('code')
        user = User.query.filter_by(email=email).first()

        if user and user.verification_code == code:
            user.is_verified = True
            user.verification_code = None  
            db.session.commit()
            flash('Email verified! You can now log in.', category='success')
            return redirect(url_for('auth.login'))
        else:
            flash('Invalid verification code. Please try again.', category='error')

    return render_template('auth/verify_email.html', email=email, user=current_user)

def generate_verification_code():
    return str(random.randint(100000, 999999))

@auth.route('/re-verify-email', methods=['GET', 'POST'])
def resend_verification_code():
    email = request.args.get('email')
    user = User.query.filter_by(email=email).first()

    if user and not user.is_verified:
        new_code = generate_verification_code()
        user.verification_code = new_code
        db.session.commit()

        msg = EmailMessage(
            subject='Resend: Email Verification',
            body=f'Your new verification code is: {new_code}',
            to=[email],
            from_email=os.environ.get('ADMIN_EMAIL')
        )
        msg.send()

        flash('A new verification code has been sent to your email.', category='success')
        return redirect(url_for('auth.verify_email', email=email))
    
    flash('User not found or already verified.', category='error')
    return redirect(url_for('auth.login'))

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('views.landing_page'))
