from app import create_app, db
from models import Business, Audit, ResourceLog, Investigation, FraudAlert, ZinaraFund, DevolutionFund, SecuritySystem, PhysicalSecurity, EmergencyResponse, TrainingAwareness, User
from werkzeug.security import generate_password_hash
from datetime import date, timedelta
from decimal import Decimal
import os

def init_db():
    os.makedirs('instance', exist_ok=True)
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Seed sample businesses
        businesses = [
            Business(name='Downtown Shop 1', type='shop', license_date=date(2024, 1, 1), renewal_date=date(2025, 1, 1)),
            Business(name='Downtown Shop 2', type='shop', license_date=date(2024, 1, 15), renewal_date=date(2025, 1, 15)),
            Business(name='Downtown Shop 3', type='shop', license_date=date(2024, 2, 1), renewal_date=date(2025, 2, 1)),
            Business(name='Downtown Shop 4', type='shop', license_date=date(2024, 2, 15), renewal_date=date(2025, 2, 15)),
            Business(name='Downtown Shop 5', type='shop', license_date=date(2024, 3, 1), renewal_date=date(2025, 3, 1)),
            Business(name='Mutare Bar 1', type='bar', license_date=date(2024, 3, 15), renewal_date=date(2025, 3, 15)),
            Business(name='Mutare Bar 2', type='bar', license_date=date(2024, 4, 1), renewal_date=date(2025, 4, 1)),
            Business(name='Club 232', type='nightclub', license_date=date(2023, 12, 1), renewal_date=date(2024, 12, 1)),
            Business(name='Village Bar', type='bar', license_date=date(2024, 6, 1), renewal_date=date(2025, 6, 1)),
            Business(name='Elite Shop', type='shop', license_date=date(2024, 2, 20), renewal_date=date(2025, 2, 20)),
            Business(name='Central Canteen', type='canteen', license_date=date(2024, 5, 1), renewal_date=date(2025, 5, 1)),
            Business(name='Highway Shop', type='shop', license_date=date(2024, 7, 1), renewal_date=date(2025, 7, 1)),
            Business(name='Night Spot', type='nightclub', license_date=date(2024, 8, 1), renewal_date=date(2025, 8, 1)),
            Business(name='River Bar', type='bar', license_date=date(2024, 9, 1), renewal_date=date(2025, 9, 1)),
            Business(name='Town Canteen', type='canteen', license_date=date(2024, 10, 1), renewal_date=date(2025, 10, 1)),
            Business(name='Market Shop 1', type='shop', license_date=date(2024, 11, 1), renewal_date=date(2025, 11, 1)),
            Business(name='Market Shop 2', type='shop', license_date=date(2024, 12, 1), renewal_date=date(2025, 12, 1)),
            Business(name='Local Bar', type='bar', license_date=date(2025, 1, 1), renewal_date=date(2026, 1, 1)),
            Business(name='Club Zone', type='nightclub', license_date=date(2025, 2, 1), renewal_date=date(2026, 2, 1)),
            Business(name='Staff Canteen', type='canteen', license_date=date(2025, 3, 1), renewal_date=date(2026, 3, 1)),
            Business(name='Corner Shop', type='shop', license_date=date(2025, 4, 1), renewal_date=date(2026, 4, 1)),
            Business(name='Riverside Bar', type='bar', license_date=date(2025, 5, 1), renewal_date=date(2026, 5, 1)),
            Business(name='Neon Club', type='nightclub', license_date=date(2025, 6, 1), renewal_date=date(2026, 6, 1)),
            Business(name='Work Canteen', type='canteen', license_date=date(2025, 7, 1), renewal_date=date(2026, 7, 1)),
        ]
        db.session.add_all(businesses)
        db.session.add_all(businesses)



        # Sample audits
        audits = [
            Audit(date=date(2024, 10, 1), type='revenue_leak', details='Uncollected fees from 5 shops', status='pending'),
            Audit(date=date(2024, 9, 15), type='finance', details='Receipting audit complete', status='completed'),
        ]
        db.session.add_all(audits)

        # Sample resource logs
        resources = [
            ResourceLog(date=date(2024, 10, 5), item='Fuel', quantity_used=Decimal('500.00'), notes='Road maintenance'),
            ResourceLog(date=date(2024, 10, 6), item='Materials', quantity_used=Decimal('2000.00'), notes='Bridge repair'),
        ]
        db.session.add_all(resources)

        # Sample investigations
        investigations = [
            Investigation(date_opened=date(2024, 10, 1), type='theft', description='Suspected fuel theft in roads dept', loss_amount=Decimal('25000.00'), status='open'),
            Investigation(date_opened=date(2024, 9, 20), type='fraud', description='License fee underreporting', loss_amount=Decimal('15000.00'), status='closed', recommendations='Implement digital receipts'),
            Investigation(date_opened=date(2024, 10, 10), type='security_breach', description='CCTV outage at warehouse', loss_amount=Decimal('0.00'), status='open'),
        ]
        db.session.add_all(investigations)

        # Sample fraud alerts
        fraud_alerts = [
            FraudAlert(date_detected=date(2024, 10, 5), type='revenue_leak', description='Unmetered water connections in industrial area', amount_lost=Decimal('45000.00'), status='open'),
            FraudAlert(date_detected=date(2024, 9, 25), type='corruption', description='Ghost workers in payroll detected', amount_lost=Decimal('120000.00'), status='closed'),
        ]
        db.session.add_all(fraud_alerts)

        # Sample ZINARA funds
        zinara = [
            ZinaraFund(date_received=date(2024, 1, 15), category='roads', amount=Decimal('500000.00'), notes='Quarter 1 road rehab'),
            ZinaraFund(date_received=date(2024, 4, 10), category='fuel', amount=Decimal('150000.00'), notes='Fuel allocation'),
            ZinaraFund(date_received=date(2024, 7, 5), category='audits', amount=Decimal('50000.00'), notes='Compliance audits'),
            ZinaraFund(date_received=date(2024, 10, 1), category='roads', amount=Decimal('600000.00'), notes='Q4 maintenance'),
            ZinaraFund(date_received=date(2025, 1, 10), category='fuel', amount=Decimal('120000.00'), notes='Q1 fuel'),
        ]
        db.session.add_all(zinara)

        # Sample Devolution funds
        devolution = [
            DevolutionFund(date_received=date(2024, 3, 1), sector='schools', amount=Decimal('800000.00'), notes='School infra'),
            DevolutionFund(date_received=date(2024, 6, 1), sector='community', amount=Decimal('500000.00'), notes='Community halls'),
            DevolutionFund(date_received=date(2024, 9, 1), sector='health', amount=Decimal('300000.00'), notes='Clinic upgrades'),
            DevolutionFund(date_received=date(2024, 12, 1), sector='roads', amount=Decimal('200000.00'), notes='Local roads'),
            DevolutionFund(date_received=date(2025, 3, 1), sector='others', amount=Decimal('200000.00'), notes='Admin'),
        ]
        db.session.add_all(devolution)

        # Sample Security Systems
        security_systems = [
            SecuritySystem(date_assessed=date(2024, 10, 5), type='cctv', facility='warehouse', effectiveness_score=7, issues='Camera blind spots', recommendations='Add 2 more cameras', status='pending'),
            SecuritySystem(date_assessed=date(2024, 9, 20), type='access_control', facility='head_office', effectiveness_score=9, status='active'),
        ]
        db.session.add_all(security_systems)

        # Sample Physical Security
        physical_security = [
            PhysicalSecurity(date_planned=date(2024, 10, 1), facility='rural_service_center', measures='fencing, patrols', risk_level='high', assets_protected='Equipment storage'),
            PhysicalSecurity(date_planned=date(2024, 9, 15), facility='head_office', measures='access_lighting, fencing', risk_level='low', status='implemented'),
        ]
        db.session.add_all(physical_security)

        # Sample Emergency Response
        emergency_responses = [
            EmergencyResponse(date_created=date(2024, 8, 1), procedure_type='fire', facility='warehouse', steps='1. Sound alarm\n2. Evacuate\n3. Call fire dept', last_drill_date=date(2024, 9, 10), status='active'),
            EmergencyResponse(date_created=date(2024, 7, 15), procedure_type='security_incident', facility='head_office', steps='1. Lockdown\n2. Notify security\n3. Police', status='active'),
        ]
        db.session.add_all(emergency_responses)

        # Sample Training & Awareness
        trainings = [
            TrainingAwareness(date_conducted=date(2024, 10, 8), type='crime_prevention', attendees_count=25, topics_covered='Theft prevention, reporting procedures', trainer='Sgt. Makoni', status='completed'),
            TrainingAwareness(date_conducted=date(2024, 9, 12), type='fire_evacuation', attendees_count=45, topics_covered='Evacuation routes, fire extinguisher use', trainer='Fire Warden Chigumbu', status='completed'),
        ]
        db.session.add_all(trainings)

        # Create sample users
        from werkzeug.security import generate_password_hash
        admin = User(username='admin', email='admin@marondera.gov.zw', password_hash=generate_password_hash('admin123'), role='admin')
        user1 = User(username='officer1', email='officer1@marondera.gov.zw', password_hash=generate_password_hash('password123'), role='user')
        db.session.add(admin)
        db.session.add(user1)

        db.session.commit()
        print('Database initialized with sample data including users (admin/admin123, officer1/password123).')

if __name__ == '__main__':
    init_db()

