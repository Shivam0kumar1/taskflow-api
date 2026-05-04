from pydantic import BaseModel

# Schema (data structure)
class Job(BaseModel):
    title: str
    description: str

class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str