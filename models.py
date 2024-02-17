from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4 

db = SQLAlchemy()

def get_uuid():
    return uuid4().hex

class Mypot(db.Model):
    __tablename__ = 'honeypot'
    ID = db.Column(db.Integer,primary_key=True)
    type = db.Column(db.String(255))
    alert = db.Column(db.String(255))
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    ip_attacker = db.Column(db.String(255))
    ip_server = db.Column(db.String(255))
    protocol = db.Column(db.String(255))
    comment = db.Column(db.String(255))

