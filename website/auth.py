from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db # from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':    # If user submits login form
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()   # Returns first user with matching username
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category='success')
                login_user(user, remember=True)     # Remembers user for 7 days
                return redirect(url_for('views.user_profile'))
            else:
                flash("Incorrect password, try again.", category='error')
        else:
            flash("Username does not exist.", category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required     # Requires user to be logged in to access this route
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')

        # Check if username or email already exists
        user = User.query.filter_by(username=username).first()
        if user:
            flash("Username already exists.", category='error')
        elif len(email) < 4:
            flash("Email must be greater than 3 characters.", category='error')
        elif len(username) < 2:
            flash("Username must be greater than 1 character.", category='error')
        elif password != confirm_password:
            flash("Passwords don\'t match.", category='error')
        elif len(password) < 7:
            flash("Password must be at least 7 characters.", category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))    # Hashes password for security
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)     # Remembers user for 7 days
            flash("Account created!", category='success')
            return redirect(url_for('views.user_profile'))
    return render_template("sign_up.html", user=current_user)