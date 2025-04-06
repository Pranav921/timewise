from .plans_schema import PlanCreate, PlanEdit, PlanDelete
from src.db.postgres import database

async def insert_plan(plan: PlanCreate, uid: str):
    query = "INSERT INTO plans (owner_uid, name, semester) VALUES ($1, $2, $3)"
    async with database.pool.acquire() as connection:
        await connection.execute(query, uid, plan.name, plan.semester)

async def edit_plan(plan: PlanEdit, uid: str):
    query = "UPDATE plans SET name = $1, semester = $2 WHERE id = $3 AND owner_uid = $4"
    async with database.pool.acquire() as connection:
        await connection.execute(query, plan.name, plan.semester, plan.id, uid)

async def delete_plan(plan: PlanDelete, uid: str):
    query = "DELETE FROM plans WHERE id = $1 AND owner_uid = $2"
    async with database.pool.acquire() as connection:
        await connection.execute(query, plan.id, uid)