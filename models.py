from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    prioridad = db.Column(db.String(20), default='media')
    tecnico = db.Column(db.String(100), default='Sin asignar')
    estado = db.Column(db.String(20), default='abierto')
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    