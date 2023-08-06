import cv2
import numpy as np

def calc_text_format(show_name, show_rate, show_type):
    text_format = ""
    if show_name:
        text_format += "[{name}]"
    if show_type:
        text_format +=  " {type}"
    if show_rate:
        text_format += " {rate:.2%}"
    return text_format

def draw_boundingbox(image:np.array, 
                     xmin, 
                     ymin, 
                     xmax, 
                     ymax, 
                     text_format, 
                     color,
                     category,
                     rate, 
                     name:str=""):
    im_height, im_width, *_ = image.shape
    text = text_format.format(name=name, type=category, rate = rate)
    image = draw_item(image, xmin, ymin, xmax, ymax, color, int(3*(im_width/720)), text, 0.4*(im_width/720))
    return image

def draw_keypoint(image:np.array, x, y, rate, color=(0, 255, 0), category=""):
    im_height, im_width, *_ = image.shape
    image = cv2.circle(image, (x,y), int(im_width / 120), color, -1)
    return image

def draw_object(image:np.array, item:dict, text_format, color, name:str="", keypoints_conf_threshold:float=0.5):
    im_height, im_width, *_ = image.shape
    xmin = int(im_width * item['coordinates']['x1'])
    ymin = int(im_height * item['coordinates']['y1'])
    xmax = int(im_width * item['coordinates']['x2'])
    ymax = int(im_height * item['coordinates']['y2'])
    draw_boundingbox(image,
                     xmin,
                     ymin,
                     xmax,
                     ymax,
                     text_format,
                     color,
                     category=item['category'],
                     rate=item['rate'],
                     name=name)

    if item['keypoints']:
        for name, kp in item['keypoints'].items():
            if kp and kp['rate']>keypoints_conf_threshold:
                x = int(xmin + (xmax - xmin) * kp['x'])
                y = int(ymin + (ymax - ymin) * kp['y'])
                image = draw_keypoint(image, x, y, kp['rate'], (0, 255, 0), name)
    return image

def draw_item(image, xmin, ymin, xmax, ymax, color, thickness, text, text_size):
    text_y_offset = 7
    font = cv2.FONT_HERSHEY_SIMPLEX
    image = cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, thickness)
    if text is None: return image

    text_x = xmin
    text_y = ymin - text_y_offset

    if text_y < 10:
        text_y = ymax + text_y_offset * 2

    return cv2.putText(image, text, (text_x, text_y), font, text_size, (52, 211, 152), 1, cv2.LINE_AA)