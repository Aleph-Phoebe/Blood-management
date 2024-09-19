from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Replace 'sqlite:///blood_management.db' with your preferred database URL
DATABASE_URL = 'sqlite:///blood_management.db'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
