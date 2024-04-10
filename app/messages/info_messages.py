from enum import Enum


class StageInfoMsg(Enum):
    PRIOR_INITIALIZED = 'successfully initialized PriorSDK, info: {}'
    PRIOR_SESSION_CREATED  = 'successfully created session, sessionID: {}'

    def __init__(self, description: str):
        self.__description = description

    @property
    def description(self) -> str:
        return self.__description
