from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class users(db.Model):
    idusers = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(100), unique=True, nullable=False)
    carts = db.relationship('cart', back_populates='user', lazy=True)
    order_histories = db.relationship(
        'order_history', back_populates='user', lazy=True)


class canteens(db.Model):
    idcanteens = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    fooditems = db.relationship('fooditems', backref='canteen', lazy=True)
    logs = db.relationship('logs', back_populates='canteenslogs', lazy = True)



class fooditems(db.Model):
    idfooditems = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    canteensid = db.Column(db.Integer, db.ForeignKey(
        'canteens.idcanteens'), nullable=False)
    image = db.Column(db.String(120), nullable=False)


class cart(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(80), unique=True, nullable=False)
    product_cost = db.Column(db.Integer, nullable=False)
    product_quantity = db.Column(db.Integer, nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey(
        'status.order_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.idusers'), nullable=False)
    statusses = db.relationship('status', back_populates='cartss', lazy=True)
    user = db.relationship('users', back_populates="carts", lazy=True)


class status(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    order_status = db.Column(db.String(45), unique=True, nullable=False)
    cartss = db.relationship('cart', back_populates='statusses', lazy=True)


class order_history(db.Model):
    transactionid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    foodid = db.Column(db.Integer, db.ForeignKey(
        'food.idfooditems'), nullable=False)
    foodname = db.Column(db.String(100))
    qty = db.Column(db.Integer)
    date = db.Column(db.Date)
    canteen_name = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.idusers'), nullable=False)
    user = db.relationship(
        'users', back_populates='order_histories', lazy=True)


class cartitems(db.Model):
    idcart = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    netcost = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


class admincan(db.Model):
    # _tablename_='admincan'
    
    adminid=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100))
    canteen_id=db.Column(db.Integer,db.ForeignKey('canteens.idcanteens'),nullable=False)
    def _rep_(self):
        return f"<admincan {self.adminid}>"
    
class logs(db.Model):
    transid = db.Column(db.Integer, primary_key=True)
    itemname = db.Column(db.String(50), nullable=False)
    itemquantity = db.Column(db.Float, nullable=False)
    itemcost = db.Column(db.Integer, nullable=False)
    itemdate = db.Column(db.Date)
    transactionno = db.Column(db.Integer)
    canteen_id = db.Column(db.Integer, db.ForeignKey('canteens.idcanteens'))
    canteenslogs = db.relationship('canteens', back_populates='logs')


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_status = db.Column(db.String(20))

    def __init__(self, order_status):
        self.order_status = order_status

class Verify(db.Model):
    __tablename__ = 'verify'
    id = db.Column(db.Integer, primary_key=True)
    gmail = db.Column(db.String(255))
    otp = db.Column(db.String(10))
    verified = db.Column(db.Integer)

    def __init__(self, gmail, otp):
        self.gmail = gmail
        self.otp = otp