import os # For environment variables
from datetime import datetime, timedelta, timezone # For token expiration
from typing import Union, Any # For type hinting

from passlib.context import CryptContext
from jose import JWTError, jwt # Import JWT components from python-jose
from dotenv import load_dotenv # To load .env variables

load_dotenv() # Load environment variables from .env

# --- Password Hashing Setup ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- JWT Configuration ---
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set for JWT encoding")

# 2. Function to verify a plain password against a stored hash
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain text password against a stored hash.

    Args:
        plain_password: The password attempt from the user.
        hashed_password: The hash stored in the database.

    Returns:
        True if the password matches the hash, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

# 3. Function to hash a plain password
def get_password_hash(password: str) -> str:
    """
    Hashes a plain text password using the configured context (bcrypt).

    Args:
        password: The plain text password to hash.

    Returns:
        The generated password hash (including salt).
    """
    return pwd_context.hash(password)

# --- NEW: JWT Token Creation ---
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """Creates a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Default expiration if not provided
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire}) # Add expiration time to payload
    # Encode payload, secret key, and algorithm into a JWT string
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt