import math

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 580

GRID_STEP = 20
GRID_WIDTH = 2

CANVAS_PEN_COLOR = '#000000'
GRAY_COLOR = '#c8c8c8'

SLIDER_MIN = 1
SLIDER_MAX = 100
SLIDER_TIC = 1

PRESENTATION_OFFSET = 20

new_scale = range(1, 101)

min_val = math.log10(0.01)
max_val = math.log10(100)

SCALE_MAPPING = {
    i: 10 ** (max_val - (i - 1) * (max_val - min_val) / 99)
    for i in new_scale
}


MAIN_PANEL_MIN_X = 1200
MAIN_PANEL_MIN_Y = 700

