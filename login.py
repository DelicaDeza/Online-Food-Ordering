from flask import render_template, request, session, redirect, url_for
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
            session['id'] = user.idusers
            session['username'] = user.username

            if stay_logged_in:
                # Set session to permanent with a longer expiration time
                session.permanent = True
                app.permanent_session_lifetime = timedelta(days=30)
            else:
                # Set session expiration to browser close
                session.permanent = False

            return redirect(url_for('food'))
        else:
            error_message = "Invalid email or password!"
            return render_template('login.html', error_message=error_message)

    # If session email exists, user is already logged in
    if 'email' in session:
        return redirect(url_for('food'))

    return render_template('login.html')
