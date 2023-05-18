from flask import Flask, render_template, request, session, redirect
import mysql.connector
from models import users
from food_menu import foodmenu
from datetime import timedelta


def index(app):
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('pswd')
        stay_logged_in = request.form.get('stay_logged_in') == 'true'

        # Check if the email and password match a user in the database
        user = users.query.filter_by(email=email, password=password).first()

        if user:
            # Store the user's email in the session for authentication
            session['email'] = user.email
            if stay_logged_in:
                session.permanent = True
                app.permanent_session_lifetime = timedelta(days=30)
            return foodmenu()
        else:
            return "Invalid email or password"

    return render_template('login.html')
