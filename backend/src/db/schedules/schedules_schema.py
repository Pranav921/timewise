from pydantic import BaseModel

class ScheduleBase(BaseModel):
    id: str

class ScheduleCreate(BaseModel):
    name: str
    semester: str

class ScheduleEdit(ScheduleBase):
    name: str
    semester: str

class ScheduleDelete(ScheduleBase):
    pass