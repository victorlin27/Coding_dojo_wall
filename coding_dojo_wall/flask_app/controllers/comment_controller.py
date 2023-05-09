from flask import render_template, redirect, request, session, flash
# from flask_app.models.post_model import Post
# from flask_app.models.user_model import User
from flask_app.models.comment_model import Comment
from flask_app import app

@app.route('/save_comment/<int:post_id>', methods = ['post'])
def save_comment(post_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'users_id':session['user_id'],
        'posts_id' : post_id,
        'comment' : request.form['comment']
    }
    Comment.save_commnent(data)
    return redirect('/success')