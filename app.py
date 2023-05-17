from flask import Flask,request,jsonify,session, redirect,url_for
from models import db,cartitem
from food_menu import foodmenu
from login import index
from forgot import forgot_password
from signup import create_account
from datetime import timedelta
from functools import wraps
from cartstatus import statusmenu

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/food'
    app.secret_key = 'your-secret-key' 
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
    db.init_app(app)
    return app


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'email' not in session:
            return redirect('/login.html')
        return view(*args, **kwargs)
    return wrapped_view


app = create_app()

@app.route('/food_menu')
@login_required
def food():
    return foodmenu()

@app.route("/api/cart", methods=["POST"])
@login_required
def add_to_cart():
    data = request.get_json()
    name = data["name"]
    netcost = data["netcost"]
    quantity = data["quantity"]
    item = cartitem(name=name, netcost=netcost, quantity=quantity)
    db.session.add(item)
    db.session.commit()
    return jsonify({"success": True})

@app.route('/create.html', methods=['GET','POST'])
def signup():
    return create_account(db)

@app.route('/login.html', methods=['GET', 'POST'])
def login():
    return index(app)

@app.route('/forgot.html', methods=['GET', 'POST'])
def forgot():
    return forgot_password(app,db)

@app.route('/logout')
def logout():
    # Clear the email from the session
    session.pop('email', None)
@app.route('/status.html')
def cart():
    return statusmenu()

if __name__ == '__main__':
    app.run(debug=True)



