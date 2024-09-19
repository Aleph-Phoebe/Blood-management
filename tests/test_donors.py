import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from donors import add_donor, get_donors
from datetime import date

# Set up a temporary test database
TEST_DATABASE_URL = "sqlite:///test_blood_management.db"
engine = create_engine(TEST_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Create a new database session for each test."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.rollback()
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_add_donor(db_session):
    """Test adding a new donor."""
    donor = add_donor(db_session, "John Doe", "A+", "john@example.com", date(2023, 9, 15))
    assert donor.name == "John Doe"
    assert donor.blood_type == "A+"
    assert donor.contact_info == "john@example.com"
    assert donor.last_donation_date == date(2023, 9, 15)

def test_get_donors(db_session):
    """Test retrieving all donors."""
    add_donor(db_session, "John Doe", "A+", "john@example.com", date(2023, 9, 15))
    donors = get_donors(db_session)
    assert len(donors) == 1
    assert donors[0].name == "John Doe"
