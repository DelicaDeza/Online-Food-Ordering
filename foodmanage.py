from flask import Flask, render_template, request
from models import fooditems,canteens

def add_food(db):
    if request.method == 'POST':
        name = request.form['food-name']
        price = float(request.form['food-price'])
        canteen = request.form['food-canteen']
        image = request.form['food-image']

        new_food = fooditems(name=name, price=price, canteensid=canteen, image=image)
        db.session.add(new_food)
        db.session.commit()

        return render_template('add.html')
    else:
        return render_template('add.html')
    

def food_items(db):
    if request.method == 'POST':
        # Get the form data
        food_items_data = request.form.getlist('food-item')
        quantities_data = request.form.getlist('quantity')

        for food_item_id, quantity in zip(food_items_data, quantities_data):
            # Retrieve the food item from the database
            food_item = fooditems.query.get(food_item_id)

            if quantity == '0':
                # Confirmation popup for removal
                # Assuming you have a JavaScript function called 'confirmRemoval'
                return f'<script>confirmRemoval("{food_item.name}", "{food_item.idfooditems}");</script>'
            else:
                # Update the quantity
                food_item.quantity = int(quantity)

        db.session.commit()

    # Retrieve all canteens from the database
    canteens_data = canteens.query.all()

    return render_template('remove.html', canteens=canteens_data)