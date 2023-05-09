from flask import render_template, redirect, request, session, flash
from flask_app.models.post_model import Post
from flask_app.models.user_model import User
from flask_app import app

@app.route('/create_post', methods =['post'] )
def create_post():
    if 'user_id' not in session:
        return redirect('/')
    if not Post.post_validator(request.form):
        return redirect('/success')
    data = {
        'content': request.form['content'],
        'id' : session['user_id']
    }
    Post.save_post(data)
    return redirect('/success')