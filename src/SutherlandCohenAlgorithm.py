class SutherlandCohenAlgorithm:

    def __init__(self, segments, rectangle):
        self.segments = segments
        self.rectangle = rectangle

        self.visible_segments = []
        self.segments_for_process = []

        self.characteristic_codes = self.calc_characteristic_codes()
        self.result_segments = self.process_segments()
        return

    def process_segments(self):
        for i in range(len(self.characteristic_codes)):
            cur_char_code = self.characteristic_codes[i]
            if self.sum_array(cur_char_code[0]) == 0 and self.sum_array(cur_char_code[1]) == 0:
                self.visible_segments.append(self.segments[i])
            elif not self.is_invisible(cur_char_code):
                self.segments_for_process.append(self.segments[i])

        x_min, y_min, x_max, y_max = self.rectangle
        found_segments = []
        for segment in self.segments_for_process:
            x1, y1, x2, y2 = segment

            x_min_segm = x1 if (x1 < x2) else x2
            x_max_segm = x1 if (x1 > x2) else x2
            y_min_segm = y1 if (y1 < y2) else y2
            y_max_segm = y1 if (y1 > y2) else y2

            points = set()
            if x1 != x2:
                x_right = x_max
                y_right = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
                if y_min <= y_right <= y_max:
                    if x_min_segm <= x_right <= x_max_segm and y_min_segm <= y_right <= y_max_segm:
                        point = (x_right, y_right)
                        points.add(point)

                x_left = x_min
                y_left = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
                if y_min <= y_left <= y_max:
                    if x_min_segm <= x_left <= x_max_segm and y_min_segm <= y_left <= y_max_segm:
                        point = (x_left, y_left)
                        points.add(point)

            if y1 != y2:
                y_top = y_max
                x_top = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
                if x_min <= x_top <= x_max:
                    if x_min_segm <= x_top <= x_max_segm and y_min_segm <= y_top <= y_max_segm:
                        point = (x_top, y_top)
                        points.add(point)

                y_bottom = y_min
                x_bottom = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
                if x_min <= x_bottom <= x_max:
                    if x_min_segm <= x_bottom <= x_max_segm and y_min_segm <= y_bottom <= y_max_segm:
                        point = (x_bottom, y_bottom)
                        points.add(point)

            if x_min <= x1 <= x_max and y_min <= y1 <= y_max:
                point = (x1, y1)
                points.add(point)
            if x_min <= x2 <= x_max and y_min <= y2 <= y_max:
                point = (x2, y2)
                points.add(point)

            if len(points) >= 2:
                found_segments.append(points)

        result = self.visible_segments
        for segment in found_segments:
            segment = list(segment)
            segment = (segment[0][0], segment[0][1], segment[1][0], segment[1][1])
            result.append(segment)

        return result

    def is_invisible(self, cur_char_code):
        res = 0
        if cur_char_code[0][0] == 1 and cur_char_code[1][0] == 1:
            res += 1
        if cur_char_code[0][1] == 1 and cur_char_code[1][1] == 1:
            res += 1
        if cur_char_code[0][2] == 1 and cur_char_code[1][2] == 1:
            res += 1
        if cur_char_code[0][3] == 1 and cur_char_code[1][3] == 1:
            res += 1
        return res != 0

    def calc_characteristic_codes(self):
        characteristic_codes = []
        for segment in self.segments:
            x1, y1, x2, y2 = segment
            char_code_start = self.get_characteristic_code(x1, y1)
            char_code_end = self.get_characteristic_code(x2, y2)
            current_char_code = [char_code_start, char_code_end]
            characteristic_codes.append(current_char_code)
        return characteristic_codes

    def get_characteristic_code(self, x, y):
        x_min, y_min, x_max, y_max = self.rectangle
        current_characteristic_code = []
        if y > y_max:
            current_characteristic_code.append(1)
        else:
            current_characteristic_code.append(0)
        if y < y_min:
            current_characteristic_code.append(1)
        else:
            current_characteristic_code.append(0)
        if x > x_max:
            current_characteristic_code.append(1)
        else:
            current_characteristic_code.append(0)
        if x < x_min:
            current_characteristic_code.append(1)
        else:
            current_characteristic_code.append(0)
        return current_characteristic_code

    def swap(self, x, y):
        return y, x

    def sum_array(self, array):
        res = 0
        for element in array:
            res += element
        return res
