from flask import Blueprint, render_template, request, redirect, url_for
from app.models.room import Rooms
from flask_login import login_required
from app import db

bp = Blueprint('room', __name__)

@bp.before_request
@login_required
def before_request():
    pass

@bp.route('/room')
def index():
    data = Rooms.query.all()   
    return render_template('room/index.html', data=data)

@bp.route('/room/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nameRoom = request.form['nameRoom']
        
        newRoom = Rooms(nameRoom=nameRoom)
        db.session.add(newRoom)
        db.session.commit()
        
        return redirect(url_for('room.index'))

    return render_template('room/add.html')

@bp.route('/room/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    room= Rooms.query.get_or_404(id)

    if request.method == 'POST':
        room.nameRoom = request.form['nameRoom']
        db.session.commit()        
        return redirect(url_for('room.index'))

    return render_template('room/edit.html', room=room)

@bp.route('/room/delete/<int:id>')
def delete(id):
   room = Rooms.query.get_or_404(id)
   
   db.session.delete(room)
   db.session.commit()
   
   return redirect(url_for('room.index'))