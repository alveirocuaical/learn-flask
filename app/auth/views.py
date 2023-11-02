
from flask import redirect, render_template, session, url_for, flash
from app.forms import LoginForm
from . import auth

@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    username = session.get('username')
    context = {
        'login_form':  login_form
    }
    if context['login_form'].validate_on_submit():
        username = login_form.username.data
        session['username'] = username

        flash('username saved success')
        return redirect(url_for('index'))
    
    return render_template('auth/login.html', **context)