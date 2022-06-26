from flask import Flask
# Import plugin sqlalchemy untuk connect ke database
from flask_sqlalchemy import SQLAlchemy
# agar bisa menggunakan os path (windows path dll)
from os import path
# manage login user
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    # Untuk keaman cookie and session
    # Jika production, jangan share kode ini
    app.config['SECRET_KEY'] = 'kajwhdk1232 daw109283'
    # Untuk mengkoneksikan ke database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # memanggil blueprint
    # dari file views import variable views
    from .views import views
    from .auth import auth

    # seperti memanggil controller views, lalu route define di controller
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # import models file
    from .models import User, Note
    # from .models import *

    create_database(app)

    login_manager = LoginManager()
    # jika user tidak login, maka di arahkan ke auth.login
    login_manager.login_view = 'auth.login'
    # menentukan menggunakan app mana
    login_manager.init_app(app)

    # menentukan user yang sedang login menggunakan id pada form login
    # seperti memasukan data login ke session user login
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# cek jika database sudah ada, maka tidak di overide
# kalau tidak ada maka di buat
# database.db
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')