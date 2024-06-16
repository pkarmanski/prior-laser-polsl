
from pydantic import BaseModel


class StageStatus(BaseModel):
    running: bool
    position: tuple


class ServiceAppParams(BaseModel):
    scale_x: float
    scale_y: float


