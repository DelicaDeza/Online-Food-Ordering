
from flask import Flask, render_template,session
from models import cart, status,users


def statusmenu():
    displaycart = cart.query.all()  # Query all available canteens from the database
    # Query all available canteens from the database
    displaystatus = status.query.all()
    return render_template('status.html',  displaycart=displaycart, displaystatus=displaystatus)


def cartmenu():
    email = session.get('email')  # Get the email from the session
    user = users.query.filter_by(email=email).first()  # Query the user based on the email
    
    if user:
        displaycart = cart.query.filter_by(user_id=user.idusers).all()  # Query the cart items for the user
        return render_template('cart.html', displaycart=displaycart)
    else:
        return 'User not found'
