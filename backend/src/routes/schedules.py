from fastapi import APIRouter, status, HTTPException
from src.routes.dependencies import AuthorizedUID
from src.db.schedules.schedules_model import ScheduleCreate, ScheduleEdit, ScheduleDelete, insert_schedule, edit_schedule, delete_schedule
from src.routes.utils import get_semester_str

router = APIRouter(
    prefix="/schedules"
)

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create(schedule: ScheduleCreate, uid: AuthorizedUID):
    try:
        schedule.semester = get_semester_str(schedule.semester)
        await insert_schedule(schedule, uid)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating a schedule")

@router.post("/get", status_code=status.HTTP_200_OK)
async def get(id: str, uid: AuthorizedUID):
    try:
        # await insert_plan(Plan(name=plan.name), uid)
        pass
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching the schedule")

@router.post("/edit", status_code=status.HTTP_200_OK)
async def edit(schedule: ScheduleEdit, uid: AuthorizedUID):
    try:
        schedule.semester = get_semester_str(schedule.semester)
        await edit_schedule(schedule, uid)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error editing schedule")
    
@router.post("/delete", status_code=status.HTTP_200_OK)
async def delete(schedule: ScheduleDelete, uid: AuthorizedUID):
    try:
        await delete_schedule(schedule, uid)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error deleting schedule")