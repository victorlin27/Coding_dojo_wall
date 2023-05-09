from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

db = "coding_dojo_wall"

class Comment :
    def __init__(self,data):
        self.users_id = data['users_id']
        self.posts_id = data['posts_id']
        self.comment = data['comment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at'] 

    def save_comment(cls, data):
        query = 'INSERT INTO comments (users_id, posts_id, comment) VALUES (%(users_id)s,%(posts_id)s, %(comment)s)'
        return connectToMySQL(db).query_db(query,data)