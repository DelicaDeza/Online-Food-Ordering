from flask import Flask, render_template, request, session, redirect
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Set your own secret key

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Gokul007$",
    database="test"
)
mycursor = mydb.cursor()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('pswd')

        # Check if the email and password match a user in the database
        sql = "SELECT * FROM users WHERE email = %s AND password = %s"
        val = (email, password)
        mycursor.execute(sql, val)
        user = mycursor.fetchone()

        if user:
            # Store the user's email in the session for authentication
            session['email'] = user[1]
            return redirect('/dashboard')
        else:
            return "Invalid email or password"

    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    # Check if the user is logged in by verifying the email in the session
    if 'email' in session:
        email = session['email']
        return f"Welcome, {email}! This is your dashboard."
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    # Clear the session to log out the user
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
