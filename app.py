from flask import Flask, render_template, redirect, url_for, flash, request
from config import Config
from models import db, User, ZinaraFund, DevolutionFund, Business, Payment, Audit, ResourceLog, Investigation, FraudAlert, SecuritySystem, PhysicalSecurity, EmergencyResponse, TrainingAwareness
from werkzeug.security import generate_password_hash, check_password_hash

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
    @login_required
    def dashboard():
        today = date.today()
        businesses = Business.query.all()
        overdue_businesses = [b for b in businesses if b.renewal_date < today]
        compliant_count = len(businesses) - len(overdue_businesses)
        overdue_count = len(overdue_businesses)
        total_owed = sum(float(b.balance) for b in businesses if hasattr(b, 'balance'))  # Safe access
        audits = Audit.query.filter_by(status='pending').all()
        audits_count = len(audits)
        open_incidents_count = Investigation.query.filter_by(status='open').count()
        open_fraud_alerts_count = FraudAlert.query.filter_by(status='open').count()
        pending_security_count = SecuritySystem.query.filter_by(status='pending').count()
        high_risk_facilities = PhysicalSecurity.query.filter_by(risk_level='high').count()
        active_emergency_plans = EmergencyResponse.query.filter_by(status='active').count()
        recent_payments = Payment.query.order_by(Payment.date.desc()).limit(5).all() if 'Payment' in globals() else []
        compliance_rate = round((compliant_count / len(businesses) * 100) if businesses else 0, 1)
        recent_audits = Audit.query.order_by(Audit.date.desc()).limit(5).all()
        current_user = User.query.get(session['user_id'])
        return render_template('index.html', today=today, businesses=businesses, compliant_count=compliant_count, overdue_count=overdue_count, total_owed=total_owed, audits_count=audits_count, open_incidents_count=open_incidents_count, open_fraud_alerts_count=open_fraud_alerts_count, pending_security_count=pending_security_count, high_risk_facilities=high_risk_facilities, active_emergency_plans=active_emergency_plans, recent_payments=recent_payments, compliance_rate=compliance_rate, recent_audits=recent_audits, current_user=current_user)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password_hash, password):
                session['user_id'] = user.id
                session['username'] = user.username
                flash(f'Welcome back, {user.username}!', 'success')
                return redirect(url_for('dashboard'))
            flash('Invalid username or password.', 'danger')
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('login.html')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return render_template('login.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return render_template('login.html')
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.clear()
        flash('Logged out successfully.')
        return redirect(url_for('login'))

    def login_required(f):
        from functools import wraps
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please login to access this page.', 'warning')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function

    @app.route('/licenses', methods=['GET', 'POST'])
    def licenses():
        if request.method == 'POST':
            action = request.form.get('action')
            if action == 'add':
                business = Business(
                    name=request.form['name'],
                    type=request.form['type'],
                    license_date=date.fromisoformat(request.form['license_date']),
                    renewal_date=date.fromisoformat(request.form['renewal_date']),
                    balance=Decimal(request.form.get('balance', '0'))
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
                business.balance = Decimal(request.form.get('balance', '0'))
                db.session.commit()
                flash('Business updated successfully!')
                return redirect(url_for('licenses'))
        businesses = Business.query.all()
        return render_template('licenses.html', businesses=businesses)

@app.route('/payments', methods=['GET', 'POST'])
    def payments():
        if request.method == 'POST':
            action = request.form.get('action')
            if action == 'add':
                payment = Payment(
                    date=date.fromisoformat(request.form['date']),
                    amount=Decimal(request.form['amount']),
                    business_id=int(request.form['business_id'])
                )
                db.session.add(payment)
                db.session.commit()
                flash('Payment added successfully!')
                return redirect(url_for('payments'))
            elif action == 'edit':
                payment_id = int(request.form['payment_id'])
                payment = Payment.query.get_or_404(payment_id)
                payment.date = date.fromisoformat(request.form['date'])
                payment.amount = Decimal(request.form['amount'])
                payment.business_id = int(request.form['business_id'])
                db.session.commit()
                flash('Payment updated successfully!')
                return redirect(url_for('payments'))
            elif action == 'delete':
                payment_id = int(request.form['payment_id'])
                payment = Payment.query.get_or_404(payment_id)
                db.session.delete(payment)
                db.session.commit()
                flash('Payment deleted successfully!')
                return redirect(url_for('payments'))
        payments = Payment.query.order_by(Payment.date.desc()).all()
        businesses = Business.query.all()  # for add/edit forms
        return render_template('payments.html', payments=payments, businesses=businesses)

    @app.route('/zinara', methods=['GET', 'POST'])
    def zinara():
        if request.method == 'POST':
            fund = ZinaraFund(
                date_received=date.fromisoformat(request.form['date_received']),
                category=request.form['category'],
                amount=Decimal(request.form['amount']),
                notes=request.form.get('notes', '')
            )
            db.session.add(fund)
            db.session.commit()
            flash('ZINARA fund added successfully.')
            return redirect(url_for('zinara'))
        funds = ZinaraFund.query.order_by(ZinaraFund.date_received.desc()).all()
        return render_template('zinara.html', funds=funds)

    @app.route('/devolution', methods=['GET', 'POST'])
    def devolution():
        if request.method == 'POST':
            fund = DevolutionFund(
                date_received=date.fromisoformat(request.form['date_received']),
                sector=request.form['sector'],
                amount=Decimal(request.form['amount']),
                notes=request.form.get('notes', '')
            )
            db.session.add(fund)
            db.session.commit()
            flash('Devolution fund added successfully.')
            return redirect(url_for('devolution'))
        funds = DevolutionFund.query.order_by(DevolutionFund.date_received.desc()).all()
        return render_template('devolution.html', funds=funds)

@app.route('/audits', methods=['GET', 'POST'])
    def audits():
        if request.method == 'POST':
            action = request.form.get('action')
            if action == 'add':
                audit = Audit(
                    date=date.fromisoformat(request.form['date']),
                    type=request.form['type'],
                    details=request.form['details'],
                    status=request.form.get('status', 'pending')
                )
                db.session.add(audit)
                db.session.commit()
                flash('Audit added successfully!')
                return redirect(url_for('audits'))
            elif action == 'edit':
                audit_id = int(request.form['audit_id'])
                audit = Audit.query.get_or_404(audit_id)
                audit.date = date.fromisoformat(request.form['date'])
                audit.type = request.form['type']
                audit.details = request.form['details']
                audit.status = request.form['status']
                db.session.commit()
                flash('Audit updated successfully!')
                return redirect(url_for('audits'))
            elif action == 'delete':
                audit_id = int(request.form['audit_id'])
                audit = Audit.query.get_or_404(audit_id)
                db.session.delete(audit)
                db.session.commit()
                flash('Audit deleted successfully!')
                return redirect(url_for('audits'))
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

    @app.route('/fraud', methods=['GET', 'POST'])
    def fraud():
        if request.method == 'POST':
            action = request.form.get('action', '')
            if action == 'add':
                alert = FraudAlert(
                    date_detected=date.fromisoformat(request.form.get('date_detected', date.today().strftime('%Y-%m-%d'))),
                    type=request.form['type'],
                    description=request.form['description'],
                    amount_lost=Decimal(request.form['amount_lost']),
                    status='open'
                )
                db.session.add(alert)
                db.session.commit()
                flash('Fraud alert raised successfully.')
            elif action == 'edit':
                alert_id = int(request.form['alert_id'])
                alert = FraudAlert.query.get_or_404(alert_id)
                alert.type = request.form['type']
                alert.description = request.form['description']
                alert.amount_lost = Decimal(request.form['amount_lost'])
                alert.status = request.form['status']
                db.session.commit()
                flash('Fraud alert updated successfully.')
            elif action == 'delete':
                alert_id = int(request.form['alert_id'])
                alert = FraudAlert.query.get_or_404(alert_id)
                db.session.delete(alert)
                db.session.commit()
                flash('Fraud alert deleted.')
            return redirect(url_for('fraud'))
        fraud_alerts = FraudAlert.query.order_by(FraudAlert.date_detected.desc()).all()
        return render_template('fraud.html', fraud_alerts=fraud_alerts)

@app.route('/resources', methods=['GET', 'POST'])
    def resources():
        if request.method == 'POST':
            action = request.form.get('action')
            if action == 'add':
                log = ResourceLog(
                    date=date.fromisoformat(request.form['date']),
                    item=request.form['item'],
                    quantity_used=Decimal(request.form.get('quantity_used', '0')),
                    notes=request.form['notes']
                )
                db.session.add(log)
                db.session.commit()
                flash('Resource log added!')
                return redirect(url_for('resources'))
        logs = ResourceLog.query.order_by(ResourceLog.date.desc()).all()
        return render_template('resources.html', logs=logs)

    @app.route('/security_systems', methods=['GET', 'POST'])
    def security_systems():
        if request.method == 'POST':
            system = SecuritySystem(
                date_assessed=date.fromisoformat(request.form['date_assessed']) if request.form.get('date_assessed') else date.today(),
                type=request.form['type'],
                facility=request.form['facility'],
                effectiveness_score=int(request.form['effectiveness_score']),
                issues=request.form.get('issues', ''),
                recommendations=request.form.get('recommendations', ''),
                status=request.form.get('status', 'active')
            )
            db.session.add(system)
            db.session.commit()
            flash('Security system assessed successfully.')
            return redirect(url_for('security_systems'))
        systems = SecuritySystem.query.order_by(SecuritySystem.date_assessed.desc()).all()
        return render_template('security_systems.html', security_systems=systems)

    @app.route('/physical_security', methods=['GET', 'POST'])
    def physical_security():
        if request.method == 'POST':
            plan = PhysicalSecurity(
                date_planned=date.fromisoformat(request.form['date_planned']) if request.form.get('date_planned') else date.today(),
                facility=request.form['facility'],
                measures=request.form['measures'],
                risk_level=request.form['risk_level'],
                assets_protected=request.form.get('assets_protected', ''),
                status=request.form.get('status', 'planned')
            )
            db.session.add(plan)
            db.session.commit()
            flash('Physical security plan created successfully.')
            return redirect(url_for('physical_security'))
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

    @app.route('/analytics')
    def analytics():
        payments_data = {
            'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'values': [850, 0, 1200, 0, 0, 200]
        }
        businesses = Business.query.all()
        today = date.today()
        overdue_businesses = [b for b in businesses if b.renewal_date < today]
        compliance_data = {
            'labels': ['Compliant', 'Overdue'],
            'values': [len(businesses) - len(overdue_businesses), len(overdue_businesses)]
        }
        audits_by_type = Counter([a.type for a in Audit.query.all()])
        audits_data = {
            'labels': list(audits_by_type.keys()),
            'values': list(audits_by_type.values())
        }
        business_types = Counter([b.type for b in businesses])
        business_types_data = {
            'labels': list(business_types.keys()),
            'values': list(business_types.values())
        }
        zinara_by_cat = Counter([f.category for f in ZinaraFund.query.all()])
        zinara_data = {
            'labels': list(zinara_by_cat.keys()),
            'values': [float(v) for v in zinara_by_cat.values()]
        }
        devolution_by_sector = Counter([f.sector for f in DevolutionFund.query.all()])
        devolution_data = {
            'labels': list(devolution_by_sector.keys()),
            'values': [float(v) for v in devolution_by_sector.values()]
        }
        incidents_by_type = Counter([i.type for i in Investigation.query.all()])
        incidents_data = {
            'labels': list(incidents_by_type.keys()),
            'values': list(incidents_by_type.values())
        }
        fraud_by_type = Counter([f.type for f in FraudAlert.query.all()])
        fraud_data = {
            'labels': list(fraud_by_type.keys()),
            'values': list(fraud_by_type.values())
        }
        security_by_type = Counter([s.type for s in SecuritySystem.query.all()])
        security_data = {
            'labels': list(security_by_type.keys()),
            'values': list(security_by_type.values())
        }
        physical_risk = Counter([p.risk_level for p in PhysicalSecurity.query.all()])
        risk_data = {
            'labels': list(physical_risk.keys()),
            'values': list(physical_risk.values())
        }
        emergency_by_type = Counter([e.procedure_type for e in EmergencyResponse.query.all()])
        emergency_data = {
            'labels': list(emergency_by_type.keys()),
            'values': list(emergency_by_type.values())
        }
        total_fraud_loss = sum(float(f.amount_lost) for f in FraudAlert.query.all())
        analytics_data = {
            'payments': payments_data,
            'compliance': compliance_data,
            'audits': audits_data,
            'businessTypes': business_types_data,
            'zinara': zinara_data,
            'devolution': devolution_data,
            'incidents': incidents_data,
            'fraud': fraud_data,
            'security': security_data,
            'risk': risk_data,
            'emergency': emergency_data,
            'totalFraudLoss': total_fraud_loss
        }
        return render_template('analytics.html', analytics_data=analytics_data)

    @app.route('/training_awareness', methods=['GET', 'POST'])
    def training_awareness():
        from models import TrainingAwareness
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

    return app

  