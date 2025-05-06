from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash
from app.models.apprentice import Apprentices
from app.models.equipment import Equipments
from app.models.wachiman import Wachiman
from app.models.record import Records
from app import db
from flask_login import login_required
from datetime import datetime
import pytz


bp = Blueprint('record', __name__)

@bp.before_request
@login_required
def before_request():
    pass

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
    return redirect(url_for('record.add', success='1'))

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



@bp.route('/record/get_data_by_qr', methods=['GET'])
def get_data_by_qr():
    apprentice_id = request.args.get('apprenticeId')
    equipment_id = request.args.get('equipmentId')
    wachiman_id = request.args.get('wachimanId')
    
    record = Records.query.filter_by(apprentice_id=apprentice_id, equipment_id=equipment_id, wachiman_id=wachiman_id).all()

    records_data = [{
        'idRecords': record.idRecords,
        'dataEntry': record.dataEntry,
        'dataExit': record.dataExit,
        'apprentice': {'nameApprentice': record.apprentice.nameApprentice},
        'equipment': {'codeEquipment': record.equipment.codeEquipment},
        'wachiman': {'nameWachiman': record.wachiman.nameWachiman}
    } for record in records_data]
      

    return redirect('/addconqr')

@bp.route('/record/addqr/<int:id>', methods=['GET'])
def addconqr(id):
    equipo = Equipments.query.get_or_404(id)
    colombia_tz = pytz.timezone('America/Bogota')

    apprenticeId = equipo.apprenticeId
    wachimanId = '1'
    equipmentId = equipo.idEquipment
    dataEntry = datetime.now(colombia_tz)
    dataExit = datetime.now(colombia_tz)

    newRecord = Records(
        apprenticeId=apprenticeId,
        dataEntry=dataEntry,
        wachimanId=wachimanId,
        equipmentId=equipmentId,
        dataExit=dataExit
    )
    db.session.add(newRecord)
    db.session.commit()

    return redirect(url_for('record.index'))
    
