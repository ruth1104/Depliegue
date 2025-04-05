from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.apprentice import Apprentices
from app.models.equipment import Equipments
from app.models.wachiman import Wachiman
from app.models.record import Records
from app import db
from datetime import datetime
import pytz


bp = Blueprint('record', __name__)

@bp.route('/record')
def index():
    data = Records.query.all()
    return render_template('record/index.html', data=data)

@bp.route('/record/add', methods=['GET', 'POST'])
def add():
    colombia_tz = pytz.timezone('America/Bogota')
    if request.method == 'POST':
        
        apprenticeId = request.form['apprenticeId']
        wachimanId = request.form['wachimanId']
        equipmentId = request.form['equipmentId']
        dataEntry = datetime.now(colombia_tz)
        dataExit = datetime.now(colombia_tz)
        
        newRecords = Records(apprenticeId=apprenticeId, dataEntry=dataEntry, wachimanId=wachimanId, equipmentId=equipmentId, dataExit=dataExit)
        db.session.add(newRecords)
        db.session.commit()
        
        return redirect(url_for('record.index'))
    
    apprentice = Apprentices.query.all()
    equipment = Equipments.query.all()
    wachiman = Wachiman.query.all()
    return render_template('record/add.html', apprentices=apprentice, equipments=equipment, wachimanes=wachiman)

@bp.route('/record/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    colombia_tz = pytz.timezone('America/Bogota')
    record = Records.query.get_or_404(id)
    apprentice = Apprentices.query.all()
    equipment = Equipments.query.all()
    wachiman = Wachiman.query.all()
    
    if request.method == 'POST':
        try:
            # 🔹 Convertir la fecha de string a datetime
            
            record.dataEntry = datetime.now(colombia_tz)
            record.dataExit = datetime.strptime(request.form['dataExit'], "%Y-%m-%dT%H:%M")
            record.apprenticeId = request.form['apprenticeId']
            record.equipmentId = request.form['equipmentId']
            record.wachimanId = request.form['wachimanId']
            db.session.commit()
            return redirect(url_for('record.index'))
        
        except ValueError as e:
            flash(f"Error al actualizar préstamo: {str(e)}", "danger")
            return redirect(url_for('record.edit', id=id))
    

    return render_template('record/edit.html', record=record, apprentice=apprentice, equipment=equipment, wachiman=wachiman)

@bp.route('/recorsd/delete/<int:id>')
def delete(id):
    record = Records.query.get_or_404(id)
    
    db.session.delete(record)
    db.session.commit()
    
    return redirect(url_for('record.index'))

@bp.route('/salida/<int:id>')
def salida(id):
    prestamo = Records.query.get_or_404(id)
    
    prestamo.dataExit = datetime.now()
    db.session.commit()
  
    return redirect(url_for('record.index'))