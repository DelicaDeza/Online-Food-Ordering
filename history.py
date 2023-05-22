from flask import render_template
from models import users
from flask import session


def view_order_history():
    email = session.get('email')  # Retrieve the email from the session
    # Retrieve the user based on the email
    user = users.query.filter_by(email=email).first()
    if user:
        # Access the order history through the back reference
        order_history = user.order_histories
        return render_template("orderhistory.html", hist=order_history)
    else:
        return "User not found"
