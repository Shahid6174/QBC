from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import random
from flask_mailman import Mail, EmailMessage
from datetime import datetime, timedelta
from .models import User
from flask_login import login_user, current_user   
from werkzeug.security import generate_password_hash, check_password_hash
from . import db  
from flask import current_app

mail = Mail()

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'
        user = User.query.filter_by(email=email).first()

        if user:
            if not user.is_verified:
                flash('Please verify your email before logging in.', category='error')
                return redirect(url_for('auth.verify_email', email=email))

            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=remember)
                return redirect(url_for('views.dashboard'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Email doesn\'t exist', category='error')

    return render_template('login.html', user=current_user)

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
                qualification=qualification,
                dob=dob,
                verification_code=verification_code
            )
            db.session.add(new_user)
            db.session.commit()

            # Create email message
            msg = EmailMessage(
                subject='Welcome to QBC - Email Verification',
                body=f'''
                Hello {full_name},

                Welcome to QBC! Please use the following code to verify your email address:

                Verification Code: {verification_code}

                This code will expire in 24 hours.

                If you did not create this account, please ignore this email.

                Best regards,
                QBC Team
                ''',
                to=[email],
                from_email=current_app.config['MAIL_DEFAULT_SENDER']
            )
            
            try:
                msg.send()
                flash('Verification code sent! Please check your email.', category='info')
                return redirect(url_for('auth.verify_email', email=email))
            except Exception as e:
                flash('Error sending verification email. Please try again.', category='error')
                db.session.delete(new_user)
                db.session.commit()
                print(f"Email error: {str(e)}")

    return render_template('sign-up.html', user=current_user)

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

    return render_template('verify_email.html', email=email, user=current_user)

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
            from_email='qbc_admin@fastmail.com'
        )
        msg.send()

        flash('A new verification code has been sent to your email.', category='info')
        return redirect(url_for('auth.verify_email', email=email))
    
    flash('User not found or already verified.', category='error')
    return redirect(url_for('auth.login'))

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('views.landing_page'))

@auth.route('/reset-password-request', methods=['GET', 'POST'])
def reset_password_request():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Generate a random reset code
            reset_code = ''.join(random.choices('0123456789', k=6))
            user.reset_code = reset_code
            user.reset_code_expires = datetime.utcnow() + timedelta(hours=1)
            db.session.commit()

            # Send reset code email
            msg = EmailMessage(
                subject='Password Reset Request',
                body=f'Your password reset code is: {reset_code}\nThis code will expire in 1 hour.',
                to=[email]
            )
            msg.send()
            
            flash('Password reset code has been sent to your email.', category='info')
            return redirect(url_for('auth.reset_password', email=email))
        else:
            flash('Email not found.', category='error')
    
    return render_template('reset_password_request.html', user=current_user)

@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    email = request.args.get('email')
    if request.method == 'POST':
        code = request.form.get('code')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash('User not found.', category='error')
            return redirect(url_for('auth.login'))
            
        if not user.reset_code or user.reset_code != code:
            flash('Invalid reset code.', category='error')
            return redirect(url_for('auth.reset_password', email=email))
            
        if datetime.utcnow() > user.reset_code_expires:
            flash('Reset code has expired.', category='error')
            return redirect(url_for('auth.reset_password_request'))
            
        if new_password != confirm_password:
            flash('Passwords do not match.', category='error')
            return redirect(url_for('auth.reset_password', email=email))
            
        if len(new_password) < 8:
            flash('Password must be at least 8 characters long.', category='error')
            return redirect(url_for('auth.reset_password', email=email))
            
        # Update password
        user.password = generate_password_hash(new_password)
        user.reset_code = None
        user.reset_code_expires = None
        db.session.commit()
        
        flash('Your password has been reset successfully.', category='success')
        return redirect(url_for('auth.login'))
        
    return render_template('reset_password.html', email=email, user=current_user)  