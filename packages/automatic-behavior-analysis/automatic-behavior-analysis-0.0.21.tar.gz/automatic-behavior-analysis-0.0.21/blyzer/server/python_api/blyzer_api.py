import requests
from time import sleep

import io
import numpy as np
import matplotlib.pyplot as plt


class InferenceApi():
    def __init__(self, ip="172.0.0.1", port=1217):
        self.ip = ip
        self.port = port

    def upload_image(self, encoded_image):
        file = {'file': ('image.jpg', encoded_image.tostring(),
                         'image/jpeg', {'Expires': '0'})}
        try:
            r = requests.post(
                'http://{}:{}/api/blyzer/storage/image'.format(self.ip, self.port), files=file)
        except requests.exceptions.ConnectionError:
            return None

        if r.status_code != 202:
            print("Wrong request", r.content)
            return None
        print(r.json())
        return r.json()['task_id']

    def upload_video(self, video_path, progress:int = 0):
        file = {'file': ('video.mp4', open(video_path,'rb'),
                         'video/mp4', {'Expires': '0'})}
        try:
            r = requests.post(
                'http://{}:{}/api/blyzer/storage/video/{}'.format(self.ip, self.port, progress), files=file)
        except requests.exceptions.ConnectionError:
            return None

        if r.status_code != 202:
            print("Wrong request", r.content)
            return None
        print(r.json())
        return r.json()['task_id']

    def get_result(self, task_id):
        print("request {}".format(task_id))
        r = requests.get(
            'http://{}:{}/api/blyzer/task/{}/result'.format(self.ip, self.port, task_id))
        if r.status_code == 200:
            print(r.json()['result'])
            return r.json()['result'], True
        elif r.status_code == 206:
            #Частичный ответ
            return r.json()['result'], False
        else:
            return None, None

    def upload_model(self, model_path):
        file = {'file': ('model.zip', open(model_path, 'rb'),
                         'application/zip', {'Expires': '0'})}
        try:
            r = requests.post(
                'http://{}:{}/api/blyzer/model/upload'.format(self.ip, self.port), files=file)
        except requests.exceptions.ConnectionError:
            return None

        if r.status_code != 202:
            print("Wrong request", r.content)
            return None
        print(r.json())
        return r.json()['task_id']
