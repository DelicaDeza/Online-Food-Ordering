from flask import Flask, render_template, request, session, redirect
import mysql.connector
from models import users
from food_menu import foodmenu
from datetime import timedelta
import bcrypt

def index(app):
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('pswd')
        stay_logged_in = request.form.get('stay_logged_in') == 'true'

        # Retrieve the user from the database based on the email
        user = users.query.filter_by(email=email).first()

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            # Store the user's email in the session for authentication
            session['email'] = user.email
            user = users.query.filter_by(email=email).first()
    
            if user:
                # Retrieve the username from the user object
                session['username'] = user.username
            if stay_logged_in:
                session.permanent = True
                app.permanent_session_lifetime = timedelta(days=30)
            return foodmenu()
        else:
            return "Invalid email or password"

    return render_template('login.html')