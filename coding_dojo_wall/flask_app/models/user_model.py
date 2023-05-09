from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.post_model import Post
import pprint
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-])$')

db = "coding_dojo_wall"

class User:
    def __init__(self,data):
        self.id=  data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at'] 
        self.posts = []

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s)" 
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM users'
        results = connectToMySQL(db).query_db(query) 
        all_users = []
        pprint.pprint(results)
        for user in results:
            all_users.append(cls(user))
        return all_users

    @classmethod
    def get_users_with_posts(cls):
        query = "SELECT * FROM users JOIN posts on users.id = posts.user_id ORDER BY users.id ASC"
        results = connectToMySQL(db).query_db(query)
        users = []
        for row in results:
            if len(users) ==0:
                users.append(cls(row))
            else:
                last_user = users[len(users) - 1]    
                if last_user.id != row['id']:
                    users.append(cls(row))
            last_user = users[len(users) - 1]
            post_data = {
                'id': row['posts.id'],
                'content': row['content'],
                'created_at': row['posts.created_at'],
                'updated_at': row['posts.updated_at']
            }
            last_user.posts.append(Post(post_data))
        return users

    @classmethod
    def get_user_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_user_by_id(cls,id):
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL(db).query_db(query,{'id':id})
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def update_user(cls,data,id):
        query = f'''
        UPDATE users
        set first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, password = %(password)s
        WHERE id = {id}
        '''
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def delete_user(cls,id):
        query = f"DELETE FROM users where id = {id}"
        return connectToMySQL(db).query_db(query)

    @staticmethod
    def user_validator(user):
        is_valid = True
        if len(user['first_name']) < 1:
            flash('Your first_name is not long enough!')
            is_valid = False
        
        if len(user['last_name']) < 1:
            flash('Your last_name is not long enough!')
            is_valid = False

        if not EMAIL_REGEX.match(user['email']):
            flash('Your email is invalid!')
            is_valid = False

        if len(user['password']) < 8:
            if not PASSWORD_REGEX.match(user['password']):
                flash('Your password is invalid!')
                is_valid = False

        if not user['password'] == user['cpass']:
            flash('Your passwords do not match!')
            is_valid = False

        return is_valid

