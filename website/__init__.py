from flask import Flask
from flask_cors import CORS
from os import path
from flask_login import LoginManager
from .models import User
import pandas as pd


# Function to load users from an Excel file
def load_users_from_excel(file_path):
    df = pd.read_excel(file_path)
    users = {}
    for _, row in df.iterrows():
        user = User(user_id=row['user_id'], username=row['username'], password=row['password'], account_type=row['account_type'], course_id=row['course_id'])
        users[user.user_id] = user
    return users


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY'] = 'secret_key'

    from .auth import auth
    from .home import home

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(home, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Load users from the Excel file
    users = load_users_from_excel('./data_tables/accounts.xlsx')


    @login_manager.user_loader
    def load_user(id):
        return users.get(int(id))

    return app
