from flask import Flask, jsonify, render_template, session, redirect
from models import db, cart,admincan,canteens,fooditems
from food_menu import foodmenu, add_to_cart, update_cart_item_quantity
from login import index
from forgot import forgot_password
from signup import create_account
from datetime import timedelta
from functools import wraps
from cartstatus import statusmenu, cartmenu
from history import view_order_history
from foodmanage import add_food,food_items
from logs import eda
from cartupdate import update_status


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/food'
    app.config['SESSION_TYPE'] = 'filesystem'
    # Set the session configuration
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    # Ensure secure session cookie (requires HTTPS)
    app.config['SESSION_COOKIE_SECURE'] = True
    # Prevent client-side access to the session cookie
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    # Limit cross-site cookie usage
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    # Set the session timeout to None
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(
        days=30)  # Set a longer timeout (e.g., 30 days)
    # Session cookie expires when browser is closed
    app.config['SESSION_COOKIE_MAXAGE'] = None
    db.init_app(app)
    return app


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'email' not in session:
            return redirect('/')
        return view(*args, **kwargs)
    return wrapped_view


app = create_app()


@app.route('/food_menu')
@login_required
def food():
    return foodmenu()


@app.route("/api/cart", methods=["POST"])
def add():
    return add_to_cart(db)


@app.route("/api/cart/update_quantity", methods=["POST"])
def update():
    return update_cart_item_quantity(db)


@app.route('/create.html', methods=['GET', 'POST'])
def signup():
    return create_account(db)


@app.route('/', methods=['GET', 'POST'])
def login():
    return index(app)


@app.route('/forgot.html', methods=['GET', 'POST'])
def forgot():
    return forgot_password(app, db)


@app.route('/logout')
def logout():
    # Clear the email from the session
    session.pop('email', None)
    return redirect('/')


@app.route('/status.html')
@login_required
def status():
    return statusmenu()


@app.route('/cart.html')
@login_required
def cart1():
    return cartmenu()


@app.route('/delete_item/<product_id>', methods=['POST'])
def delete_item(product_id):
    try:
        # Assuming you are using SQLAlchemy as the ORM for your database
        # Assuming your model is named CartItem
        cart_item = cart.query.get(product_id)

        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Cart item deleted successfully'})
        else:
            return jsonify({'success': False, 'message': 'Cart item not found'})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route("/orderHistory")
@login_required
def order():
    return view_order_history()

@app.route("/admin")
def adminpage():
    manid = admincan.query.get(1)
    canteen = canteens.query.filter_by(idcanteens=manid.canteen_id).all()
    food_items = fooditems.query.all()
    return render_template("dashadmin.html", food_items=food_items, canteen=canteen)
@app.route('/add-food', methods=['GET','POST'])
def foodadd():
    return add_food(db)

@app.route('/food-items', methods=['GET', 'POST'])
def foodremve():
    return food_items(db)

@app.route('/eda')
def analysis():
    return eda()

@app.route('/update_status', methods=['GET','POST'])
def updatee():
    return update_status(db)
if __name__ == '__main__':
    app.run(debug=True)
