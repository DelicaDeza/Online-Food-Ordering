from flask import Flask
from models import db
from food_menu import foodmenu
from login import index
app = Flask(__name__)
app.secret_key = 'your-secret-key' 

def create_app():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/food'
    db.init_app(app)
    return app

app = create_app()

@app.route('/food_menu')
def food():
    return foodmenu()

@app.route('/', methods=['GET', 'POST'])
def login():
    return index()
if __name__ == '__main__':
    app.run(debug=True)



