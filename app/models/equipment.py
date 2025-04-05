from app import db 

class Equipments(db.Model):
   __tablename__ = 'equipment'
   idEquipment = db.Column(db.Integer, primary_key=True)
   brandEquipment = db.Column(db.String(255), nullable=False)
   codeEquipment = db.Column(db.String(255), unique=True, nullable=False)
   accassoriesEquipment = db.Column(db.String(255), nullable=False)
   apprenticeId = db.Column(db.Integer, db.ForeignKey('apprentice.idApprentice'), nullable = True)
   instructorId = db.Column(db.Integer, db.ForeignKey('instructor.idInstructor'), nullable = True)
   
   instructor = db.relationship("Instructors", back_populates="equipment")
   apprentice = db.relationship("Apprentices", back_populates="equipment")
   record = db.relationship("Records", back_populates="equipment")
   recordsIn = db.relationship("RecordsIn", back_populates="equipment")
   
   