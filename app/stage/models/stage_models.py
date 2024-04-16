from typing import TypeVar, Generic

from pydantic import BaseModel

from app.enums.service_errors import ServiceError

T = TypeVar("T", bound=BaseModel)


class StageError(BaseModel):
    error: ServiceError
    description: str
    return_status: int = 0


class StageResponse(BaseModel, Generic[T]):
    data: T
    error: StageError
