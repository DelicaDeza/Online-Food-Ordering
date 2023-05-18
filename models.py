from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import mysql.connector

db = SQLAlchemy()


class users(db.Model):
    idusers = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(100), unique=True, nullable=False)


class canteens(db.Model):
    idcanteens = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)


class fooditems(db.Model):
    idfooditems = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    canteensid = db.Column(db.Integer, db.ForeignKey(
        'canteen.id'), nullable=False)
    image = db.Column(db.String(120), nullable=False)


class cartitem(db.Model):
    idcart = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    netcost = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


class cart(db.Model):
    product_id = db.Column(db.String(3), primary_key=True)
    product_name = db.Column(db.String(80), unique=True, nullable=False)
    product_cost = db.Column(db.Integer, nullable=False)
    product_quantity = db.Column(db.Integer, nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey(
        'status.order_id'), nullable=False)


class status(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    order_status = db.Column(db.String(45), unique=True, nullable=False)


class order_history(db.Model):
    transactionid = db.Column(db.Integer, primary_key = True)
    username=db.Column(db.String(100))
    foodid=db.Column(db.Integer, db.ForeignKey(
        'food.idfooditems'), nullable=False)
    foodname=db.Column(db.String(100))
    qty=db.Column(db.Integer)
    date=db.Column(db.Date)