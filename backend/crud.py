# backend/crud.py

from sqlalchemy.orm import Session

# Import the SQLAlchemy model and the Pydantic schema
from . import models, schemas 

# --- Loan CRUD Functions ---

def get_loan(db: Session, loan_id: int):
    """Retrieves a single loan by its ID."""
    return db.query(models.Loan).filter(models.Loan.id == loan_id).first()

def get_loans(db: Session, skip: int = 0, limit: int = 100):
    """Retrieves a list of loans with pagination."""
    return db.query(models.Loan).offset(skip).limit(limit).all()

def create_loan(db: Session, loan: schemas.LoanCreate):
    """Creates a new loan entry in the database."""
    # Create a SQLAlchemy models.Loan instance from the Pydantic schema data
    db_loan = models.Loan(**loan.model_dump()) 

    # Add the instance to the session
    db.add(db_loan) 

    # Commit the session to save the loan to the database
    db.commit() 

    # Refresh the instance to get the data back from the DB, 
    # including the auto-generated ID and created_at timestamp
    db.refresh(db_loan) 

    # Return the newly created SQLAlchemy model instance
    return db_loan 

# --- User CRUD Functions (Add later if needed) ---
# def get_user(db: Session, user_id: int): ...
# def get_user_by_email(db: Session, email: str): ...
# def create_user(db: Session, user: schemas.UserCreate): ...