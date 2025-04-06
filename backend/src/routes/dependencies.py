from typing import Annotated
from fastapi import Header, HTTPException, Depends
from src.firebase import verify_firebase_token

async def verifyUser(authorization: Annotated[str, Header()]):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")

    token = authorization.split("Bearer ")[1]

    try:
        user = verify_firebase_token(token)
        return user["uid"]
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Firebase token")

AuthorizedUID = Annotated[str, Depends(verifyUser)]