from sqlalchemy import Column, Integer, String, Float, DateTime, func, Boolean
from .database import Base
from sqlalchemy.sql import func # Need this for server_default timestamp

# Import the Base class from database.py (using relative import)
from .database import Base 

class Loan(Base):
    # Tell SQLAlchemy the name of the table in the database
    __tablename__ = "loans" 

    # Define columns for the 'loans' table
    # id: Primary key, integer, automatically increments, indexed for fast lookups
    id = Column(Integer, primary_key=True, index=True) 

    # borrower_name: String, indexed for potential searching
    borrower_name = Column(String, index=True, nullable=False) 

    # amount: Float, cannot be null
    amount = Column(Float, nullable=False) 

    # interest_rate: Float, cannot be null
    interest_rate = Column(Float, nullable=False) 

    # time_period_months: Integer, cannot be null
    time_period_months = Column(Integer, nullable=False) 

    # created_at: DateTime, cannot be null, 
    # Set default value to the database's current time when a record is created
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False) 

    # Add relationship to User model later if needed
    # owner_id = Column(Integer, ForeignKey("users.id")) 
    # owner = relationship("User", back_populates="loans")


    # ... (Loan class definition) ...

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    # Email used for login, must be unique
    email = Column(String, unique=True, index=True, nullable=False)
    # Hashed password storage (never plain text)
    hashed_password = Column(String, nullable=False)
    # Flag to easily disable accounts if needed later
    is_active = Column(Boolean, default=True)
    # Timestamp for user creation
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationship placeholder (add later)
    # loans = relationship("Loan", back_populates="owner")