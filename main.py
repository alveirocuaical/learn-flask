
import unittest
from flask import flash, redirect, request, make_response, render_template, session, url_for
from flask_login import current_user, login_required
from app import create_app
from flask_sqlalchemy import SQLAlchemy

from app.forms import DeleleTodoForm, TodoForm
from app.models import TodoData
from app.pgsql_service import get_all, create_todo, delete_todo
from flask_login import current_user


app = create_app()

@app.cli.command()
def test():
    """Run the unit tests."""
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html', error=error)


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html', error=error)


@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip

    return response


@app.route('/hello', methods=['GET', 'POST'])
@login_required
def hello():
    user_ip = session.get('user_ip')
    username = current_user.id
    todo_form = TodoForm()
    delete_todo = DeleleTodoForm()
    
    if todo_form.validate_on_submit():
        description = todo_form.description.data
        user_id = username
        
        todo_data = TodoData(description, user_id)
        
        todos = create_todo(todo_data)
        
        flash('Todo created successfull')
        return redirect(url_for('hello'))
        
    
    
    context = {
        'user_ip': user_ip,
        'todos': get_all(username),
        'username': username,
        'todo_form': todo_form,
        'delete_todo' : delete_todo
    }

    return render_template('hello.html', **context)

@app.route('/delete/<todo_id>', methods=['POST'])
def delete(todo_id):
    delete_todo(todo_id)
    flash('Todo deleted')
    return redirect(url_for('hello'))