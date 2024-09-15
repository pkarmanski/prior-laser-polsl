import logging
import sys
import ezdxf
import math
from typing import List, Tuple, Union
from ezdxf.document import Drawing
from app.files_processing.enums import Figures
from app.files_processing.models import Entity
from app.consts.presentation_consts import (
    CANVAS_WIDTH,
    CANVAS_HEIGHT,
)
import numpy as np


class DXFReader:
    def __init__(self, filename: str):
        self.__logger = logging.getLogger(__name__)
        self.__filename = filename
        self.__dxf = None

        self.__read_dxf_file()

    def __read_dxf_file(self):
        try:
            self.__dxf = ezdxf.readfile(self.__filename)
        except Exception as e:
            self.__logger.error(e)

    def get_dxf_file(self) -> Drawing:
        return self.__dxf

    def get_figures(self) -> List:
        msp = self.__dxf.modelspace()

        figures = [self.get_coordinates(entity) for entity in msp]
        return figures

    @staticmethod
    def get_coordinates(entity) -> Entity:
        # for entity in msp:
        entity_type = entity.dxftype()

        match entity_type:
            case Figures.LINE.value:
                # print([(entity.dxf.start.x, entity.dxf.start.y,), (entity.dxf.end.x, entity.dxf.end.y,)])
                return Entity(coords=[(entity.dxf.start.x, entity.dxf.start.y,), (entity.dxf.end.x, entity.dxf.end.y,)],
                              entity_type=Figures.LINE)

            case Figures.CIRCLE.value:
                return Entity(coords=[(entity.dxf.center.x - entity.dxf.radius, entity.dxf.center.y + entity.dxf.radius,)],
                              radius=entity.dxf.radius,
                              entity_type=Figures.CIRCLE)

            case Figures.ARC.value:
                center = entity.dxf.center
                radius = entity.dxf.radius
                start_angle = entity.dxf.start_angle
                end_angle = entity.dxf.end_angle

                return Entity(coords=[(center.x - radius, center.y + radius)],
                              radius=radius,
                              entity_type=Figures.ARC,
                              params=(start_angle, end_angle))

            case Figures.POINT.value:
                return Entity(coords=[(entity.dxf.location.x, entity.dxf.location.y,)],
                              entity_type=Figures.POINT)

            case Figures.ELLIPSE.value:
                major_axis = (entity.dxf.major_axis.x, entity.dxf.major_axis.y,)
                ratio = entity.dxf.ratio

                major_len = (math.sqrt((major_axis[0] ** 2 + major_axis[1] ** 2)))
                minor_len = major_len * ratio
                angle = math.atan2(-major_axis[1], major_axis[0])
                angle = math.degrees(angle)

                return Entity(coords=[(entity.dxf.center.x, entity.dxf.center.y)],
                              entity_type=Figures.ELLIPSE,
                              params=(major_len, minor_len),
                              angle=angle)

            case Figures.POLYLINE.value:
                return Entity(coords=[(v.dxf.location.x, v.dxf.location.y) for v in entity.vertices],
                              entity_type=Figures.POLYLINE)

            case Figures.LWPOLYLINE.value:
                point, start_width, end_width, bulge = entity
                print(f"{point=}, {start_width=}, {end_width=}, {bulge=}")
                # spline_curve = entity.construction_tool()
                # points = list(spline_curve.flattening(0.01))
                # return Entity(coords=[(p.x, p.y,) for p in points],
                #               entity_type=Figures.LWPOLYLINE)
            case Figures.SPLINE.value:
                control_points = np.array(entity.control_points)
                control_points = control_points[:, :2]

                return Entity(coords=control_points, entity_type=Figures.SPLINE)
            case _:
                print(entity_type)
                return Entity(coords=[],  entity_type=Figures.NONE)
