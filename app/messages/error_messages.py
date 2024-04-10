from enum import Enum


class StageErrorMsg(Enum):
    PRIOR_INITIALIZATION_ERROR = 'error initializing, error: {}'
    PRIOR_SESSION_ERROR = 'error getting sessionID, error: {}'

    def __init__(self, description: str):
        self.__description = description

    @property
    def description(self) -> str:
        return self.__description
