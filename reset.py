from flask import Flask, render_template, request, redirect, url_for,session,flash
import bcrypt
from flask_sqlalchemy import SQLAlchemy
from models import users


def set_password(self, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.password_hash = hashed_password.decode('utf-8')

def verify_password(self, password):
    return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
def reset_password(db):
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        # Verify the current password
        user = users.query.filter_by(idusers=session.get('idusers')).first()
        if user and user.verify_password(current_password):
            if new_password == confirm_password:
                # Update the password
                user.set_password(new_password)
                db.session.commit()
                flash('Password has been reset successfully!', 'success')
                return redirect(url_for('index'))
            else:
                flash('New password and confirm password do not match.', 'error')
        else:
            flash('Invalid current password.', 'error')
    
    return render_template('reset.html')
