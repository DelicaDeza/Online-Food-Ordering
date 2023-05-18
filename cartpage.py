from flask import Flask, render_template,Blueprint,request
from flask_sqlalchemy import SQLAlchemy
from models import fooditems, cart, order_history


# @app.route("/addtocart",methods=["GET","POST"])
def addtocart(db):
    username = "abc"  # Assuming you have the username

    if request.method == "POST":
        carts = request.form

        for item_id, quantity in carts.items():
            food_item = fooditems.query.get(item_id)
            if food_item:
                name = food_item.name
                net_cost = food_item.price * int(quantity)
                transaction_id = "your_transaction_id"  # Replace with actual transaction ID

                cart_item = cart(username=username, transaction_id=transaction_id, name=name, quantity=quantity, net_cost=net_cost)
                db.session.add(cart_item)
                db.session.commit()

    return render_template("food.html")
    
def view_order_history():
    return render_template("orderhistory.html",hist=order_history.query.filter_by(username="abc").all())