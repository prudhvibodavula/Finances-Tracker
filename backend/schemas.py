# backend/schemas.py

# Add computed_field to imports
from pydantic import BaseModel, Field, ConfigDict, computed_field 
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