from fastapi import FastAPI
from pydantic import BaseModel, Field
import datetime


# Create an instance of the FastAPI class
app = FastAPI()
# --- Temporary In-Memory Storage (replace with database later) ---
# This is just for demonstration purposes. Data will be lost when the server restarts.
temp_loans_db = {} # Dictionary to store loans, keyed by loan ID
loan_id_counter = 0 # Simple counter to generate unique IDs
# Define a route for the root URL ("/")



class LoanBase(BaseModel):
    # Define a Pydantic model for the request body
    borrower_name: str = Field(..., example="John Doe")
    amount: float = Field(..., gt=0, example=1500.50) # gt = greater than
    interest_rate: float = Field(..., ge=0, example=4.75) # ge = greater than or equal to
    time_period_months: int = Field(..., gt=0, example=12) # Assuming term is in months

class LoanCreate(LoanBase):
    pass

class Loan(LoanBase):
    id : int
    created_at: datetime.datetime



# --- API Endpoints ---

@app.post("/loans/", response_model=Loan, status_code=201) # status_code=201 indicates resource created
async def create_loan(loan_data: LoanCreate):
    """
    Creates a new loan entry.
    Receives loan details in the request body, validates them using LoanCreate,
    assigns a unique ID and timestamp, stores it, and returns the created loan.
    """
    global loan_id_counter, temp_loans_db # Declare we are modifying global variables

    loan_id_counter += 1 # Increment the ID counter

    # Create a complete Loan object including generated fields
    new_loan = Loan(
        id=loan_id_counter,
        created_at=datetime.datetime.now(datetime.timezone.utc), # Use timezone-aware UTC time
        # Unpack the validated data from loan_data (which matches LoanBase fields)
        # Use model_dump() for Pydantic v2+
        **loan_data.model_dump() 
    )

    # Store the new loan in our temporary dictionary
    temp_loans_db[new_loan.id] = new_loan

    # Return the newly created loan object (FastAPI validates it against response_model=Loan)
    return new_loan

@app.get("/loans/", response_model=list[Loan])
async def get_loans():
    """
    Retrieves a list of all stored loan entries.
    """
    return list(temp_loans_db.values()) # Return the dictionary values as a list

@app.get("/")
async def read_root():
    return {"message": "Hello from the Interest Calculator Backend!"}

# Define another example route
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    # This route takes a path parameter 'item_id' and an optional query parameter 'q'
    return {"item_id": item_id, "q": q}
