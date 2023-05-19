import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button
import numpy as np

from KirusBeckAlgorithm import Point, Polygon, Segment
from SutherlandCohenAlgorithm import SutherlandCohenAlgorithm

global segments
global rectangle
global polygon
global figure_type
global figure_points


def read_data(file_name):
    global segments
    global rectangle
    global polygon
    global figure_type
    global figure_points

    with open(file_name) as file:
        figure_type = file.readline()
        figure_type = figure_type.strip()

        num_segments = int(file.readline())
        segments = []
        for i in range(num_segments):
            segment = file.readline()
            segment = segment.strip()
            segment = segment.split(" ")
            x1 = float(segment[0])
            y1 = float(segment[1])
            x2 = float(segment[2])
            y2 = float(segment[3])
            segments.append((x1, y1, x2, y2))

        figure_points = []
        num_figure_points = int(file.readline())
        for i in range(num_figure_points):
            point = file.readline()
            point = point.strip()
            point = point.split(" ")
            x1 = float(point[0])
            y1 = float(point[1])
            figure_points.append((x1, y1))

        rectangle = None
        if figure_type == "rectangle":
            x_min = figure_points[0][0]
            x_max = figure_points[0][0]
            y_min = figure_points[0][1]
            y_max = figure_points[0][1]
            for point in figure_points:
                x_min = min(x_min, point[0])
                x_max = max(x_max, point[0])
                y_min = min(y_min, point[1])
                y_max = max(y_max, point[1])
            rectangle = (x_min, y_min, x_max, y_max)

        polygon = []
        for point in figure_points:
            polygon.append(Point(point[0], point[1]))


def draw_segments(segments, segm_color):
    for segment in segments:
        x1, y1, x2, y2 = segment
        x = np.array([x1, x2])
        y = np.array([y1, y2])
        plt.plot(x, y, color=segm_color)


def draw_segments_and_polygon(segments, polygon, visible_segments, init):
    x = np.array([])
    y = np.array([])

    plt.subplot(1, 2, 1)
    plt.cla()

    for point in polygon:
        x = np.append(x, point.x)
        y = np.append(y, point.y)
    x = np.append(x, polygon[0].x)
    y = np.append(y, polygon[0].y)
    color = 'black'
    plt.plot(x, y, color=color)

    draw_segments(segments, 'blue')
    if visible_segments is not None:
        draw_segments(visible_segments, 'red')

    if tb_scale.text != "":
        try:
            scale = int(tb_scale.text)
            plt.xlim(-scale, scale)
            plt.ylim(-scale, scale)
            plt.gca().set_aspect('equal', adjustable='box')
        except Exception:
            print("Scale error")

    plt.title("Отсечение отрезков")
    plt.xlabel("x")
    plt.ylabel("y")

    plt.grid(True)

    if not init:
        plt.show()


def on_btn_show_click(event):
    file = tb.text
    read_data(file)
    draw_segments_and_polygon(segments, polygon, None, False)


def on_btn_sutherland_cohen_click(event):
    if figure_type == "rectangle":
        sutherland_cohen = SutherlandCohenAlgorithm(segments, rectangle)
        draw_segments_and_polygon(segments, polygon, sutherland_cohen.result_segments, False)


def on_btn_kirus_beck_click(event):
    segments_for_polygon = []
    for segment in segments:
        segments_for_polygon.append(Segment(Point(segment[0], segment[1]), Point(segment[2], segment[3])))

    kirus = Polygon(polygon)
    result = kirus.kirus_beck_algo_all(segments_for_polygon)

    result_segments = []
    for segment in result:
        result_segments.append([segment.start.x, segment.start.y, segment.end.x, segment.end.y])

    draw_segments_and_polygon(segments, polygon, result_segments, False)


file = "sutherland_cohen.txt"
# file = "kirus_beck.txt"

plt.figure(figsize=(12, 5))

text_box = plt.axes([0.65, 0.9, 0.2, 0.07])
ax_tb = plt.gca()
tb = TextBox(text_box, "Название файла: ")
tb.set_val(file)

text_box = plt.axes([0.65, 0.2, 0.2, 0.07])
ax_tb_scale = plt.gca()
tb_scale = TextBox(text_box, "Масштаб: ")
tb_scale.set_val("")

read_data(file)
draw_segments_and_polygon(segments, polygon, None, True)

axes_button_show = plt.axes([0.65, 0.8, 0.2, 0.07])
btn_show = Button(axes_button_show, 'Показать исходные данные')
btn_show.on_clicked(on_btn_show_click)

axes_button_sutherland_cohen = plt.axes([0.65, 0.6, 0.2, 0.07])
btn_sutherland_cohen = Button(axes_button_sutherland_cohen, 'Сазерленд-Коэн')
btn_sutherland_cohen.on_clicked(on_btn_sutherland_cohen_click)

axes_button_kirus_beck = plt.axes([0.65, 0.5, 0.2, 0.07])
btn_kirus_beck = Button(axes_button_kirus_beck, 'Кирус-Бек')
btn_kirus_beck.on_clicked(on_btn_kirus_beck_click)

plt.show()
