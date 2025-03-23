from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from src.auth.firebase_auth import verify_firebase_token
from src.database.database import get_db
from src.database.models import User

router = APIRouter()

@router.post("/auth/login")
async def login(authorization: str = Header(None), db: Session = Depends(get_db)):
    """
    - Receives Firebase ID token in Authorization header (Bearer token)
    - Verifies token and stores user in PostgreSQL if new
    - Returns user info
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")

    token = authorization.split("Bearer ")[1]

    try:
        decoded_user = verify_firebase_token(token)
        uid = decoded_user["uid"]
        email = decoded_user.get("email")

        # Check if user exists in PostgreSQL
        user = db.query(User).filter(User.uid == uid).first()
        if not user:
            new_user = User(uid=uid, email=email)
            db.add(new_user)
            db.commit()

        return {"uid": uid, "email": email}

    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Firebase token")
