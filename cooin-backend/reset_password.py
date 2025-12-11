"""
Script to reset password for a user
Usage: python reset_password.py
"""
import sys
sys.path.insert(0, 'C:\\Windows\\System32\\cooin-app\\cooin-backend')

from app.db.base import SessionLocal
from app.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def reset_password(email: str, new_password: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user:
            user.hashed_password = pwd_context.hash(new_password)
            db.commit()
            print(f"[SUCCESS] Password reset successful for {email}")
            print(f"New password: {new_password}")
            return True
        else:
            print(f"[ERROR] User not found: {email}")
            return False
    except Exception as e:
        print(f"[ERROR] {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    # Reset password for x@x.com
    reset_password("x@x.com", "Testx123456")
