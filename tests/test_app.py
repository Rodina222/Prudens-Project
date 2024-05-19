import unittest
from flask import current_app, url_for
from prudens import app, db  # Adjust imports based on your application setup
from prudens.models import Researcher, User,NonResearcher
from prudens.forms import RegistrationForm  # Import your RegistrationForm



    
class TestResearcherAuth(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF tokens for testing
        self.app = app.test_client()

        # Create a temporary researcher for testing
        with app.app_context():
            db.create_all()
    



    def test_researcher_signup(self):
        # Test researcher signup
        response = self.app.post('/researcher_signup', data={
            'fname': 'New',
            'lname': 'Researcher',
            'username': 'newresearcher2',
            'email': 'testresearcher2@zewailcity.edu.eg',
            'password': 'hashed_password_here',  # Replace with hashed password
            'field_of_study': 'Biology',
            'linkedin_account': 'https://linkedin.com/newresearcher',
            'google_scholar_account': 'https://scholar.google.com/newresearcher'
        }, follow_redirects=True)

      
        self.assertEqual(response.status_code, 200)

    def test_invalid_researcher_signup(self):
        # Test researcher signup
        response = self.app.post('/researcher_signup', data={
            'fname': 'New',
            'lname': 'Researcher',
            'username': 'newresearcher2',
            'email': 'testresearcher2@com',
            'password': 'hashed_password_here',  # Replace with hashed password
            'field_of_study': 'Biology',
            'linkedin_account': 'https://linkedin.com/newresearcher',
            'google_scholar_account': 'https://scholar.google.com/newresearcher'
        }, follow_redirects=True)

        #self.assertIn(b'Account created successfully for newresearcher2', response.data)
        print("================",response.data)
        self.assertEqual(response.status_code, 200)
        

    def test_researcher_login(self):
    # Test researcher login


        response = self.app.post('/login', data={
            'email': 'testresearcher@zewailcity.edu.eg',
            'password': 'QcpYaQFyU68e@ie'  # Replace with the actual plaintext password
        }, follow_redirects=True)

        # Check for a welcome message
        self.assertIn(b'Welcome, testresearcher', response.data)
        
        # Check for the title of the home page
        self.assertIn(b'<title>Home Page</title>', response.data)

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that session variables are correctly set after login
        with self.app.session_transaction() as sess:
            self.assertEqual(sess['current_user_email'], 'testresearcher@zewailcity.edu.eg')

        #self.assertEqual(session['user_id'], 1)  # Assuming user ID 1 for the first researcher created
    def test_valid_reset_request(self):
        response = self.app.post('/forgot_password', data={'email': 'testresearcher@zewailcity.edu.eg'}, follow_redirects=True)

        # Check for the expected flash message
       
        
        # Check for the redirect to reset_password page with the email as a query parameter
        self.assertEqual(response.status_code, 200)
     
        self.assertIn(b'<title>Reset Password</title>', response.data)


if __name__ == "__main__":
    unittest.main()
