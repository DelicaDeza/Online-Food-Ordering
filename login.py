from flask import Flask, render_template, request, session, redirect
import mysql.connector
from models import users
from food_menu import foodmenu
from datetime import timedelta

# app = Flask(__name__)
#  # Set your own secret key

# mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="root",
#     database="food"
# )
# mycursor = mydb.cursor()

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('pswd')

#         # Check if the email and password match a user in the database
#         sql = "SELECT * FROM users WHERE email = %s AND password = %s"
#         val = (email, password)
#         mycursor.execute(sql, val)
#         user = mycursor.fetchone()

#         if user:
#             # Store the user's email in the session for authentication
#             session['email'] = user[1]
#             return food_app.foodmenu()
#         else:
#             return "Invalid email or password"

#     return render_template('index.html')

# @app.route('/dashboard')
# def dashboard():
#     # Check if the user is logged in by verifying the email in the session
#     if 'email' in session:
#         email = session['email']
#         return f"Welcome, {email}! This is your dashboard."
#     else:
#         return redirect('/')

# @app.route('/logout')
# def logout():
#     # Clear the session to log out the user
#     session.clear()
#     return redirect('/')

# if __name__ == '__main__':
#     app.run(debug=True)


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
