import logging
import sys
import ezdxf
import math
from typing import List, Tuple, Union
from ezdxf.document import Drawing
from app.files_processing.enums import Figures


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
    def get_coordinates(entity) -> Tuple[List, Union[int, list, None], Union[Figures, str]]:
        entity_type = entity.dxftype()
        match entity_type:
            case Figures.LINE.value:
                return [(entity.dxf.start.x, entity.dxf.start.y,),
                        (entity.dxf.end.x, entity.dxf.end.y,)], None, Figures.LINE

            case Figures.CIRCLE.value:
                return [(entity.dxf.center.x, entity.dxf.center.y,)], entity.dxf.radius, Figures.CIRCLE

            case Figures.ARC.value:
                start_angle = entity.dxf.start_angle
                end_angle = entity.dxf.end_angle
                center = (entity.dxf.center.x, entity.dxf.center.y,)
                radius = entity.dxf.radius

                start_point = (
                    center[0] + radius * math.cos(math.radians(start_angle)),
                    center[1] + radius * math.sin(math.radians(start_angle)),
                )
                end_point = (
                    center[0] + radius * math.cos(math.radians(end_angle)),
                    center[1] + radius * math.sin(math.radians(end_angle)),
                )
                return [start_point, center, end_point], radius, Figures.ARC

            case Figures.POINT.value:
                return [(entity.dxf.location.x, entity.dxf.location.y,)], None, Figures.POINT

            case Figures.ELLIPSE.value:
                center = (entity.dxf.center.x, entity.dxf.center.y,)
                major_axis = (entity.dxf.major_axis.x, entity.dxf.major_axis.y,)
                ratio = entity.dxf.ratio
                start_param = entity.dxf.start_param
                end_param = entity.dxf.end_param
                return [center], [major_axis, ratio, start_param, end_param], Figures.ELLIPSE

            case Figures.LWPOLYLINE.value:
                points = [(v.dxf.location.x, v.dxf.location.y) for v in entity.vertices]
                return points, None, Figures.LWPOLYLINE

            case Figures.POLYLINE.value:
                spline_curve = entity.construction_tool()
                points = list(spline_curve.flattening(0.01))
                return [(p.x, p.y,) for p in points], None, Figures.SPLINE
            case _:
                return [], None, Figures.NONE
