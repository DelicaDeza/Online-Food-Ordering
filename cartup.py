from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class cart(db.Model):
    username=db.Column(db.Integer,primary_key=True)
   
    foodname=db.Column(db.String(100))
    qty=db.Column(db.Integer)
    cost=db.Column(db.Integer)




