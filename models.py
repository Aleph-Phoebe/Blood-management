from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    is_staff = Column(Boolean, default=False)  # To differentiate between staff and donors

class Donor(Base):
    __tablename__ = 'donors'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    blood_type = Column(String, index=True)
    contact_info = Column(String)
    last_donation_date = Column(Date)

    donations = relationship("Donation", back_populates="donor")

class BloodInventory(Base):
    __tablename__ = 'blood_inventory'

    id = Column(Integer, primary_key=True, index=True)
    blood_type = Column(String, index=True)
    quantity = Column(Integer)
    expiry_date = Column(Date)

class Donation(Base):
    __tablename__ = 'donations'

    id = Column(Integer, primary_key=True, index=True)
    donor_id = Column(Integer, ForeignKey('donors.id'))
    date = Column(Date)
    blood_type = Column(String)
    quantity = Column(Integer)

    donor = relationship("Donor", back_populates="donations")
