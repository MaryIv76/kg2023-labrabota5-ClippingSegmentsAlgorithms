import math


class Segment:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    @property
    def normal(self):
        return Point(self.end.y - self.start.y, self.start.x - self.end.x)

    @property
    def direction(self):
        return Point(self.end.x - self.start.x, self.end.y - self.start.y)

    def intersection_parameter(self, edge):
        segment = self

        segment_to_edge = edge.start.sub(segment.start)
        segment_dir = segment.direction
        edge_dir = edge.direction

        t = edge_dir.cross(segment_to_edge) / edge_dir.cross(segment_dir)

        if math.isnan(t):
            t = 0
        return t

    def get_visible_segment(self, t_bottom, t_top):
        d = self.direction
        return Segment(self.start.add(d.mul(t_bottom)), self.start.add(d.mul(t_top)))

    def on_left(self, p):
        ab = self.end.sub(self.start)
        ap = p.sub(self.start)
        return ab.cross(ap) >= 0


class Polygon:

    def __init__(self, list_points):
        self.list_points = list_points

    @property
    def is_convex(self):
        if len(self.list_points) >= 3:
            a = len(self.list_points) - 2
            b = len(self.list_points) - 1
            for c in range(len(self.list_points)):
                if not Segment(self.list_points[a], self.list_points[b]).on_left(self.list_points[c]):
                    return False
                a = b
                b = c
        return True

    @property
    def edges(self):
        if len(self.list_points) >= 2:
            a = len(self.list_points) - 1
            for b in range(len(self.list_points)):
                yield Segment(self.list_points[a], self.list_points[b])
                a = b

    def sign(self, x):
        return -1 if x < 0 else (1 if x > 0 else 0)

    def kirus_beck_algo(self, segment):
        segm_dir = segment.direction
        t_bottom = 0.0
        t_top = 1.0
        for edge in self.edges:
            s = self.sign(edge.normal.dot(segm_dir))
            if s < 0:
                t = segment.intersection_parameter(edge)
                if t > t_bottom:
                    t_bottom = t
            elif s > 0:
                t = segment.intersection_parameter(edge)
                if t < t_top:
                    t_top = t
            elif not edge.on_left(segment.start):
                return False
        if t_bottom > t_top:
            return False
        segment = segment.get_visible_segment(t_bottom, t_top)
        return True, segment

    def kirus_beck_algo_all(self, segments):
        if not self.is_convex:
            self.list_points = self.list_points[::-1]
            if not self.is_convex:
                raise ValueError("Polygon must be convex")

        clipped_segments = []
        for segment in segments:
            clipped_segment = segment
            try:
                flag, clipped_segment = self.kirus_beck_algo(clipped_segment)
            except Exception:
                continue
            if flag:
                clipped_segments.append(clipped_segment)
        return clipped_segments


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def sub(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def mul(self, scalar):
        return Point(self.x * scalar, self.y * scalar)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def cross(self, other):
        return self.x * other.y - self.y * other.x
