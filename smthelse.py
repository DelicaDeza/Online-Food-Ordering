from flask import Flask, render_template, session, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'your_database_uri'
db = SQLAlchemy(app)

class Canteens(db.Model):
    idcanteens = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    fooditems = db.relationship('FoodItems', backref='canteen', lazy=True)

class FoodItems(db.Model):
    idfooditems = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    canteensid = db.Column(db.Integer, db.ForeignKey('canteens.idcanteens'), nullable=False)
    image = db.Column(db.String(120), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    carts = db.relationship('Cart', backref='user', lazy=True)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(80), nullable=False)
    product_cost = db.Column(db.Integer, nullable=False)
    product_quantity = db.Column(db.Integer, nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_status = db.Column(db.String(80), nullable=False)
    carts = db.relationship('Cart', backref='status', lazy=True)

@app.route('/statusmenu')
def statusmenu():
    email = session.get('email')  # Retrieve the email from the session
    # Retrieve the user based on the email
    user = User.query.filter_by(email=email).first()

    if user:
        # Query the carts and status associated with the user
        displaycart = Cart.query.filter_by(user=user).all()
        displaystatus = Status.query.join(Cart).filter(Cart.user == user).all()

        return render_template('refund.html', displaycart=displaycart, displaystatus=displaystatus)
    else:
        return "User not found"

@app.route('/')
def index():
    # Retrieve the cancelled item's cost from the request parameters
    cancelled_item_cost = request.args.get('cancelled_item_cost')
    if cancelled_item_cost is not None:
        cancelled_item_cost = float(cancelled_item_cost)

    # Set the maximum price to the cost of the cancelled item
    max_price = cancelled_item_cost

    # Retrieve the canteens and food items based on the maximum price limit
    canteens = Canteens.query.all()
    if max_price is not None:
        food_items = FoodItems.query.filter(FoodItems.price <= max_price).all()
    else:
        food_items = FoodItems.query.all()

    # Pass the necessary data to the template
    return render_template('index.html', canteens=canteens, food_items=food_items, max_price=max_price)


if __name__ == '__main__':
    app.run()

