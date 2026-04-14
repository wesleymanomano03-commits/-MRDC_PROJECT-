from flask_sqlalchemy import SQLAlchemy
from datetime import date, timedelta
from decimal import Decimal

db = SQLAlchemy()

class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # shop, bar, nightclub
    license_date = db.Column(db.Date, nullable=False)
    renewal_date = db.Column(db.Date, nullable=False)






class Audit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(20), default='finance')  # finance, revenue_leak
    details = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, completed


class ResourceLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    item = db.Column(db.String(50), nullable=False)  # fuel, equipment, materials
    quantity_used = db.Column(db.Numeric(10,2))
    notes = db.Column(db.Text)

class Investigation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_opened = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(20), default='theft')  # theft, fraud, accident, safety, security_breach, emergency, other
    description = db.Column(db.Text, nullable=False)
    loss_amount = db.Column(db.Numeric(12,2), default=Decimal('0.00'))
    vehicle_involved = db.Column(db.String(50))
    status = db.Column(db.String(20), default='open')  # open, closed
    findings = db.Column(db.Text)
    recommendations = db.Column(db.Text)

class ZinaraFund(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_received = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(30), nullable=False)  # roads, fuel, audits
    amount = db.Column(db.Numeric(12,2), nullable=False)
    notes = db.Column(db.Text)

class FraudAlert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_detected = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(20), default='revenue_leak')  # revenue_leak, corruption, other
    description = db.Column(db.Text, nullable=False)
    amount_lost = db.Column(db.Numeric(12,2), default=Decimal('0.00'))
    status = db.Column(db.String(20), default='open')  # open, closed

class DevolutionFund(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_received = db.Column(db.Date, nullable=False)
    sector = db.Column(db.String(30), nullable=False)  # schools, community, health, roads, others
    amount = db.Column(db.Numeric(12,2), nullable=False)
    notes = db.Column(db.Text)

class SecuritySystem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_assessed = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(20), nullable=False)  # access_control, key_control, cctv
    facility = db.Column(db.String(50), nullable=False)  # head_office, warehouse, rural_service_center
    effectiveness_score = db.Column(db.Integer, nullable=False)  # 1-10
    issues = db.Column(db.Text)
    recommendations = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')  # active, pending, review

class PhysicalSecurity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_planned = db.Column(db.Date, nullable=False)
    facility = db.Column(db.String(50), nullable=False)
    measures = db.Column(db.String(100), nullable=False)  # access_lighting, fencing, patrols
    risk_level = db.Column(db.String(20), nullable=False)  # low, medium, high
    assets_protected = db.Column(db.Text)
    status = db.Column(db.String(20), default='planned')  # planned, implemented, review

class EmergencyResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.Date, nullable=False)
    procedure_type = db.Column(db.String(30), nullable=False)  # security_incident, fire, threat
    facility = db.Column(db.String(50), nullable=False)
    steps = db.Column(db.Text, nullable=False)
    last_drill_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='active')  # active, draft, archived

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='user')  # user, admin

    def __repr__(self):
        return f'<User {self.username}>'


class TrainingAwareness(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_conducted = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(50), nullable=False)  # crime_prevention, health_safety, fire_evacuation, risk_control
    attendees_count = db.Column(db.Integer, nullable=False)
    topics_covered = db.Column(db.Text)
    trainer = db.Column(db.String(100))
    status = db.Column(db.String(20), default='completed')  # scheduled, completed, cancelled

