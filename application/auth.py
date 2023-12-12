from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_bcrypt import Bcrypt
from . import db
from .models import User
from flask_login import login_user, current_user, logout_user, login_required

auth = Blueprint('auth', __name__)
bc = Bcrypt()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userEmail = request.form.get('userEmail')
        userPass = request.form.get('userPass')
        user = User.query.filter_by(email=userEmail).first()
        if user:
            if bc.check_password_hash(user.passw, userPass):
                flash('Login Successful', category='success')
                login_user(user, remember=True)
                return redirect(url_for('view.dash'))
            else:
                flash('Username or Password do not match', category='error')
            return redirect(url_for('auth.login'))
        else:
            flash('Login not possible', category='error')
            return redirect(url_for('auth.login'))
        return redirect(url_for('auth.login'))
    return render_template('login.html')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        userName = request.form.get('userName')
        userEmail = request.form.get('userEmail')
        userPass = request.form.get('userPass')
        userPass1 = request.form.get('userPass1')
        if userPass != userPass1:
            flash("Passwords don't match", category='error')
        elif len(userPass) < 8:
            flash('Password length cannot be less than 8 characters.', category='error')
        else:
            new_user = User(name=userName, email=userEmail, passw=bc.generate_password_hash(userPass))
            db.session.add(new_user)
            db.session.commit()
            flash('User Registered.', category='success')
            return redirect(url_for('auth.login'))
        return redirect(url_for('auth.signup'))
    return render_template('signup.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Successfully logged out!', category='success')
    return redirect(url_for('auth.login'))