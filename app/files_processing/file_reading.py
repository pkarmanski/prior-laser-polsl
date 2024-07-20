import logging
import sys
import ezdxf
import math
from typing import List, Tuple, Union
from ezdxf.document import Drawing
from app.files_processing.enums import Figures


class DXFReader:
    def __init__(self):
        self.__logger = logging.getLogger(__name__)

    def read_dxf_file(self, file_path: str) -> Union[Drawing, None]:
        try:
            return ezdxf.readfile(file_path)
        except Exception as e:
            self.__logger.error(e)
            print(e)

    @staticmethod
    def get_coordinates(entity) -> Tuple[List, Union[int, list, None], Union[Figures, str]]:
        entity_type = entity.dxftype()
        if entity_type == Figures.LINE.value:
            return [(entity.dxf.start.x, entity.dxf.start.y,),
                    (entity.dxf.end.x, entity.dxf.end.y,)], None, Figures.LINE

        elif entity_type == Figures.CIRCLE.value:
            return [(entity.dxf.center.x, entity.dxf.center.y,)], entity.dxf.radius, Figures.CIRCLE

        elif entity_type == Figures.ARC.value:
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

        elif entity_type == Figures.POINT.value:
            return [(entity.dxf.location.x, entity.dxf.location.y,)], None, Figures.POINT

        elif entity_type == Figures.ELLIPSE.value:
            center = (entity.dxf.center.x, entity.dxf.center.y,)
            major_axis = (entity.dxf.major_axis.x, entity.dxf.major_axis.y,)
            ratio = entity.dxf.ratio
            start_param = entity.dxf.start_param
            end_param = entity.dxf.end_param
            return [center], [major_axis, ratio, start_param, end_param], Figures.ELLIPSE

        elif entity_type == Figures.LWPOLYLINE.value:
            points = [(v.dxf.location.x, v.dxf.location.y) for v in entity.vertices]
            return points, None, Figures.LWPOLYLINE

        elif entity_type == Figures.POLYLINE.value:
            spline_curve = entity.construction_tool()
            points = list(spline_curve.flattening(0.01))  # Adjust the distance tolerance as needed
            return [(p.x, p.y,) for p in points], None, Figures.SPLINE

        return [], None, Figures.NONE


if __name__ == "__main__":
    file_path = r"C:\Users\blach\PycharmProjects\prior-laser-polsl\eo4kry7j.dxf"
    reader = DXFReader()
    doc = reader.read_dxf_file(file_path)
    if doc:
        print("DXF file read successfully!")

    msp = doc.modelspace()

    for entity in msp:
        coords, radius, entity_type = reader.get_coordinates(entity)
        if entity_type == Figures.CIRCLE and radius is not None:
            for coord in coords:
                print(f"Coordinate: {coord}, Radius: {radius}, Type: {entity_type}")
        elif entity_type == Figures.LINE:
            if len(coords) == 2:
                start = coords[0]
                end = coords[1]
                print(f"Start Coordinate: {start}, End Coordinate: {end}, Type: {entity_type}")
        elif entity_type == Figures.ARC:
            if len(coords) == 3:
                start = coords[0]
                center = coords[1]
                end = coords[2]
                print(f"Start Coordinate: {start}, Center Coordinate: {center}, End Coordinate: {end}, Radius: {radius}, Type: {entity_type}")
        else:
            for coord in coords:
                print(f"Coordinate: {coord}, Type: {entity_type}")
