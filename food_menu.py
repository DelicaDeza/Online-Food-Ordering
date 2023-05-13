from flask import Flask, render_template,Blueprint
from models import canteens, fooditems

def foodmenu():
    canteen = canteens.query.all() # Query all available canteens from the database
    food_items = fooditems.query.all() # Query all available food items from the database
    return render_template('food.html', food_items=food_items, canteen=canteen)

