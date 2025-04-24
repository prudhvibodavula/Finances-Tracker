# backend/main.py

from fastapi import FastAPI, Depends # Added Depends
from sqlalchemy.orm import Session # Added Session

# Updated imports to use new modules
from . import crud, models, schemas 
from .database import engine, get_db # Added get_db

# --- Database Table Creation ---
# This line should still be here to ensure tables are created on startup
models.Base.metadata.create_all(bind=engine)

# --- FastAPI App Instance ---
app = FastAPI()

# --- API Endpoints ---

@app.post("/loans/", response_model=schemas.Loan, status_code=201)
async def create_loan_endpoint( # Renamed slightly to avoid conflict with crud function
    loan_data: schemas.LoanCreate, # Use schema for request body
    db: Session = Depends(get_db) # Inject DB session
):
    """
    Creates a new loan entry by calling the CRUD function.
    """
    # Call the CRUD function to handle database interaction
    return crud.create_loan(db=db, loan=loan_data)

@app.get("/loans/", response_model=list[schemas.Loan])
async def get_loans_endpoint( # Renamed slightly
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db) # Inject DB session
):
    """
    Retrieves a list of loans using the CRUD function with pagination.
    """
    # Call the CRUD function to get loans
    loans = crud.get_loans(db=db, skip=skip, limit=limit)
    return loans

@app.get("/")
async def read_root():
    return {"message": "Hello from the Interest Calculator Backend!"}

# Optional: Add an endpoint to get a single loan by ID
@app.get("/loans/{loan_id}", response_model=schemas.Loan)
async def get_loan_endpoint(loan_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a specific loan by its ID using the CRUD function.
    """
    db_loan = crud.get_loan(db=db, loan_id=loan_id)
    if db_loan is None:
        from fastapi import HTTPException # Import HTTPException here
        raise HTTPException(status_code=404, detail="Loan not found")
    return db_loan

# (Keep the /items/{item_id} example endpoint or remove it)
# ...