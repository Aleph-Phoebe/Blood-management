from sqlalchemy.orm import Session
from models import BloodInventory
from datetime import date

def add_blood_inventory(db: Session, blood_type: str, quantity: int, expiry: date):
    inventory = BloodInventory(blood_type=blood_type, quantity=quantity, expiry_date=expiry)
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    return inventory

def get_blood_inventory(db: Session):
    return db.query(BloodInventory).all()

def update_blood_inventory(db: Session, inventory_id: int, quantity: int):
    inventory = db.query(BloodInventory).filter(BloodInventory.id == inventory_id).first()
    if inventory:
        inventory.quantity = quantity
        db.commit()
        db.refresh(inventory)
    return inventory
