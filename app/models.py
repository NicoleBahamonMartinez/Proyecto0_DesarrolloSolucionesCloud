# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

import enum

class Categorias(enum.IntEnum):
    Conferencia = 1
    Seminario = 2
    Congreso = 3
    Curso = 4

class IntEnum(db.TypeDecorator):
    impl = db.Integer

    def __init__(self, enumtype, *args, **kwargs):
        super(IntEnum, self).__init__(*args, **kwargs)
        self._enumtype = enumtype

    def process_bind_param(self, value, dialect):
        if isinstance(value, int):
            return value

        return value.value

    def process_result_value(self, value, dialect):
        return self._enumtype(value)


class Employee(UserMixin, db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    events = db.relationship('Evento', backref='employees',
                                lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee: {}>'.format(self.username)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))

class Evento(db.Model):

    __tablename__ = 'eventos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(60), unique=True)
    categoria = db.Column(IntEnum(Categorias),default=Categorias.Conferencia)
    lugar=db.Column(db.String(80))
    direccion=db.Column(db.String(80))
    fechaInicio=db.Column(db.DateTime)
    fechaFin=db.Column(db.DateTime)
    presencial=db.Column(db.Boolean)
    employee_id=db.Column(db.Integer,db.ForeignKey('employees.id'))

    def __repr__(self):
        return '<Department: {}>'.format(self.name)




