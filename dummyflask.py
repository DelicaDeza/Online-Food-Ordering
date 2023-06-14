from flask import render_template, session
from models import Cart, Status, Users
from flask import redirect, url_for
from flask import request, jsonify

@app.route('/cancel_order', methods=['POST'])
def cancel_order():
    order_id = request.form.get('order_id')
    
    # Check if the order exists and is in the "Waiting" stage
    order = Order.query.get(order_id)
    if order and order.status == 'Waiting':
        # Update the order status to "Cancelled"
        order.status = 'Cancelled'
        db.session.commit()

        # Return a success response
        return redirect(url_for('refund'))
    else:
        # Return an error response
        return jsonify({'success': False, 'message': 'Unable to cancel the order.'})

def statusmenu():
    email = session.get('email')  # Retrieve the email from the session
    # Retrieve the user based on the email
    user = Users.query.filter_by(email=email).first()

    if user:
        # Query the carts and status associated with the user
        displaycart = Cart.query.filter_by(user=user).all()
        displaystatus = Status.query.join(Cart).filter(Cart.user == user).all()

        return render_template('status.html', displaycart=displaycart, displaystatus=displaystatus, can_cancel=True)
    else:
        return "User not found"

def cartmenu():
    email = session.get('email')  # Get the email from the session
    # Query the user based on the email
    user = Users.query.filter_by(email=email).first()

    if user:
        # Query the cart items for the user
        displaycart = Cart.query.filter_by(user=user).all()
        return render_template('cart.html', displaycart=displaycart)
    else:
        return 'User not found'
