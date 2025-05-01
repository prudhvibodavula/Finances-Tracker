# backend/main.py

# Change this line near the top of main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session # Added Session
# Add to top imports in main.py
from fastapi.security import OAuth2PasswordRequestForm # For login form data
from datetime import timedelta
from . import auth # Import the updated auth module
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

# Add these endpoints in backend/main.py (e.g., below the loan endpoints)

@app.post("/users/", response_model=schemas.User, status_code=201, tags=["Users"])
async def create_user_endpoint(
    user: schemas.UserCreate, 
    db: Session = Depends(get_db)
):
    """
    Creates a new user (Signup).
    Checks if email already exists before creating.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.post("/token", response_model=schemas.Token, tags=["Users"])
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), # Expects form data: username=..., password=...
    db: Session = Depends(get_db)
):
    """
    Logs in a user by verifying email/password and returning a JWT token.
    Uses OAuth2PasswordRequestForm for standard form input.
    """
    # 1. Get user by email (form sends email in 'username' field)
    user = crud.get_user_by_email(db, email=form_data.username)

    # 2. Verify user exists, password is correct, and user is active
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401, # Use 401 for authentication failure
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}, # Standard header for auth errors
        )
    if not user.is_active:
         raise HTTPException(status_code=400, detail="Inactive user") # Or 401/403

    # 3. Create the JWT access token
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        # Data to encode in the token (subject 'sub' is standard)
        data={"sub": user.email}, 
        expires_delta=access_token_expires
    )

    # 4. Return the token
    return {"access_token": access_token, "token_type": "bearer"}