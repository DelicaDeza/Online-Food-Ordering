
from flask import Flask, render_template
from models import cart,status

def statusmenu():
    displaycart = cart.query.all() # Query all available canteens from the database
    displaystatus = status.query.all() # Query all available canteens from the database
    return render_template('status.html',  displaycart=displaycart, displaystatus=displaystatus)

def cartmenu():
    displaycart = cart.query.all() # Query all available canteens from the database
    return render_template('cart.html',  displaycart=displaycart)
