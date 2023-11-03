from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class UserData:
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password
        
        
class TodoData:
    def __init__(self, description, user_id) -> None:        
        self.description = description
        self.user_id = user_id

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    def __init__(self, user_data):
        """ 
        :param user_data: UserData
        """
        self.id = user_data.username
        self.password = user_data.password
        
    
    id = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
        
        
class Todo(db.Model):
    
    __tablename__  = 'todos'
    
    def __init__(self, todo_data):              
        self.description = todo_data.description
        self.user_id = todo_data.user_id
        
        
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    user_id = db.Column(db.String)
    status = db.Column(db.Boolean)