from flask import render_template, request, redirect, url_for
from flask_mail import Mail, Message
import random
import string


def send_otp(app):
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'delicadezaaa@gmail.com'
    app.config['MAIL_PASSWORD'] = 'wxeosqldsqtxaggr'
    mail = Mail(app)
    if request.method == 'POST':
        email = request.form['email']
        otp = ''.join(random.choices(string.digits, k=4))
        msg = Message('One Time Password of your order',sender='your-email-address-here', recipients=[email])
        msg.body = f'Your OTP of the order is : {otp}'
        mail.send(msg)
        return render_template('payment.html')

    else:
        return render_template('payment.html')



