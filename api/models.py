from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


db = SQLAlchemy()


class HouseHold(db.Model):
    __tablename__ = 'household'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    type = db.Column(db.Enum('HDB', 'Condominium',
                             'Landed', name='housing_types'))


class FamilyMember(db.Model):
    __tablename__ = 'family_member'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.Enum('Male', 'Female'))

    # Assumes in this case that a person is either single or married
    marital_status = db.Column(db.Enum('Single', 'Married'))

    spouse_name = db.Column(db.String(100))
    occupation_type = db.Column(db.Enum('Unemployed', 'Student', 'Employed'))
    annual_income = db.Column(db.Numeric(10, 2))
    dob = db.Column(db.Date, nullable=False)
