from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import relationship


db = SQLAlchemy()


class HouseHold(db.Model):
    __tablename__ = 'household'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    type = db.Column(db.Enum('HDB', 'Condominium',
                             'Landed', name='housing_types'))
    family = db.relationship(
        'FamilyMember', backref=db.backref('household'), cascade='delete')

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        except SQLAlchemyError:
            db.session.rollback()

    def update(self):
        return db.session.commit()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()


class FamilyMember(db.Model):
    __tablename__ = 'family_member'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.Enum('Male', 'Female'), nullable=False)

    # Assumes in this case that a person is either single or married
    marital_status = db.Column(
        db.Enum('Single', 'Married', 'Widowed', 'Divorced'), nullable=False)
    spouse_name = db.Column(db.String(100))
    occupation_type = db.Column(
        db.Enum('Unemployed', 'Student', 'Employed'), nullable=False)
    annual_income = db.Column(db.Numeric(10, 2))
    dob = db.Column(db.Date, nullable=False)
    household_id = db.Column(db.Integer(), db.ForeignKey('household.id'))

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            error = str(e.__dict__['orig'])
            db.session.rollback()
            return error
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            db.session.rollback()
            print(error)
            return error

    def update(self):
        return db.session.commit()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
