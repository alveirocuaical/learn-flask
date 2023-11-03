
from flask import redirect, render_template, session, url_for, flash
from flask_login import login_required, login_user, logout_user
from app import pgsql_service
from app.forms import LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, UserData
from . import auth


@auth.route('/login', methods=['GET', 'POST'])
def login():
    


    login_form = LoginForm()

    context = {
        'login_form':  login_form
    }
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        user = pgsql_service.query(username)
        print(user)
        if user is not None:
            password_from_db = user.password

            #validate password hashed 
            
            if check_password_hash(password_from_db, password):
                user_data = UserData(username, password)
                user = User(user_data)

                login_user(user)
                flash('Welcome ' + username)
                redirect(url_for('hello'))
            else:
                flash('Invalid password')
        else:
            flash('User not found')

        return redirect(url_for('index'))

    return render_template('auth/login.html', **context)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('auth.login'))


@auth.route('/singup', methods= ['GET', 'POST'])
def singup():
    singup_form = LoginForm()
    context = {
        'signup_form' : singup_form
    }
    
    if singup_form.validate_on_submit():
        username = singup_form.username.data
        password = singup_form.password.data
        
        user_exists = pgsql_service.query(username)
        if user_exists is None:
            password_hash = generate_password_hash(password)
            user_data = UserData(username, password_hash)
            
            user = pgsql_service.insert(user_data)           
            
            user = User(user_data)
            login_user(user)
            flash('Welcome ' + username)
            return redirect(url_for('hello'))
        else : 
            flash('User already exists')
    
    return render_template('auth/singup.html', **context)


