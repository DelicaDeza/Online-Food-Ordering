from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import mysql.connector

db = SQLAlchemy()

class users(db.Model):
    idusers = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)


class canteens(db.Model):
    idcanteens = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

class fooditems(db.Model):
    idfooditems = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    canteensid = db.Column(db.Integer, db.ForeignKey('canteen.id'), nullable=False)
    image = db.Column(db.String(120),nullable=False)

class cartitem(db.Model):
    idcart = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    netcost = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)