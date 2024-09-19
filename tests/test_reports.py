import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from reports import generate_inventory_report, generate_donor_report
from donors import add_donor
from inventory import add_blood_inventory
from datetime import date

# Set up a temporary test database
TEST_DATABASE_URL = "sqlite:///test_blood_management.db"
engine = create_engine(TEST_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.rollback()
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_generate_inventory_report(db_session):
    """Test inventory report generation."""
    add_blood_inventory(db_session, "B+", 15, date(2024, 10, 10))
    report = generate_inventory_report(db_session)
    assert len(report) == 1
    assert report[0]["Blood Type"] == "B+"
    assert report[0]["Quantity"] == 15
    assert report[0]["Expiry Date"] == date(2024, 10, 10)

def test_generate_donor_report(db_session):
    """Test donor report generation."""
    add_donor(db_session, "Jane Doe", "B+", "jane@example.com", date(2023, 8, 20))
    report = generate_donor_report(db_session)
    assert len(report) == 1
    assert report[0]["Name"] == "Jane Doe"
    assert report[0]["Blood Type"] == "B+"
    assert report[0]["Last Donation Date"] == date(2023, 8, 20)
