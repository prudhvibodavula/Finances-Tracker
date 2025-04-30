# backend/auth.py

from passlib.context import CryptContext

# --- Password Hashing Setup ---

# 1. Create a CryptContext instance
#    - schemes=["bcrypt"]: Specifies the hashing algorithm to use (bcrypt is recommended).
#    - deprecated="auto": Tells passlib to automatically handle upgrading hashes
#      if you change the scheme list in the future.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

# --- JWT Token Handling (Add later) ---
# We will add functions here later for creating and verifying JWT tokens
# for login sessions.