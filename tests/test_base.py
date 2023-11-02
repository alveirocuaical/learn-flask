from flask import current_app, url_for
from flask_testing import TestCase
from main import app, index


class MainTest(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def test_app_exists(self):
        self.assertIsNotNone(current_app)

    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])

    # Returns a redirect response to '/hello' URL.
    def test_redirect_response(self):
        response = index()
        assert response.status_code == 302
        assert response.location == '/hello'
        
    def test_hello_get(self):
        response = self.client.get(url_for('hello'))
        self.assert200(response)
        
    
    def test_hello_post(self):
                            
        response = self.client.post(url_for('hello'))
        
        self.assertStatus(response, 405)
        
        
    def test_auth_blueprint_exists(self):
        self.assertIn('auth', self.app.blueprints)
        
    def test_auth_login_get(self):
        response = self.client.get(url_for('auth.login'))
        self.assert200(response)
        
        
    def test_login_template(self):
        self.client.get(url_for('auth.login'))
        self.assertTemplateUsed('auth/login.html')
        
    def test_auth_login_post(self):
        fake_form = {
            'username': 'fake',
            'password': 'fake-password'
        }
        response = self.client.post(url_for('auth.login'), data=fake_form)
        self.assertRedirects(response, url_for('index'))