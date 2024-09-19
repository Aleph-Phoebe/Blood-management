import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from inventory import add_blood_inventory, get_blood_inventory
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

def test_add_blood_inventory(db_session):
    """Test adding blood inventory."""
    inventory = add_blood_inventory(db_session, "O+", 10, date(2024, 9, 19))
    assert inventory.blood_type == "O+"
    assert inventory.quantity == 10
    assert inventory.expiry_date == date(2024, 9, 19)

def test_get_blood_inventory(db_session):
    """Test retrieving blood inventory."""
    add_blood_inventory(db_session, "O+", 10, date(2024, 9, 19))
    inventory = get_blood_inventory(db_session)
    assert len(inventory) == 1
    assert inventory[0].blood_type == "O+"
    assert inventory[0].quantity == 10
