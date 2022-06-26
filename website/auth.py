# untuk menyimpan routes

# menyatakan bahwa file ini adalah blueprint
# dimana blueprint adalah has bunch of roots inside
# request untuk handle request post
# flash digunakan untuk menampilkan flash message seperti session error pada laravel

# Blueprint : untuk membuat route seperti views.py/auth.py
from flask import Blueprint, render_template, request, flash, redirect, url_for
# import model untuk menggunakan user
from .models import User
from . import db
# seperti auth()->user() dll
from flask_login import login_user, login_required, logout_user, current_user

# import wekzeug untuk hashing pass
from werkzeug.security import generate_password_hash, check_password_hash

# auth bebas menggunakan apa saja, tdetapi harus dengan paramater __name__
auth = Blueprint('auth', __name__)

# Dapat menerima permintaan GET dan POST
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # cari user berdasarkan email
        # seperti User::findOrFail(email)->first()
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                # jika password benar, maka login
                # flash digunakan untuk menampilkan flash message seperti session error pada laravel
                flash('Login Success!', category='success')
                # remember true : menyimpan data user sampai session di clear/logout
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Login Failed!', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", text="Testing passing variable", user=current_user)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password2')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists', category='error')
            # jika panjang email adalah 4 karakter lebih
        elif len(email) < 4:
            flash('Email must be greater than 3 character', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character', category='error')
        elif password1 != password2:
            flash('Password don\'t match', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 character', category='error')
        else:
            # add user to database
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()

            # remember true : menyimpan data user sampai session di clear/logout
            login_user(user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)


@auth.route('/logout')
# seperti auth() pada laravel untuk check user sudah login atau belum
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
