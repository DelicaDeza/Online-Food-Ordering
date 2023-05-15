from flask import Flask, render_template, request, jsonify, redirect
from models import users
from sqlalchemy import or_

def create_account(db):
    # Retrieve the create.html form data
    if request.method != 'POST':
        return render_template('create.html')
    username = request.form.get('username')
    email = request.form.get('email')
    phone_number = request.form.get('phoneNumber')
    password = request.form.get('password')

    # Check if the email, phone number, and username already exist in the database
    existing_records = users.query.filter(or_(users.email == email, users.phone_number == phone_number, users.username == username)).all()

    if existing_records:
        # Existing credentials found
        response = {
            'message': 'Email, phone number, or username already exists. Please enter different credentials.'
        }
    else:
        # Insert the new account into the database
        new_user = users(username=username, email=email, phone_number=phone_number, password=password)
        db.session.add(new_user)
        db.session.commit()

        response = {
            'message': 'Account created successfully',
            'username': username,
            'email': email,
            'phone_number': phone_number
        }
        #print response

    return jsonify(response)
    return render_template('create.html')
