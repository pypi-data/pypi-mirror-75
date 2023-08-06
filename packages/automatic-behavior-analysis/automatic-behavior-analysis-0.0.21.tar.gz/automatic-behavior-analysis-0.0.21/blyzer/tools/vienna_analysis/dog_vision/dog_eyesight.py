from Line import *
from Point import *
from csv_helper import *
import cv2
from Vienna_lines_screens import *
from shapely.geometry.polygon import Polygon
import shapely.geometry

class Dog_Eyesight:
    def __init__(self, head, nose, height, width, Theta = 30):
        self.head = head
        self.nose = nose
        self.Theta = Theta
        self.width = width
        self.height = height

    def calc_field_of_vision(self):
        l1 = Line(self.head, self.nose)
        l2 = l1.rotate_line(math.radians(self.Theta))
        l3 = l1.rotate_line(math.radians(-self.Theta))
        l2.extend_line(self.width, self.height)
        l3.extend_line(self.width, self.height)
        return l2, l3

    def draw_field_of_vision(self, frame):
        left, right = self.calc_field_of_vision()
        cv2.line(frame, (left.get_p1().getX(), left.get_p1().getY()), (left.get_p2().getX(),
                                                                       left.get_p2().getY()), (255, 0, 0))
        cv2.line(frame, (right.get_p1().getX(), right.get_p1().getY()), (right.get_p2().getX(),
                                                                         right.get_p2().getY()), (255, 0, 0))


        return frame

    def is_visible(self, point_of_interest):
        left, right = self.calc_field_of_vision()
        leftp = shapely.geometry.Point(left.get_p2().getX(), left.get_p2().getY())
        rightp = shapely.geometry.Point(right.get_p2().getX(), right.get_p2().getY())
        headp = shapely.geometry.Point(self.head.getX(), self.head.getY())
        poly = Polygon([(leftp.x, leftp.y), (rightp.x, rightp.y), (headp.x, headp.y)])
        poi = shapely.geometry.Point(point_of_interest.getX(), point_of_interest.getY())
        if poly.contains(poi):
            return True
        return False


def display_dog_eye_sight(path, csv_name, vid_name):

    cap = cv2.VideoCapture(path + vid_name)
    iter_rows = iter(csv_helper(path+csv_name).csv_generator())
    next(iter_rows)
    next(iter_rows)
    next(iter_rows)
    count = 0
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(vid_name.split('.')[0] + '_final.mp4', fourcc, fps, (int(width), int(height)))
    accuracy = 0.85
    screens_mark_size = 25
    ret, frame = cap.read()
    data = get_data(frame)
    '''SCREEN CENTERS'''
    center_left_screen = Point((data[3][0]+data[2][0])/2, (data[3][1]+data[2][1])/2)
    center_right_screen = Point((data[4][0]+data[5][0])/2, (data[4][1]+data[5][1])/2)
    left_screen_seconds = 0
    right_screen_seconds = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if ret == False:
            break
        count = count + 1
        try:
            '''CSV ITERATOR'''
            row = next(iter_rows)
        except:
            break
        row = row.split(',')
        head_likehood = float(row[3])
        nose_likehood = float(row[6])
        frame = cv2.circle(frame, (center_left_screen.getX(), center_left_screen.getY()), screens_mark_size, (0, 0, 255))
        frame = cv2.circle(frame, (center_right_screen.getX(), center_right_screen.getY()), screens_mark_size, (0, 0, 255))
        if head_likehood > accuracy and nose_likehood > accuracy:
            head = Point(float(row[1]), float(row[2]))
            nose = Point(float(row[4]), float(row[5]))
            """NEW INSTANCE"""
            DE = Dog_Eyesight(head, nose, height, width)
            frame = DE.draw_field_of_vision(frame)

            #------------test--------------
            if DE.is_visible(center_left_screen):
                frame = cv2.circle(frame, (center_left_screen.getX(), center_left_screen.getY()), screens_size, (0, 255, 0))
                left_screen_seconds += 1

            if DE.is_visible(center_right_screen):
                frame = cv2.circle(frame, (center_right_screen.getX(), center_right_screen.getY()), screens_size, (0, 255, 0))
                right_screen_seconds += 1
            #------------------------------

            cv2.imshow('a',  frame)
            out.write(frame)

        else:
            cv2.imshow('a', frame)
            out.write(frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    left_screen_seconds /= fps
    right_screen_seconds /= fps
    out.release()
    cap.release()
    cv2.destroyAllWindows()  # destroy all the opened windows

path = '/home/gabi/Videos/splitted_videos/'
vid_name = 'Velvet_session_1_trial_1DLC_resnet50_ViennaJan15shuffle1_34000_labeled.mp4'
csv_name = 'Velvet_session_1_trial_1DLC_resnet50_ViennaJan15shuffle1_34000.csv'
display_dog_eye_sight(path, csv_name, vid_name)
