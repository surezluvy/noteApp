# Menyimpan model untuk database

# import dari current folder (website) / __init__ (karena file ini otomatis dijalankan)
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# pada sqlalchemy, class dibuat dengan huruf capital di awal
# tetapi pada database, tabel dibuat dengan huruf kecil semua
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000))
    # func.now() ambil waktu sekarang dari sqlalchemy.sql
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# pada sqlalchemy, class dibuat dengan huruf capital di awal
# tetapi pada database, tabel dibuat dengan huruf kecil semua
# UserMixin bawaan flask_login
class User(db.Model, UserMixin):
    # db.tipe_data(panjang max)
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(20), unique=True)
    # menyimpan semua note yang dibuat oleh user ini
    # gunakan kapital di awal karena relationship
    notes = db.relationship('Note')