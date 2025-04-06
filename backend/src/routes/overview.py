from fastapi import APIRouter, HTTPException, status
from src.routes.dependencies import AuthorizedUID
from src.db.postgres import database

router = APIRouter(
    prefix="/overview"
)

@router.get("/", status_code=status.HTTP_200_OK)
async def get_overview(uid: AuthorizedUID):
    try:
        async with database.pool.acquire() as connection:
            async with connection.transaction():
                plans_query = "SELECT * FROM plans WHERE plans.owner_uid = $1"
                plans_data = await connection.fetch(plans_query, uid)

                schedules_query = "SELECT * FROM schedules WHERE schedules.owner_uid = $1"
                schedules_data = await connection.fetch(schedules_query, uid)

                result = {
                    "plans": plans_data,
                    "schedules": schedules_data,
                }

                return result
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching overview data")

  