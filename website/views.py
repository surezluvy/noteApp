# untuk menyimpan routes
# blueprint harus di daftarkan di __init__.py

# menyatakan bahwa file ini adalah blueprint
# dimana blueprint adalah has bunch of roots inside
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

# views bebas menggunakan apa saja, tetapi harus dengan paramater __name__
views = Blueprint('views', __name__)


# @nama_blueprint('url')
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()

            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)

    if note:
        # cek apakah note itu milik user yang sedang login
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    # mengirim return kosong, requirement dari flask jadi mungkin harus ada
    return jsonify({})

@views.route('/delete', methods=['GET'])
def deleteNote():
    id = request.args.get('id')
    note = Note.query.get(id)

    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash('Note deleted!', category='success')
    return redirect(url_for('views.home'))

@views.route('/edit', methods=['POST'])
def updateNote():
    id = request.args.get('id')
    note = Note.query.get(id)

    if note:
        data = request.form.get('data')
        db.session.query(Note).filter(Note.id == id).update({'data': data})
        db.session.commit()

    return redirect(url_for('views.home'))