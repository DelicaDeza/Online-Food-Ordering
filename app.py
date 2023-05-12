# from flask import Flask, render_template
# from flask_sqlalchemy import SQLAlchemy
# import mysql.connector

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/food'
# db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)

# class canteens(db.Model):
#     idcanteens = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), unique=True, nullable=False)

# class fooditems(db.Model):
#     idfooditems = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), unique=True, nullable=False)
#     price = db.Column(db.Float, nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)
#     canteensid = db.Column(db.Integer, db.ForeignKey('canteen.id'), nullable=False)
#     image = db.Column(db.String(120),nullable=False)

# @app.route('/')
# def index():
#     canteen = canteens.query.all() # Query all available canteens from the database
#     food_items = fooditems.query.all() # Query all available food items from the database
#     return render_template('food.html', food_items=food_items, canteen=canteen)



# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask
from food_menu import app

if __name__ == '__main__':
    app.run(debug=True)



