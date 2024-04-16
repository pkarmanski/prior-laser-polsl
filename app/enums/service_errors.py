from enum import Enum


class ServiceError(Enum):
    OK = (0, "OK")
    STAGE_ERROR = (1, "STAGE_ERROR")
    STAGE_OPEN_SESSION_ERROR = (2, "STAGE_OPEN_SESSION_ERROR")
    STAGE_CONNECT_ERROR = (3, "STAGE_CONNECT_ERROR")

    def __init__(self, code: int, description: str):
        self.__code = code
        self.__description = description

    @property
    def code(self) -> int:
        return self.__code

    @property
    def description(self) -> str:
        return self.__description