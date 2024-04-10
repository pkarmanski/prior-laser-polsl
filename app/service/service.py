"""
This class will talk with repositories and will have logic for error handling
and what to return to window when error happens
"""

from app.stage.stage_repository import StageRepository


class Service:
    def __init__(self):
        self.__stage_repository = StageRepository()
