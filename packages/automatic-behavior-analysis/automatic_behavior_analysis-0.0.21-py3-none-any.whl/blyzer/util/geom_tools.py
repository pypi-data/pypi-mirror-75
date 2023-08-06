def rect_xmin(rect):
    return min(rect[1], rect[3])

def rect_xmax(rect):
    return max(rect[1], rect[3])

def rect_ymin(rect):
    return min(rect[0], rect[2])

def rect_ymax(rect):
    return max(rect[0], rect[2])

# Rectangle format: (y1, x1, y2, x2)
def rect_area(rect):
    return abs(rect[2] - rect[0]) * abs(rect[3] - rect[1])

def rect_overlap(a, b):
    a_xmin, a_xmax = rect_xmin(a), rect_xmax(a)
    a_ymin, a_ymax = rect_ymin(a), rect_ymax(a)
    b_xmin, b_xmax = rect_xmin(b), rect_xmax(b)
    b_ymin, b_ymax = rect_ymin(b), rect_ymax(b)
    dx = min(a_xmax, b_xmax) - max(a_xmin, b_xmin)
    dy = min(a_ymax, b_ymax) - max(a_ymin, b_ymin)
    if dx > 0 and dy > 0:
        return dx * dy
    return 0