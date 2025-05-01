# backend/schemas.py

# Add computed_field to imports
from pydantic import BaseModel, Field, ConfigDict, computed_field , EmailStr
import datetime

# --- Loan Schemas ---

class LoanBase(BaseModel):
    # ... (fields remain the same)
    borrower_name: str = Field(..., example="Jane Doe")
    amount: float = Field(..., gt=0, example=1500.50)
    interest_rate: float = Field(..., ge=0, example=4.75) # Annual rate %
    time_period_months: int = Field(..., gt=0, example=24)

class LoanCreate(LoanBase):
    pass

class Loan(LoanBase):
    id: int
    created_at: datetime.datetime
    
    # --- Add Computed Field for Simple Interest ---
    @computed_field 
    @property # Use property decorator
    def calculated_interest(self) -> float:
        """Computes simple interest for the loan period."""
        monthly_rate = (self.interest_rate / 100) / 12
        simple_interest = self.amount * monthly_rate * self.time_period_months
        # Optional: round to 2 decimal places
        return round(simple_interest, 2) 

    # --- ORM Mode Configuration ---
    model_config = ConfigDict(from_attributes=True)


# --- User Schemas ---

class UserBase(BaseModel):
    # Common base field: email
    # EmailStr type provides automatic email format validation
    email: EmailStr 

class UserCreate(UserBase):
    # Schema specifically for user creation (signup)
    # Includes the plain text password provided by the user
    password: str 
    # Note: We receive the plain password here, hash it in the backend (crud.py), 
    # and store the HASH in the database (models.User.hashed_password).

class User(UserBase):
    # Schema for data returned by the API when representing a user
    # Inherits email from UserBase
    id: int
    is_active: bool
    created_at: datetime.datetime

    # --- ORM Mode Configuration ---
    # Allows creating this schema from the SQLAlchemy User model object
    model_config = ConfigDict(from_attributes=True)

    # Note: We intentionally DO NOT include 'password' or 'hashed_password' here
    # to avoid ever sending password info back out through the API.



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    # Schema for data held within the token (optional but good practice)
    email: str | None = None