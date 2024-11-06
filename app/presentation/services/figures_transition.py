from app.files_processing.enums import Figures
from app.files_processing.models import Entity
from app.consts.presentation_consts import PRESENTATION_OFFSET
import math


class FiguresTransitionService:
    def __init__(self, scale: float):
        self.scale = scale

    def apply_offset(self, figures: list[Entity]) -> list[Entity]:
        # in case there is "from_canvas" selected
        if not figures:
            return []

        x_offset, y_offset = self.get_offset(figures)
        for entity in figures:
            coords = entity.coords
            scaled_coords = [(((x - x_offset) / self.scale) + PRESENTATION_OFFSET,
                              ((-y - y_offset) / self.scale) + PRESENTATION_OFFSET)
                             for x, y in coords]
            entity.coords = scaled_coords
            if entity.radius:
                entity.radius /= self.scale
            if entity.entity_type == Figures.ELLIPSE and entity.params:
                major, minor = entity.params
                entity.params = (major / self.scale, minor / self.scale)

        return figures

    @classmethod
    def get_offset(cls, entities: list[Entity]) -> tuple[int, int]:
        min_x = entities[0].coords[0][0]
        min_y = entities[0].coords[0][1]
        for entity in entities:
            coords = entity.coords
            if entity.entity_type == Figures.SPLINE:
                x, y = cls.get_offset_spline(coords)

            elif entity.entity_type == Figures.ELLIPSE:
                x, y = cls.get_offset_ellipse(entity)

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
    def get_offset_ellipse(entity: Entity) -> tuple[float, float]:
        coords = entity.coords
        x, y = coords[0]
        width = entity.params[0]
        height = entity.params[1]
        angle = math.radians(entity.angle)
        before_rotation = [[x - width, y + height], [x + width, y + height], [x, y + height], [x + width, y]]
        after_rotation = [
            [x * math.cos(angle) - y * math.sin(angle), y * math.cos(angle) + x * math.sin(angle)]
            for x, y in before_rotation
        ]
        min_x, min_y = after_rotation[0][0], after_rotation[0][1]
        for x, y in after_rotation[1:]:
            y *= -1
            if min_x > x:
                min_x = x

            if min_y > y:
                min_y = y

        return min_x, min_y

    @staticmethod
    def get_other_offset(coords: list) -> tuple[float, float]:
        min_x, min_y = coords[0][0], coords[0][1]
        for x, y in coords:
            y = -y
            if x < min_x:
                min_x = x
            if y < min_y:
                min_y = y

        return min_x, min_y
