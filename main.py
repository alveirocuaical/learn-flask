
import unittest
from flask import redirect, request, make_response, render_template, session
from flask_login import login_required
from app import create_app


app = create_app()


todos = ['Comprar Cafe', 'Enviar correo', 'Entregar documentos']



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


@app.route('/hello')
@login_required
def hello():
    user_ip = session.get('user_ip')
    username = session.get('username')
    context = {
        'user_ip': user_ip,
        'todos': todos,
        'username': username
    }

    return render_template('hello.html', **context)
