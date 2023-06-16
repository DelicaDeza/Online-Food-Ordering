
from flask import render_template, request,Flask
from models import status

app = Flask(__name__)

@app.route('/update_status', methods=['POST'])
def cartt():
    # Fetch all orders from the database
    orders = status.query.all()
    return render_template('cartupdate.html', displaystatus=orders)


def update_status(db):
    order_id = request.form['order_id']
    new_status = request.form['new_status']

    # Find the order by ID
    order = status.query.get(order_id)
    if order:
        order.order_status = new_status
        db.session.commit()
        return 'Status updated successfully'
    else:
        return 'Order not found'
    
