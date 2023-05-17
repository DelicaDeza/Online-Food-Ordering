from flask import Flask, render_template, request
from flask_mail import Mail, Message
import random
import string
from models import users
from flask_sqlalchemy import SQLAlchemy


def forgot_password(app,db):
    # app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'delicadezaaa@gmail.com'
    app.config['MAIL_PASSWORD'] = 'wxeosqldsqtxaggr'
    mail = Mail(app)
    if request.method == 'POST':
        email = request.form['email']
        # Check if email exists in the users table
        user = users.query.filter_by(email=email).first()
        if user:
            # Generate a random password
            new_password = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=8))
            # Update the user's password in the database
            user.password = new_password
            db.session.commit()
            # Send the new password to the user's email
            msg = Message('Your new password', sender='your-email-address-here', recipients=[email])
            msg.body = f'Your new password is: {new_password}'
            mail.send(msg)
            return 'An email with your new password has been sent.'
        else:
            return 'Email not found.'
    return render_template('forgot.html')