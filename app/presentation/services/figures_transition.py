from app.files_processing.enums import Figures
from app.files_processing.models import Entity


class FiguresTransitionService:
    def __init__(self, scale: float):
        self.scale = scale

    @classmethod
    def get_offset(cls, entities: list[Entity]) -> tuple[int, int]:
        min_x = entities[0].coords[0][0]
        min_y = entities[0].coords[0][1]
        for entity in entities:
            coords = entity.coords
            if entity.entity_type == Figures.SPLINE:
                x, y = cls.get_offset_spline(coords)
                min_x = min(min_x, x)
                min_y = min(min_y, y)
            else:
                x, y = cls.get_other_offset(coords)
                min_x = min(min_x, x)
                min_y = min(min_y, y)

        return min_x, min_y

    @staticmethod
    def get_offset_spline(coords: list[tuple[float, float]]) -> tuple[float, float]:
        min_x, min_y = coords[0][0], coords[0][1]

        for coord in coords:
            x = coord[0]
            y = coord[1]
            y = -y
            if x < min_x:
                min_x = x
            if y < min_y:
                min_y = y

        return min_x, min_y

    @staticmethod
    def get_other_offset(coords: list) -> tuple[float, float]:
        min_x, min_y = coords[0], coords[1]
        for x, y in coords:
            y = -y
            if x < min_x:
                min_x = x
            if y < min_y:
                min_y = y

        return min_x, min_y
