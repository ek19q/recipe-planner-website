from flask import Blueprint, render_template,request, flash, jsonify
from flask_login import  login_required,  current_user
from .models import Note
from . import db 
import json

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", user=current_user)

@views.route('/user-profile', methods=['GET', 'POST'])
@login_required     # Requires user to be logged in to access this route
def user_profile():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash("Note is too short!", category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added!", category='success')
    return render_template("user_profile.html", user=current_user)  # Passes user to user_profile.html

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)     # Converts JSON to Python dictionary
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:     # Checks if note belongs to current user
            db.session.delete(note)
            db.session.commit()

    return jsonify({})  # Returns empty JSON object. This is because the frontend expects a response