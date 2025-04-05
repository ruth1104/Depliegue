from app import db

class Rooms(db.Model):
   __tablename__ = 'room'
   idRoom = db.Column(db.Integer, primary_key=True)
   nameRoom = db.Column(db.String(255), nullable=False)
   
   roomLoan = db.relationship("RoomsLoans", back_populates="room")