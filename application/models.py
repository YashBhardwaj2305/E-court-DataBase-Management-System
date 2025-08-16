from .database import db
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError
import phonenumbers
from datetime import datetime


class Case_details(db.Model):
    __tablename__ = 'case_details'
    cnr_no = db.Column(db.String(16), primary_key=True)
    status_id = db.Column(db.String(10), db.ForeignKey('case_history.status_id'))
    case_no = db.Column(db.String(50), db.ForeignKey('court_details.case_no'))
    status = db.Column(db.String(20))
    fir_no = db.Column(db.String(50), db.ForeignKey('police_station.fir_no'))
    file_name = db.Column(db.String(100), db.ForeignKey('prosecutor.file_name'))

    # Relationships
    case_history = db.relationship('case_history', backref='case_details', uselist=False, foreign_keys=[status_id])
    prosecutor = db.relationship('prosecutor', backref='case_details', uselist=False, foreign_keys=[file_name])
    police_station = db.relationship('police_station', backref='case_details', uselist=False, foreign_keys=[fir_no])
    court_details = db.relationship('court_details', backref='case_details', uselist=False, foreign_keys=[case_no])

class prosecutor(db.Model):
    __tablename__ = 'prosecutor'
    file_name = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    sex = db.Column(db.String(10))
    address = db.Column(db.String(255))
    cnr_no = db.Column(db.String(16), db.ForeignKey('case_details.cnr_no'))

    # Multi-valued fields
    phone_numbers = db.relationship('phone_numbers', backref='prosecutor', cascade="all, delete-orphan")

class police_station(db.Model):
    __tablename__ = 'police_station'
    fir_no = db.Column(db.String(50), primary_key=True)
    fir_date = db.Column(db.Date)
    station_name = db.Column(db.String(100))
    inspector_name = db.Column(db.String(100))
    cnr_no = db.Column(db.String(16), db.ForeignKey('case_details.cnr_no'))

class case_history(db.Model):
    __tablename__ = 'case_history'
    status_id = db.Column(db.String(10), primary_key=True)
    cnr_no = db.Column(db.String(16), db.ForeignKey('case_details.cnr_no'))
    incident_date = db.Column(db.Date)
    incident_time = db.Column(db.Time)

    incident_location = db.Column(db.String(100))  # Updated location field to "incident_location"
    defence_name = db.Column(db.String(100))

    # Establishing relationships for multi-valued attributes
    witnesses = db.relationship('witnesses', backref='case_history', cascade="all, delete-orphan")
    acts = db.relationship('acts', backref='case_history', cascade="all, delete-orphan")
    sections = db.relationship('sections', backref='case_history', cascade="all, delete-orphan")

class acts(db.Model):
    __tablename__ = 'acts'
    id = db.Column(db.Integer, primary_key=True)
    status_id = db.Column(db.String(10), db.ForeignKey('case_history.status_id'))
    act_name = db.Column(db.String(100), nullable=False)

class sections(db.Model):
    __tablename__ = 'sections'
    id = db.Column(db.Integer, primary_key=True)
    status_id = db.Column(db.String(10), db.ForeignKey('case_history.status_id'))
    section_name = db.Column(db.String(100), nullable=False)

class witnesses(db.Model):
    __tablename__ = 'witnesses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    status_id = db.Column(db.String(100), db.ForeignKey('case_history.status_id'))  # Foreign key referencing the file_name

class court_details(db.Model):
    __tablename__ = 'court_details'
    case_no = db.Column(db.String(50), primary_key=True)
    cnr_no = db.Column(db.String(16), db.ForeignKey('case_details.cnr_no'))
    court_id = db.Column(db.String(100))
    lawyer_id = db.Column(db.String(100))
    judge_id = db.Column(db.String(100))
    hearing_date = db.Column(db.Date)
    court_location = db.Column(db.String(100))  # Updated location field to "court_location"

class phone_numbers(db.Model):
    __tablename__ = 'phone_numbers'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20))
    file_name = db.Column(db.String(100), db.ForeignKey('prosecutor.file_name'))  # Foreign key referencing the file_name

class users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)

    # def __init__(self, email, password):
    #     # Validate and set the email
    #     try:
    #         valid = validate_email(email)
    #         self.email = valid.email  # Store validated email
    #     except EmailNotValidError as e:
    #         raise ValueError(f"Invalid email address: {str(e)}")

    #     # Set the password using hashing
    #     self.set_password(password)

    # def set_password(self, password):
    #     """Hashes and sets the user's password."""
    #     self.password_hash = generate_password_hash(password)

    # def check_password(self, password):
    #     """Checks if the provided password matches the stored hash."""
    #     return check_password_hash(self.password_hash, password)

    # def __repr__(self):
    #     return f"<User {self.email}>"

class officials(db.Model):
    __tablename__ = 'officials'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    login_key = db.Column(db.String(50), nullable=False)
    registered_by_head = db.Column(db.Boolean, default=False)  # Indicates if registered by head

    # def check_login_key(self, login_key):
    #     return self.login_key == login_key

class head(db.Model):
    __tablename__ = 'head'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False, default='adminhead@gmail.com')
    password_hash = db.Column(db.String(128), nullable=False, default=generate_password_hash('adminhead'))
    is_single_user = db.Column(db.Boolean, default=True)  # Restrict to single user login

    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)

    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)