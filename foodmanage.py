from flask import Flask, render_template, request
from models import fooditems

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