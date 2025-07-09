from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from .utils import load_users_from_excel


auth = Blueprint('auth', __name__)
login_data = './data_tables/accounts.xlsx'

# Load users from an Excel file
users = load_users_from_excel(login_data)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember')

        # print(request.remote_addr)

        user = next((u for u in users.values() if u.username == username), None)

        if user:
            if password == user.password:
                # flash('Logged in successfully!', category='success')
                login_user(user, remember=True if remember else False)

                return redirect(url_for('home.home_page'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('User does not exist.', category='error')

    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
