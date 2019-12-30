# auth.py

from flask import Blueprint, request, flash, Response, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from flask_login import login_user, login_required, logout_user
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return Response('Access denied. Login required.', 403)


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return Response('Invalid credentials.', 400)  # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    session.permanent = True
    return Response('Login successful.', 200)


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('fullName')
    password = request.form.get('password')
    print(email)
    user = User.query.filter_by(
        email=email).first()  # if this returns a user, then the email already exists in database

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return Response('Email address already exists.', 409)

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'), is_admin=False)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return Response('Sign up successful.', 200)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return Response('Logged out successfully.', 200)
