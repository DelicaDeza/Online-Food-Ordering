from flask import render_template, request, jsonify
from models import canteens, fooditems, cartitems,cart


def foodmenu():
    canteen = canteens.query.all()  # Query all available canteens from the database
    # Query all available food items from the database
    food_items = fooditems.query.all()
    return render_template('food.html', food_items=food_items, canteen=canteen)


def add_to_cart(db):
    data = request.get_json()
    name = data["name"]
    netcost = data["netcost"]
    quantity = data["quantity"]  # Retrieve the quantity from the request data
    user_id = data["user_id"]

    if quantity and quantity > 0:  # Check if quantity is not None and greater than 0
        item = cart(product_name=name, product_cost=netcost, product_quantity=quantity,status_id=3,user_id= user_id)
        db.session.add(item)
        db.session.commit()
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Invalid quantity"})


def update_cart_item_quantity(db):
    data = request.get_json()
    productName = data["productName"]
    quantity = data["quantity"]

    # Find the cart item in the database by product name and update its quantity
    cart_item = cartitems.query.filter_by(name=productName).first()
    if cart_item:
        cart_item.quantity = quantity
        db.session.commit()

    return jsonify({"success": True})
