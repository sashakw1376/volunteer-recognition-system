import pytest
from tests.conftest import app, test_client, init_database
from app.forms import RegistrationForm
from app.models import User
from flask_wtf import FlaskForm
from wtforms import ValidationError
from app.extensions import bcrypt
import email_validator
import json

def test_nologin_redirects(test_client):
    """
    GIVEN a Flask application configured for testing and a user is not logged in
    WHEN any page requiring a user to be logged in is requested (GET)
    THEN check that the response redirects to the login page.
    """
    response = test_client.get('/') # home page
    assert response.status_code == 302
    response = test_client.get('/rewards')
    assert response.status_code == 302
    response = test_client.get('/edit_profile')
    assert response.status_code == 302
    response = test_client.get('/add_hours')
    assert response.status_code == 302
    response = test_client.get('/remove_user')
    assert response.status_code == 302
    response = test_client.get('/view_database')
    assert response.status_code == 302
    response = test_client.get('/logout')
    assert response.status_code == 302
    response = test_client.get('/login')
    assert response.status_code == 200
    response = test_client.get('/register')
    assert response.status_code == 200

# registers users from register form
def register(test_client, name, email, password, confirm_password, role):
    return test_client.post('/register', data=dict(
        name=name,
        email=email,
        password=password,
        confirm_password=confirm_password,
        role=role
    ), follow_redirects=True)

def test_register_success(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN a valid user registration is requested (POST)
    THEN check that a user is created successfully.
    """
    response = register(test_client, 'newuser', 'newuser@example.com', 'securePassword123', 'securePassword123', 'volunteer')
    assert response.status_code == 200
    assert b'Account created successfully! You are now logged in as newuser.' in response.data
    response = test_client.get('/logout') # last user must be logged out for tests to work

# logs in users from login form
def login(test_client, email, password, remember_me=False):
    return test_client.post('/login', data=dict(
        email=email,
        password=password,
        remember=remember_me
    ), follow_redirects=True)

def test_login_success(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN a login is requested as a valid user
    THEN check that the login is successful.
    """
    response = login(test_client, 'testvolunteer@example.com', 'password123')
    assert response.status_code == 200
    assert b'Logged in successfully as testvolunteer' in response.data
    response = test_client.get('/logout')

def test_login_redirects(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    GIVEN a user is logged in
    WHEN a user requests authentication pages
    THEN check for redirect.
    """

def test_volunteer_redirects(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    GIVEN a volunteer is logged in
    WHEN a volunteer requests volunteer access pages
    THEN check for accepted response.
    """

    """
    WHEN a volunteer requests non-volunteer access pages
    THEN check for redirects.
    """

def test_org_redirects(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    GIVEN a volunteer org is logged in
    WHEN an org requests org access pages
    THEN check for accepted response.
    """

    """
    WHEN a org requests non-org access pages
    THEN check for redirects.
    """

def test_admin_redirects(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    GIVEN an admin is logged in
    WHEN an admin requests admin access pages
    THEN check for accepted response.
    """

    """
    WHEN an admin requests non-admin access pages
    THEN check for redirects.
    """

