from flask import Flask, render_template, redirect, url_for, flash, request
from config import Config
from models import db, ZinaraFund, DevolutionFund, Business, Audit, ResourceLog, Investigation, FraudAlert, SecuritySystem, PhysicalSecurity, EmergencyResponse, TrainingAwareness

from datetime import date
from collections import Counter
from decimal import Decimal

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    @app.route('/')
    def index():
        return redirect(url_for('dashboard'))

    @app.route('/dashboard')
    def dashboard():
        today = date.today()
        businesses = Business.query.all()
        overdue_businesses = [b for b in businesses if b.renewal_date < today]
        compliant_count = len(businesses) - len(overdue_businesses)
        overdue_count = len(overdue_businesses)

        audits = Audit.query.filter_by(status='pending').all()
        audits_count = len(audits)
        open_incidents_count = Investigation.query.filter_by(status='open').count()
        open_fraud_alerts_count = FraudAlert.query.filter_by(status='open').count()
        pending_security_count = SecuritySystem.query.filter_by(status='pending').count()
        high_risk_facilities = PhysicalSecurity.query.filter_by(risk_level='high').count()
        active_emergency_plans = EmergencyResponse.query.filter_by(status='active').count()

        compliance_rate = round((compliant_count / len(businesses) * 100) if businesses else 0, 1)
        recent_audits = Audit.query.order_by(Audit.date.desc()).limit(5).all()
        return render_template('index_fixed.html', today=today, businesses=businesses, compliant_count=compliant_count, overdue_count=overdue_count, audits_count=audits_count, open_incidents_count=open_incidents_count, open_fraud_alerts_count=open_fraud_alerts_count, pending_security_count=pending_security_count, high_risk_facilities=high_risk_facilities, active_emergency_plans=active_emergency_plans, compliance_rate=compliance_rate, recent_audits=recent_audits)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            flash('Logged in successfully (demo). Use any credentials.')
            return redirect(url_for('dashboard'))
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        flash('Logged out.')
        return redirect(url_for('login'))

    @app.route('/licenses', methods=['GET', 'POST'])
    def licenses():
        if request.method == 'POST':
            action = request.form.get('action')
            if action == 'add':
                business = Business(
                    name=request.form['name'],
                    type=request.form['type'],
                    license_date=date.fromisoformat(request.form['license_date']),
                    renewal_date=date.fromisoformat(request.form['renewal_date'])
                )
                db.session.add(business)
                db.session.commit()
                flash('Business added successfully!')
                return redirect(url_for('licenses'))
            elif action == 'delete':
                business_id = int(request.form['business_id'])
                business = Business.query.get_or_404(business_id)
                db.session.delete(business)
                db.session.commit()
                flash('Business deleted successfully!')
                return redirect(url_for('licenses'))
            elif action == 'edit':
                business_id = int(request.form['business_id'])
                business = Business.query.get_or_404(business_id)
                business.name = request.form['name']
                business.type = request.form['type']
                business.license_date = date.fromisoformat(request.form['license_date'])
                business.renewal_date = date.fromisoformat(request.form['renewal_date'])
                db.session.commit()
                flash('Business updated successfully!')
                return redirect(url_for('licenses'))
        businesses = Business.query.all()
        return render_template('licenses.html', businesses=businesses)



    @app.route('/audits')
    def audits():
        audits = Audit.query.all()
        return render_template('audits.html', audits=audits)

    @app.route('/incidents', methods=['GET', 'POST'])
    def incidents():
        if request.method == 'POST':
            incident = Investigation(
                date_opened=date.fromisoformat(request.form['date_opened']),
                type=request.form['type'],
                description=request.form['description'],
                loss_amount=Decimal(request.form.get('loss_amount', '0')),
                vehicle_involved=request.form.get('vehicle_involved', ''),
                status='open'
            )
            db.session.add(incident)
            db.session.commit()
            flash('Investigation opened successfully.')
            return redirect(url_for('incidents'))
        incidents = Investigation.query.order_by(Investigation.date_opened.desc()).all()
        return render_template('incidents.html', incidents=incidents)

    @app.route('/fraud')
    def fraud():
        fraud_alerts = FraudAlert.query.order_by(FraudAlert.date_detected.desc()).all()
        return render_template('fraud.html', fraud_alerts=fraud_alerts)

    @app.route('/resources')
    def resources():
        logs = ResourceLog.query.order_by(ResourceLog.date.desc()).all()
        return render_template('resources.html', logs=logs)

    @app.route('/security_systems')
    def security_systems():
        systems = SecuritySystem.query.order_by(SecuritySystem.date_assessed.desc()).all()
        return render_template('security_systems.html', security_systems=systems)

    @app.route('/physical_security')
    def physical_security():
        plans = PhysicalSecurity.query.order_by(PhysicalSecurity.date_planned.desc()).all()
        return render_template('physical_security.html', physical_security=plans)

    @app.route('/emergency_response', methods=['GET', 'POST'])
    def emergency_response():
        if request.method == 'POST':
            procedure = EmergencyResponse(
                date_created=date.today(),
                procedure_type=request.form['procedure_type'],
                facility=request.form['facility'],
                steps=request.form['steps'],
                last_drill_date=date.fromisoformat(request.form['last_drill_date']) if request.form.get('last_drill_date') else None,
                status=request.form.get('status', 'active')
            )
            db.session.add(procedure)
            db.session.commit()
            flash('Emergency procedure created successfully.')
            return redirect(url_for('emergency_response'))
        procedures = EmergencyResponse.query.order_by(EmergencyResponse.date_created.desc()).all()
        return render_template('emergency_response.html', emergency_responses=procedures)

    @app.route('/training_awareness', methods=['GET', 'POST'])
    def training_awareness():
        if request.method == 'POST':
            session = TrainingAwareness(
                date_conducted=date.fromisoformat(request.form['date_conducted']),
                type=request.form['type'],
                attendees_count=int(request.form['attendees_count']),
                topics_covered=request.form.get('topics_covered', ''),
                trainer=request.form.get('trainer', ''),
                status=request.form.get('status', 'completed')
            )
            db.session.add(session)
            db.session.commit()
            flash('Training session recorded successfully.')
            return redirect(url_for('training_awareness'))
        trainings = TrainingAwareness.query.order_by(TrainingAwareness.date_conducted.desc()).all()
        return render_template('training_awareness.html', trainings=trainings)

    @app.route('/analytics')
    def analytics():
        # Simple test data for guaranteed charts
        analytics_data = {
            'compliance': {'labels': ['Compliant', 'Overdue'], 'values': [85, 15]},
            'audits': {'labels': ['Finance', 'Revenue Leak'], 'values': [12, 8]},
            'businessTypes': {'labels': ['Shop', 'Bar', 'Nightclub'], 'values': [45, 30, 25]},
            'totalFraudLoss': 15000
        }
        return render_template('analytics.html', analytics_data=analytics_data)

    return app
