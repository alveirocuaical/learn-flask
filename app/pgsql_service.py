from .models import Todo, db, User, UserData

def query(user_id):       
    
    user = User.query.filter_by(id=user_id).first()    
    
    if user is None:
        return None
    
    user_data = UserData(
        username =  user.id, 
        password= user.password
    )        
    return User(user_data)


def insert(user_data):
       
    #create user into data base
    user = User(user_data)
    db.session.add(user)
    db.session.commit()
    return user



# todos

def get_all(user_id):
    todos = Todo.query.filter_by(user_id=user_id).all()
    
    return todos


def create_todo(todo_data):
    todo = Todo(todo_data)
    db.session.add(todo)
    db.session.commit()
    return todo


def delete_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return True