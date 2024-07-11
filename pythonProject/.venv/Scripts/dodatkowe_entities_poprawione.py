import logging
import sys
import ezdxf
import math
import numpy as np
from typing import List, Tuple, Union
from ezdxf.document import Drawing
from app.stage.enums.figures import Figures

class DXFReader:
    def __init__(self):
        self.__logger = logging.getLogger(__name__)

    def read_dxf_file(self, file_path: str) -> Union[Drawing, None]:
        try:
            return ezdxf.readfile(file_path)
        except Exception as e:
            self.__logger.error(e)
            print(e)
            return None

    @staticmethod
    def get_coordinates(entity) -> Tuple[List, Union[Tuple, None], Union[Figures, str]]:
        if entity.dxftype() == Figures.LINE.value:
            return [(entity.dxf.start.x, entity.dxf.start.y, entity.dxf.start.z),
                    (entity.dxf.end.x, entity.dxf.end.y, entity.dxf.end.z)], None, Figures.LINE
        elif entity.dxftype() == Figures.CIRCLE.value:
            return [(entity.dxf.center.x, entity.dxf.center.y, entity.dxf.center.z)], entity.dxf.radius, Figures.CIRCLE
        elif entity.dxftype() == Figures.ARC.value:
            start_angle = entity.dxf.start_angle
            end_angle = entity.dxf.end_angle
            center = (entity.dxf.center.x, entity.dxf.center.y, entity.dxf.center.z)
            radius = entity.dxf.radius

            start_point = (
                center[0] + radius * math.cos(math.radians(start_angle)),
                center[1] + radius * math.sin(math.radians(start_angle)),
                center[2]
            )
            end_point = (
                center[0] + radius * math.cos(math.radians(end_angle)),
                center[1] + radius * math.sin(math.radians(end_angle)),
                center[2]
            )
            return [start_point, center, end_point], radius, Figures.ARC
        elif entity.dxftype() == Figures.POINT.value:
            return [(entity.dxf.location.x, entity.dxf.location.y, entity.dxf.location.z)], None, Figures.POINT
        elif entity.dxftype() == Figures.ELLIPSE.value:
            center = (entity.dxf.center.x, entity.dxf.center.y, entity.dxf.center.z)
            major_axis = (entity.dxf.major_axis.x, entity.dxf.major_axis.y, entity.dxf.major_axis.z)
            ratio = entity.dxf.ratio
            start_param = entity.dxf.start_param
            end_param = entity.dxf.end_param
            return [center], (major_axis, ratio, start_param, end_param), Figures.ELLIPSE
        elif entity.dxftype() == Figures.LWPOLYLINE.value:
            points = [(point[0], point[1]) for point in entity]
            return points, None, Figures.LWPOLYLINE
        elif entity.dxftype() == Figures.POLYLINE.value:
            polyline_type = entity.get_mode()
            if polyline_type == 'AcDb2dPolyline':
                points = [(v.dxf.location.x, v.dxf.location.y) for v in entity.vertices]
                return points, None, Figures.AcDb2dPolyline
            elif polyline_type == 'AcDb3dPolyline':
                points = [(v.dxf.location.x, v.dxf.location.y, v.dxf.location.z) for v in entity.vertices]
                return points, None, Figures.AcDb3dPolyline
            elif polyline_type == 'AcDbPolygonMesh':
                points = [(v.dxf.location.x, v.dxf.location.y, v.dxf.location.z) for v in entity.vertices]
                return points, None, Figures.AcDbPolygonMesh
            elif polyline_type == 'AcDbPolyFaceMesh':
                points = [(v.dxf.location.x, v.dxf.location.y, v.dxf.location.z) for v in entity.vertices]
                return points, None, Figures.AcDbPolyFaceMesh
        elif entity.dxftype() == Figures.SPLINE.value:
            spline_curve = entity.construction_tool()
            points = list(spline_curve.flattening(0.01))  # Adjust the distance tolerance as needed
            return [(p.x, p.y, p.z) for p in points], None, Figures.SPLINE
        return [], None, entity.dxftype()

if __name__ == "__main__":
    file_path = r"C:\Users\matri\OneDrive\Dokumenty\kwadrat(10000x100)zarc.dxf"
    reader = DXFReader()
    doc = reader.read_dxf_file(file_path)
    if doc:
        print("DXF file read successfully!")

    msp = doc.modelspace()
    found_ellipse = False

    for entity in msp:
        coords, details, entity_type = reader.get_coordinates(entity)
        if entity_type == Figures.CIRCLE and details is not None:
            for coord in coords:
                print(f"Coordinate: {coord}, Radius: {details}, Type: {entity_type}")
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
                print(f"Start Coordinate: {start}, Center Coordinate: {center}, End Coordinate: {end}, Radius: {details}, Type: {entity_type}")
        elif entity_type == Figures.ELLIPSE and details is not None:
            center = coords[0]
            major_axis, ratio, start_param, end_param = details
            print(f"Center: {center}, Major Axis: {major_axis}, Ratio: {ratio}, Start Param: {start_param}, End Param: {end_param}, Type: {entity_type}")
            found_ellipse = True
        elif entity_type == Figures.LWPOLYLINE:
            print(f"LWPOLYLINE with coordinates: {coords}")
        elif entity_type == Figures.AcDb2dPolyline:
            print(f"2D POLYLINE with coordinates: {coords}")
        elif entity_type == Figures.AcDb3dPolyline:
            print(f"3D POLYLINE with coordinates: {coords}")
        elif entity_type == Figures.AcDbPolygonMesh:
            print(f"POLYGON MESH with coordinates: {coords}")
        elif entity_type == Figures.AcDbPolyFaceMesh:
            print(f"POLYFACE MESH with coordinates: {coords}")
        elif entity_type == Figures.SPLINE:
            print(f"SPLINE with flattened points: {coords}")
        else:
            for coord in coords:
                print(f"Coordinate: {coord}, Type: {entity_type}")

    if not found_ellipse:
        print("No ellipse entities found in the DXF file.")