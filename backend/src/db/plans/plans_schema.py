from pydantic import BaseModel

class PlanBase(BaseModel):
    id: str

class PlanCreate(BaseModel):
    name: str
    semester: str

class PlanEdit(PlanBase):
    name: str
    semester: str

class PlanDelete(PlanBase):
    pass
