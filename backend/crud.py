# backend/crud.py

from sqlalchemy.orm import Session

# Import the SQLAlchemy model and the Pydantic schema
from . import models, schemas, auth

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


# --- User CRUD Functions ---

def get_user(db: Session, user_id: int):
    """Retrieves a single user by their ID."""
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """Retrieves a single user by their email address."""
    # Emails are unique, so filter by email and get the first result (or None)
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    """Creates a new user entry in the database after hashing the password."""
    # 1. Hash the plain text password from the input schema
    hashed_password = auth.get_password_hash(user.password)

    # 2. Create the SQLAlchemy models.User instance
    #    IMPORTANT: Use the hashed_password, NOT the plain one from user.password
    db_user = models.User(
        email=user.email, 
        hashed_password=hashed_password
        # is_active defaults to True in models.py
        # created_at defaults to now() in models.py
    )

    # 3. Add, commit, and refresh (same pattern as create_loan)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # 4. Return the newly created user object (with id, created_at etc.)
    return db_user