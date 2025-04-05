from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.roomLoan import RoomsLoans
from app.models.instrutor import Instructors
from app.models.room import Rooms
from app.models.wachiman import Wachiman
from app import db
from datetime import datetime
import pytz

bp = Blueprint('roomLoan', __name__)

@bp.route('/roomLoan')
def index():
    roomLoan = RoomsLoans.query.all()
    return render_template('roomLoan/index.html', roomLoan=roomLoan)

@bp.route('/roomLoan/add', methods=['GET', 'POST'])
def add():
    colombia_tz = pytz.timezone('America/Bogota')
    if request.method == 'POST':
        returnDate = request.form['datetime']
        instructorId = request.form['instrutorId']
        wachimanId = request.form['wachimanId']
        roomId = request.form['roomId']
        date = datetime.now(colombia_tz)
        return_date = datetime.strptime(returnDate, "%Y-%m-%dT%H:%M") if returnDate else None
        
        newLoan = RoomsLoans(instructorId=instructorId, date=date, wachimanId=wachimanId, roomId=roomId, returnDate=return_date)
        db.session.add(newLoan)
        db.session.commit()
        
        return redirect(url_for('roomLoan.index'))
    
    instructors = Instructors.query.all()
    rooms = Rooms.query.all()
    wachiman = Wachiman.query.all()
    return render_template('roomLoan/add.html', instructors=instructors, rooms=rooms, wachiman=wachiman)

@bp.route('/roomLoan/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    roomLoan = RoomsLoans.query.get_or_404(id)
    instructor = Instructors.query.all()
    room = Rooms.query.all()
    wachiman = Wachiman.query.all()
    if request.method == 'POST':
        try:
            # 🔹 Convertir la fecha de string a datetime
            roomLoan.date = datetime.strptime(request.form['date'], "%Y-%m-%dT%H:%M")
            roomLoan.returnDate = datetime.strptime(request.form['returnDate'], "%Y-%m-%dT%H:%M")
            roomLoan.instructorId = request.form['instructorId']
            roomLoan.wachimanId = request.form['wachimanId']
            roomLoan.roomId = request.form['roomId']
            db.session.commit()
            return redirect(url_for('roomLoan.index'))
        
        except ValueError as e:
            flash(f"Error al actualizar préstamo: {str(e)}", "danger")
            return redirect(url_for('roomLoan.edit', id=id))
    

    return render_template('roomLoan/edit.html', roomLoan=roomLoan, instructors=instructor, rooms=room, wachiman=wachiman)

@bp.route('/delete/<int:id>')
def delete(id):
    roomLoan = RoomsLoans.query.get_or_404(id)
    db.session.delete(roomLoan)
    db.session.commit()
    return redirect(url_for('roomLoan.index'))

@bp.route('/devolver/<int:id>')
def devolver(id):
     # 1. Buscar el préstamo en la base de datos
    prestamo = RoomsLoans.query.get_or_404(id)
    # 2. Actualizar la fecha de devolución con la fecha/hora actual
    prestamo.returnDate = datetime.now()
    # 3. Guardar cambios
    db.session.commit()
    # 4. Redirigir a la vista de la lista de préstamos
    return redirect(url_for('roomLoan.index'))