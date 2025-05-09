from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.instrutor import Instructors
from app.models.equipment import Equipments
from app.models.wachiman import Wachiman
from app.models.recordsIn import RecordsIn
from app.models.user import User
from flask_login import login_required,current_user
from app import db
from datetime import datetime
import pytz


bp = Blueprint('recordsIn', __name__)

@bp.before_request
@login_required
def before_request():
    pass

@bp.route('/recordsIn')
def index():
    data = RecordsIn.query.all()
    return render_template('recordsIn/index.html', data=data)

@bp.route('/recordsIn/add', methods=['GET', 'POST'])
def add():
    colombia_tz = pytz.timezone('America/Bogota')
    if request.method == 'POST':
        
        instructorId = request.form['instructorId']
        wachimanId = request.form['wachimanId']
        equipmentId = request.form['equipmentId']
        dataEntry = datetime.now(colombia_tz)
        dataExit = datetime.now(colombia_tz)
        
        newRecordsIn = RecordsIn(instructorId=instructorId, dataEntry=dataEntry, wachimanId=wachimanId, equipmentId=equipmentId, dataExit=dataExit)
        db.session.add(newRecordsIn)
        db.session.commit()
        
        return redirect(url_for('recordsIn.index'))
    
    instructor = Instructors.query.all()
    equipment = Equipments.query.all()
    wachiman = Wachiman.query.all()
    return render_template('recordsIn/add.html', instructor=instructor, equipments=equipment, wachimanes=wachiman)

@bp.route('/recordIn/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    colombia_tz = pytz.timezone('America/Bogota')
    recordsIn = RecordsIn.query.get_or_404(id)
    instructor = Instructors.query.all()
    equipment = Equipments.query.all()
    wachiman = Wachiman.query.all()
    
    if request.method == 'POST':
        try:
            # 🔹 Convertir la fecha de string a datetime
            
            recordsIn.dataEntry = datetime.now(colombia_tz)
            recordsIn.dataExit = datetime.strptime(request.form['dataExit'], "%Y-%m-%dT%H:%M")
            recordsIn.instructorId = request.form['instructorId']
            recordsIn.equipmentId = request.form['equipmentId']
            recordsIn.wachimanId = request.form['wachimanId']
            db.session.commit()
            return redirect(url_for('recordsIn.index'))
        
        except ValueError as e:
            flash(f"Error al actualizar préstamo: {str(e)}", "danger")
            return redirect(url_for('recordsIn.edit', id=id))
    

    return render_template('recordsIn/edit.html', recordsIn=recordsIn, instructor=instructor, equipment=equipment, wachiman=wachiman)

@bp.route('/delete/registro_instructor/<int:id>')
def delete(id):
    recordsIn = RecordsIn.query.get_or_404(id)
    
    db.session.delete(recordsIn)
    db.session.commit()
    
    return redirect(url_for('recordsIn.index'))

@bp.route('/salida/registro_instructor/<int:id>')
def salida(id):
    prestamo = RecordsIn.query.get_or_404(id)
    
    prestamo.dataExit = datetime.now()
    db.session.commit()
  
    return redirect(url_for('recordsIn.index'))

@bp.route('/recordsIn/get_data_by_qr', methods=['GET'])
def get_data_by_qr():
    instructor_id = request.args.get('equipmentId')
    equipment_id = request.args.get('equipmentId')
    user_id = request.args.get('current_user.idUser')
    
    record = RecordsIn.query.filter_by(instructor_id=instructor_id, equipment_id=equipment_id, user_id=user_id).all()

    records_data = [{
        'idRecords': record.idRecords,
        'dataEntry': record.dataEntry,
        'dataExit': record.dataExit,
        'instructor': {'nameInstructor': record.instructor.nameInstructor},
        'equipment': {'codeEquipment': record.equipment.codeEquipment},
        'user': {'username': record.user.username}
    } for record in records_data]
      

    return redirect('/addconqr')

@bp.route('/recordsIn/addqr/<int:id>', methods=['GET'])
def addconqr(id):
    equipo = Equipments.query.get_or_404(id)
    colombia_tz = pytz.timezone('America/Bogota')

    instructorId = equipo.instructorId
    userId = current_user.idUser
    equipmentId = equipo.idEquipment
    dataEntry = datetime.now(colombia_tz)
    dataExit = datetime.now(colombia_tz)

    newRecord = RecordsIn(
        instructorId=instructorId,
        dataEntry=dataEntry,
        userId=userId,
        equipmentId=equipmentId,
        dataExit=dataExit
    )
    db.session.add(newRecord)
    db.session.commit()

    return redirect(url_for('recordsIn.index'))