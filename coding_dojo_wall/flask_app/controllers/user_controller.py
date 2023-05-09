from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
from flask_app.models.user_model import User
from flask_app import app
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('/login.html')

@app.route('/create_user', methods = ['post'])
def create_user():
    print(request.form)
    if not User.user_validator(request.form):
        return redirect('/')
    if User.get_user_by_email(request.form):
        flash('email is already in use or your password and confirm password do not match')
        return redirect('/')
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    print(data['password'])
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/success')

@app.route('/login', methods = ['post'])
def login():
    data = {'email': request.form['email']}
    user_in_db = User.get_user_by_email(data)
    if not user_in_db:
        flash('Email/ Password is invalid')
        return redirect('/login')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Email/ Password is invalid')
        return redirect('/login')
    session['user_id'] = user_in_db.id
    return redirect('/success')

@app.route('/success')
def success():
    User.get_users_with_posts()
    return render_template('dashboard.html', user = User.get_user_by_id(session['user_id']), all_posts = User.get_users_with_posts())

@app.route('/clear_session')
def clear_session():
    session.clear()
    return redirect('/')