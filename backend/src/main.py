from src.auth.auth_routes import router as auth_router
from src.auth.protected_routes import router as protected_router
from fastapi import FastAPI

app = FastAPI()

app.include_router(auth_router, prefix="/api")
app.include_router(protected_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to Timewise API"}
