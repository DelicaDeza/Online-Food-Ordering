from flask import render_template, request
from models import Verify, cart, users
def check():
    if request.method == 'POST':
        gmail = request.form['gmail']
        otp = request.form['otp']

        try:
            verify_entry = Verify.query.filter_by(gmail=gmail).first()
            if verify_entry and verify_entry.otp == otp:
                response = "Verification successful!<br>"
                user_entry = users.query.filter_by(email=gmail).first()
                user_id = user_entry.idusers
                cart_items = cart.query.filter_by(user_id=user_id).all()
                
                response += f"User ID: {user_id}<br>"
                response += "<table>"
                response += "<tr><th>Product Name</th><th>Product Quantity</th><th>Product Cost</th></tr>"
                for item in cart_items:
                    response += f"<tr><td>{item.product_name}</td><td>{item.product_quantity}</td><td>{item.product_cost}</td></tr>"
                response += "</table>"
                return response
            else:
                return "Verification failed."
            
            




        except Exception as e:
            return f"Error: {str(e)}"

    return render_template('verify.html')