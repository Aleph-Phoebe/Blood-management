from sqlalchemy.orm import Session
from models import BloodInventory, Donor

def generate_inventory_report(db: Session):
    inventory = db.query(BloodInventory).all()
    report = []
    for item in inventory:
        report.append({
            "Blood Type": item.blood_type,
            "Quantity": item.quantity,
            "Expiry Date": item.expiry_date
        })
    return report

def generate_donor_report(db: Session):
    donors = db.query(Donor).all()
    report = []
    for donor in donors:
        report.append({
            "Name": donor.name,
            "Blood Type": donor.blood_type,
            "Last Donation Date": donor.last_donation_date
        })
    return report
