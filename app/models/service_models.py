from pydantic import BaseModel


class StageStatus(BaseModel):
    running: bool
    position: tuple
