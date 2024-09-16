import math

from PyQt5.QtWidgets import QFileDialog

from app.presentation.components.additional_windows import Additional_Windows_Text
from app.files_processing.models import Entity
from app.files_processing.enums import Figures


class WindowUtils:
    @staticmethod
    def open_file(main_window):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        dialog.setNameFilter("CAD (*.DWG *.DWF *.DXF")
        dialog_success = dialog.exec()
        if dialog_success:
            main_window.upload_file(dialog.selectedFiles())

    @staticmethod
    def test(main_window):  # Fixme to jest zmodyfikowana twoja funkcja test która wcześniej była w pliku functions
        print(main_window.selected_files)

    @staticmethod # FIXME nie wiem czy to powinno byc statyczna metoda
    def text_window(main_window):   # FIXME zastanawiam sie czy napisac to jako funkcjie czy oddzielna klase, do okna
        main_window.text = Additional_Windows_Text
        main_window.text.show()

    @staticmethod
    def convert_float_to_int_list(float_list: list[float]) -> list[int]:
        converted = [int(x) for x in float_list]
        return converted

    @staticmethod
    def convert_list_of_list_float_to_int(float_list: list[tuple[float]]) -> list[tuple[int, int]]:
        converted = [(int(x), int(y)) for x, y in float_list]
        return converted

    @staticmethod
    def get_offset(entities: list[Entity]) -> tuple[int, int]:
        min_x = entities[0].coords[0][0]
        min_y = entities[0].coords[0][1]
        # print(f"{min_x} --- {min_y}")
        for entity in entities:
            coords = entity.coords
            if entity.entity_type == Figures.SPLINE:
                for coord in coords:
                    x = coord[0]
                    y = coord[1]
                    y = -y
                    if x < min_x:
                        min_x = x
                    if y < min_y:
                        min_y = y
                continue

            elif entity.entity_type == Figures.ELLIPSE:
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
                continue
                # x -= entity.params[0] * math.cos(math.radians(entity.angle))
                # y += math.sqrt(entity.params[0] ** 2 + entity.params[1] ** 2) * math.sin(math.radians(entity.angle))
                #
                # y *= -1
                # if x < min_x:
                #     min_x = x
                # if y < min_y:
                #     min_y = y
                # continue

            for x, y in coords:
                y = -y
                if x < min_x:
                    min_x = x
                if y < min_y:
                    min_y = y
        print(f"{min_x} --- {min_y}")
        return min_x, min_y
