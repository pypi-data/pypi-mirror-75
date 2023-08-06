import cv2
import numpy as np
import argparse
import sys

LEFT_SCREEN_RATIO = 0.35
RIGHT_SCREEN_RATIO = 0.63
HORIZONTAL_LINE_RATIO = 0.5
VERTICAL_LINE_RATIO = 0.56
SCREEN_WIDTH = 160
SCREEN_HEIGHT = 60


def get_co(borders_tl_x, borders_tl_y, borders_br_x, borders_br_y):
    """
    :param borders_tl_x: X coordinate of Top-Left point of the expriment space
    :param borders_tl_y:
    :param borders_br_x:
    :param borders_br_y:
    :return: X axis of Horizontal separation line, Y axis of vertical separation, left screen Top-Left Coordinates, left
    screen Bottom-Right Coordinates, right screen Top-Left Coordinates, right screen Bottom-Right Coordinates
    """
    tmp_x = borders_tl_x + borders_br_x
    tmp_y = borders_tl_y + borders_br_y
    Horizontal_line_x = int(tmp_x * HORIZONTAL_LINE_RATIO)
    Vertical_line_y = int(tmp_y * VERTICAL_LINE_RATIO)
    Left_screen_center = (tmp_x * LEFT_SCREEN_RATIO, borders_br_y)
    Right_screen_center = (tmp_x * RIGHT_SCREEN_RATIO, borders_br_y)
    Left_screen_TL = (int(Left_screen_center[0]-SCREEN_WIDTH/2), int(Left_screen_center[1]+SCREEN_HEIGHT/2))
    Left_screen_BR = (int(Left_screen_center[0] + SCREEN_WIDTH / 2), int(Left_screen_center[1] - SCREEN_HEIGHT / 2))
    Right_screen_TL = (int(Right_screen_center[0] - SCREEN_WIDTH / 2), int(Right_screen_center[1] + SCREEN_HEIGHT / 2))
    Right_screen_BR = (int(Right_screen_center[0] + SCREEN_WIDTH / 2), int(Right_screen_center[1] - SCREEN_HEIGHT / 2))
    return Horizontal_line_x, Vertical_line_y, Left_screen_TL, Left_screen_BR, Right_screen_TL, Right_screen_BR


def get_image(path, frame_number):
    """
    :param path: full path to video
    :param frame_number: frame number we would like to extract from the video, usually 100 should be fine for this project.
    :return: frame number (frame_number) will be returned as np array
    """
    cap = cv2.VideoCapture(path)
    count = 0
    img = None
    while cap.isOpened():
        ret, frame = cap.read()
        count += 1
        if count == frame_number:
            img = frame
            break
    cap.release()
    cv2.destroyAllWindows()
    return img


def check_if_black(rgb):
    """
    :param rgb: 1 pixels' (R,G,B) tuple
    :return: if the pixels' color is relatively black
    """
    for color in rgb:
        if color >= 20:
            return False
    return True


def find_tl(img):
    """
    :param img: image we want to work on
    :return: Top-Left Coordinates of the experiment space
    """
    starting_check_x = 280
    starting_check_y = 290
    while check_if_black(img[starting_check_y][starting_check_x]):
        starting_check_x += 1

    starting_check_x += 3

    while not check_if_black(img[starting_check_y][starting_check_x]):
        starting_check_y -= 1

    return starting_check_x, starting_check_y


def find_br(img):
    """
    :param img: image we want to work on
    :return: Bottom-Right Coordinates of the experiment space
    """
    starting_check_x = 890
    starting_check_y = 528
    while check_if_black(img[starting_check_y][starting_check_x]):
        starting_check_x -= 1

    starting_check_x -= 3

    while not check_if_black(img[starting_check_y][starting_check_x]):
        starting_check_y += 1

    return starting_check_x, starting_check_y


def get_borders(img):
    """
    :param img: image we want to work on
    :return: TL;BR Coordinates of the experiment space
    """
    return find_tl(img), find_br(img)


def get_data(img):
    """
    :param img: image we want to work on
    :return: X axis of Horizontal separation line, Y axis of vertical separation, left screen Top-Left Coordinates, left
    screen Bottom-Right Coordinates, right screen Top-Left Coordinates, right screen Bottom-Right Coordinates
    """

    borders = get_borders(img)
    data = get_co(borders[0][0], borders[0][1], borders[1][0], borders[1][1])
    return data


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-path", type=str, help="contain full path to video file")
    args = parser.parse_args()
    if args.path is None:
        print("no path given")
        sys.exit(-1)
    img = get_image(args.path, 1)
    data = get_data(img)
    print(get_data(img))

    ### visualisation check####
    while True:
        cv2.rectangle(img, data[2], data[3], 1)
        cv2.rectangle(img, data[4], data[5], 1)
        cv2.line(img, (data[0], 0), (data[0], 720), 1)
        cv2.line(img, (0, data[1]), (1200, data[1]), 1)
        cv2.imshow('test', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break




if __name__ == '__main__':
    main()
