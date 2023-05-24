from flask import render_template, request, jsonify,session
from models import canteens, fooditems, cartitems,cart


def foodmenu():
    canteen = canteens.query.all()  # Query all available canteens from the database
    # Query all available food items from the database
    food_items = fooditems.query.all()
    return render_template('food.html', food_items=food_items, canteen=canteen)


from sqlalchemy import and_

def add_to_cart(db):
    data = request.get_json()
    name = data["name"]
    netcost = data["netcost"]
    quantity = data["quantity"]
    user_id = data["user_id"]

    if quantity and quantity > 0:
        existing_item = cart.query.filter(and_(cart.product_name == name, cart.user_id == user_id)).first()
        if existing_item:
            existing_item.product_quantity = quantity
            db.session.commit()
            return jsonify({"success": True})
        else:
            new_item = cart(product_name=name, product_cost=netcost, product_quantity=quantity, status_id=3, user_id=user_id)
            db.session.add(new_item)
            db.session.commit()
            return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Invalid quantity"})



def update_cart_item_quantity(db):
    data = request.get_json()
    productName = data["productName"]
    quantity = data["quantity"]
    user_id = session["id"]

    # Find the cart item in the database by product name and user ID
    cart_item = cart.query.filter_by(product_name=productName, user_id=user_id).first()

    if cart_item:
        if quantity == 0:
            # Delete the cart item if the quantity is 0
            db.session.delete(cart_item)
        else:
            # Update the cart item quantity
            cart_item.product_quantity = quantity

        db.session.commit()

    return jsonify({"success": True})


