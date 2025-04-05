from flask import Blueprint, render_template, request, redirect, url_for
from app.models.equipment import Equipments
from app.models.apprentice import Apprentices
from app.models.instrutor import Instructors
from flask_login import current_user
from app import db

bp = Blueprint('equipment', __name__)

@bp.route('/equipment')
def index():
    data = Equipments.query.all()   
    return render_template('equipment/index.html', data=data)

@bp.route('/equipment/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        brandEquipment = request.form['brandEquipment']
        codeEquipment = request.form['codeEquipment']
        accassoriesEquipment = request.form['accassoriesEquipment']
        apprenticeId = request.form['apprenticeId'] 
        instructorId = request.form['instructorId']       
        newEquipment = Equipments(brandEquipment=brandEquipment, codeEquipment=codeEquipment, accassoriesEquipment=accassoriesEquipment, apprenticeId=apprenticeId, instructorId=instructorId )
        db.session.add(newEquipment)
        db.session.commit()
        
        return redirect(url_for('equipment.index'))
    
    adata = Apprentices.query.all()
    idata = Instructors.query.all()
    return render_template('equipment/add.html', adata = adata, idata=idata)

@bp.route('/equipment/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    equipment= Equipments.query.get_or_404(id)
    apprentices = Apprentices.query.all()

    if request.method == 'POST':
        equipment.brandEquipment = request.form['brandEquipment']
        equipment.codeEquipment =request.form['codeEquipment']
        equipment.accassoriesEquipment= request.form ['accassoriesEquipment']
        equipment.apprenticeId= request.form ['apprenticeId']
        db.session.commit()        
        return redirect(url_for('equipment.index'))

    return render_template('equipment/edit.html', equipment=equipment, apprentices = apprentices)

@bp.route('/equipment/delete/<int:id>')
def delete(id):
   equipment = Equipments.query.get_or_404(id)
   
   db.session.delete(equipment)
   db.session.commit()
   
   return redirect(url_for('equipment.index'))