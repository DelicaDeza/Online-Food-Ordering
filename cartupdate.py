
from flask import render_template, request
from models import Order


def index():
    # Fetch all orders from the database
    orders = Order.query.all()
    return render_template('status.html', orders=orders)

def update_status(db):
    order_id = request.form['order_id']
    new_status = request.form['new_status']

    # Find the order by ID
    order = Order.query.get(order_id)
    if order:
        order.order_status = new_status
        db.session.commit()
        return 'Status updated successfully'
    else:
        return 'Order not found'
