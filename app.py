from flask import Flask,request,jsonify
from models import db,cartitem
from food_menu import foodmenu
from login import index
from forgot import forgot_password
from signup import create_account
from datetime import timedelta

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/food'
    app.secret_key = 'your-secret-key' 
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
    db.init_app(app)
    return app

app = create_app()

@app.route('/food_menu')
def food():
    return foodmenu()
@app.route("/api/cart", methods=["POST"])
def add_to_cart():
    data = request.get_json()
    name = data["name"]
    netcost = data["netcost"]
    quantity = data["quantity"]
    item = cartitem(name=name, netcost=netcost, quantity=quantity)
    db.session.add(item)
    db.session.commit()
    return jsonify({"success": True})
@app.route('/create_account', methods=['POST'])
def signup():
    return create_account(db)
@app.route('/', methods=['GET', 'POST'])
def login():
    return index(app)
@app.route('/forgot.html', methods=['GET', 'POST'])
def forgot():
    return forgot_password(db)
if __name__ == '__main__':
    app.run(debug=True)



