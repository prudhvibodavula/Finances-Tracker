# backend/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy.orm import Session
# Load environment variables from a .env file if it exists
# Looks for a .env file in the current directory or parent directories
load_dotenv() 

# --- Database URL Configuration ---
# Get the database URL from the environment variable "DATABASE_URL"
# If it's not set, default to a local SQLite database file named "loans.db"
# in the same directory as this script (or wherever the app runs from).
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///backend/loans.db")
# Example for PostgreSQL later: DATABASE_URL="postgresql://user:password@host:port/database"

# --- SQLAlchemy Engine Setup ---
# create_engine is the core interface to the database.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    # connect_args is needed only for SQLite to ensure compatibility with FastAPI's threading
    connect_args={"check_same_thread": False} 
)

# --- Session Management ---
# sessionmaker creates a factory that produces database sessions (Session objects).
# A session manages persistence operations for ORM-mapped objects (talking to the DB).
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Base Class for Models ---
# declarative_base() returns a class that maintains a catalog of classes and tables 
# relative to that base. Our database models (like models.Loan) will inherit from this.
Base = declarative_base()

# --- Dependency for getting DB session ---
def get_db():
    """
    Dependency function that creates and yields a database session,
    ensuring it's closed afterwards.
    """
    db = SessionLocal() # Create a new Session using the sessionmaker factory
    try:
        yield db # Provide the session to the path operation function
    finally:
        db.close() # Close the session when the request is finished