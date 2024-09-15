from typing import List, Any

from pydantic import BaseModel

from app.files_processing.enums import Figures


class Entity(BaseModel):
    coords: List = None
    radius: float = None
    entity_type: Figures
    params: Any = None
    angle: float = None

