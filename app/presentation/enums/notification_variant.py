from enum import Enum


class NotificationVariant(Enum):
    Error = 'notification-error'
    Success = 'notification-success'
    Choice = 'notification-choice'

    def __init__(self, object_name: str):
        self.__object_name = object_name

    @property
    def object_name(self) -> str:
        return self.__object_name
