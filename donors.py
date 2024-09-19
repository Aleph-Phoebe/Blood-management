from sqlalchemy.orm import Session
from models import Donor
from datetime import date

def add_donor(db: Session, name: str, blood_type: str, contact_info: str, last_donation_date: date):
    donor = Donor(name=name, blood_type=blood_type, contact_info=contact_info, last_donation_date=last_donation_date)
    db.add(donor)
    db.commit()
    db.refresh(donor)
    return donor

def get_donors(db: Session):
    return db.query(Donor).all()

def update_donation_date(db: Session, donor_id: int, last_donation_date: date):
    donor = db.query(Donor).filter(Donor.id == donor_id).first()
    if donor:
        donor.last_donation_date = last_donation_date
        db.commit()
        db.refresh(donor)
    return donor
