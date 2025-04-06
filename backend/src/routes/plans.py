from fastapi import APIRouter, status, HTTPException
from src.routes.dependencies import AuthorizedUID
from src.db.plans.plans_model import PlanCreate, PlanEdit, PlanDelete, insert_plan, edit_plan, delete_plan
from src.routes.utils import get_semester_str

router = APIRouter(
    prefix="/plans"
)

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create(plan: PlanCreate, uid: AuthorizedUID):
    """
    Creates a new 4-year plan for a user.

    Args:
        plan (Plan): The plan object containing the name and semester information.
        uid (AuthorizedUID): The authorized user ID of the user creating the plan.

    Raises:
        HTTPException: If an error occurs while creating the plan, an HTTP 500 error is raised with a relevant message.
    """
    try:
        # TODO: i don't think this is best practice
        plan.semester = get_semester_str(plan.semester)
        await insert_plan(plan, uid)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating a 4-year plan")

@router.post("/edit", status_code=status.HTTP_200_OK)
async def edit(plan: PlanEdit, uid: AuthorizedUID):
    try:
        plan.semester = get_semester_str(plan.semester)
        await edit_plan(plan, uid)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error editing 4-year plan")
    
@router.post("/delete", status_code=status.HTTP_200_OK)
async def delete(plan: PlanDelete, uid: AuthorizedUID):
    try:
        await delete_plan(plan, uid)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error deleting 4-year plan")