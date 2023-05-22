
from flask import Flask, render_template, session
from models import cart, status, users


def statusmenu():
    email = session.get('email')  # Retrieve the email from the session
    # Retrieve the user based on the email
    user = users.query.filter_by(email=email).first()

    if user:
        # Query the carts and status associated with the user
        displaycart = cart.query.filter_by(user=user).all()
        displaystatus = status.query.join(cart).filter(cart.user == user).all()

        return render_template('status.html', displaycart=displaycart, displaystatus=displaystatus)
    else:
        return "User not found"


def cartmenu():
    email = session.get('email')  # Get the email from the session
    # Query the user based on the email
    user = users.query.filter_by(email=email).first()

    if user:
        # Query the cart items for the user
        displaycart = cart.query.filter_by(user_id=user.idusers).all()
        return render_template('cart.html', displaycart=displaycart)
    else:
        return 'User not found'
