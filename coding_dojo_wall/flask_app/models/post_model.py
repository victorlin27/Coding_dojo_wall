from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

db = "coding_dojo_wall"

class Post :
    def __init__(self,data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def save_post(cls,data):
        query = "INSERT INTO posts (content, user_id) VALUES (%(content)s, %(id)s )"
        return connectToMySQL(db).query_db(query,data)

    @staticmethod
    def post_validator(post_data):
        is_valid = True
        if (len(post_data['content']) == 0):
            flash('The content field must not be empty')
            is_valid = False
        return is_valid
