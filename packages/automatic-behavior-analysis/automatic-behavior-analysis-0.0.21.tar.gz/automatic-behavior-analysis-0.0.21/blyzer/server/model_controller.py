# -*- coding: utf-8 -*-
"""
Copyright (c) Wed Oct 24 18:58:55 2018 Sinitca Alekandr <amsinitca@etu.ru, siniza.s.94@gmail.com>

Created on Wed Oct 24 18:58:55 2018
@author: Sinitca Alekandr <amsinitca@etu.ru, siniza.s.94@gmail.com>
"""

import os
import numpy as np
import json

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

import tensorflow as tf
import cv2

vr_str = tf.__version__
vr_int = int(vr_str[0]) * 100 + int(vr_str[2]) * 10 + int(vr_str[2])

if vr_int > 200:
    import tensorflow.compat.v1 as tf
    tf.disable_v2_behavior()

from blyzer.server.model_wrappers.dcl_wrapper import DclModelWrapper
from blyzer.server.model_wrappers.od_wrapper import ObjectDetectionModelWrapper


class ModelController():
    def __init__(self):
        self._config = {}
        self._od_model = None

    def init_model(self, model_root:str):
        settigs_filename = os.path.join(model_root, 'blzr_config.json')
        try:
            with open(settigs_filename, 'r', encoding='utf-8') as file:
                self._config = json.load(file)
        except:
            print("Error: some troubles with configuration")

        # Disable all memory allocating
        gpus = tf.config.experimental.list_physical_devices('GPU')
        if gpus:
            try:
                for gpu in gpus:
                    tf.config.experimental.set_memory_growth(gpu, True)
            except RuntimeError as e:
                print(e)

        print("Loading ObjectDetectionModelWrapper")
        self._od_model = ObjectDetectionModelWrapper(model_root, self._config)

        self._key_point_model = None
        if self._config.get('dlc_model', None):
            print("Loading DclModelWrapper")
            self._key_point_model = DclModelWrapper(model_root, self._config['dlc_model'])

    def _decode_image(self, raw_img):
        nparr = np.frombuffer(raw_img, np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return img_np

    def _prepare_report_to_client(self, objects_report, keypoints):
        '''
        JSON_EXAMPLE see in documentation/samples/report_frame.json
        '''
        result = []

        for ind, r in enumerate(objects_report):
            item = {}
            item['id'] = ind
            item['coordinates'] = {}
            item['coordinates']['x1'] = float(r[0][1])
            item['coordinates']['y1'] = float(r[0][0])
            item['coordinates']['x2'] = float(r[0][3])
            item['coordinates']['y2'] = float(r[0][2])
            if self._key_point_model:
                item['keypoints'] = keypoints[ind]
            else:
                item['keypoints'] = {}
            item['children'] = []
            item['rate'] = float(r[1])
            item['category'] = self._od_model.category_index[r[2]]['name']
            item['attributes'] = {}
            result.append(item)

        return {'objects': result}

    def process_image(self, payload, is_decoded=False):
        """[summary]

        Parameters
        ----------
        payload : list or np.array
            [description]s
        is_decoded : bool, optional
            [description], by default False

        Returns
        -------
        dict or list of dicts
            Prediction or list of prediction for Imaged
        """
        if not is_decoded:
            image = self._decode_image(payload)
        else:
            image = payload

        objects_report = self._od_model.predict(image)
        # key points proccessing
        keypoints = []
        if self._key_point_model:
            for ind, r in enumerate(objects_report): # TODO: stack images
                category = self._od_model.category_index[r[2]]['name']
                if category == self._config.get('target_object', 'dog'): # TODO: get from config
                    y1 = int(image.shape[0] * float(r[0][0]))
                    x1 = int(image.shape[1] * float(r[0][1]))
                    y2 = int(image.shape[0] * float(r[0][2]))
                    x2 = int(image.shape[1] * float(r[0][3]))

                    y_size = y2 - y1
                    x_size = x2 - x1
                    y1_e = int(max(0, y1 - y_size * 0.2))
                    x1_e = int(max(0, x1 - x_size * 0.2))
                    y2_e = int(min(image.shape[0], y2 + y_size * 0.2))
                    x2_e = int(min(image.shape[1], x2 + x_size * 0.2))
                    crop_img_np = np.copy(image[y1_e:y2_e, x1_e:x2_e])
                    kp_obj = self._key_point_model.predict(crop_img_np)[0]
                    for pb_key in kp_obj.keys():
                        kp_obj[pb_key]['x'] = (kp_obj[pb_key]['x'] + x1_e - x1) / x_size
                        kp_obj[pb_key]['y'] = (kp_obj[pb_key]['y'] + y1_e - y1) / y_size

                    keypoints.append(kp_obj)
                else:
                    keypoints.append({})
        return self._prepare_report_to_client(objects_report, keypoints)
