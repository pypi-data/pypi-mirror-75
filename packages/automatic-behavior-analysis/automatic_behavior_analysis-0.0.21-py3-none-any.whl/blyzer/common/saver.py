#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) Mon Nov 05 19:14:09 2018 Sinitca Alekandr <amsinitca@etu.ru, siniza.s.94@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Created on Mon Nov 05 19:14:09 2018
@author: Sinitca Alekandr <amsinitca@etu.ru, siniza.s.94@gmail.com>
"""

__author__ = 'Sinitca Alekandr'
__contact__ = 'amsinitca@etu.ru, siniza.s.94@gmail.com'
__copyright__ = 'Sinitca Alekandr'
__license__ = 'MIT'
__date__ = 'Mon Nov 05 19:14:09 2018'
__version__ = '0.1'

import os
import time
import json
import cv2
from blyzer.tools.labelImg.libs.pascal_voc_io import PascalVocWriter

def save_annotation(file_name, annotation, **kwargs):
    """
    Запись аннотации в формате json
    """
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(annotation, file, **kwargs)

def load_annotation(file_name):
    """
    Загрузить аннотацию из файла в формате json
    """
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data

class FrameSaver:
    def __init__(self, config):
        self.save_json = config.annotation_format == 'json'
        self.save_xml = config.annotation_format == 'pascal-voc'
        self.output_dir = output_dir = config.get('output_dir', config.frame_dump_dir)
        sub = lambda key: config[key].replace('{frame_dump_dir}', output_dir)
        if self.save_json or self.save_xml:
            self.json_annotation_dir = sub('json_annotation_dir')
            self.xml_annotation_dir = sub('xml_annotation_dir')
            self.annotation_dir = self.json_annotation_dir if self.save_json else self.xml_annotation_dir
            self.annotation_dir_ok = False
        self.image_extension = config.get('image_extension', "jpg")
        self.noisy = config.get('verbose')

    def print(self, message):
        if self.noisy:
            print(message)

    def save(self, basename, index, image, response):
        basename_with_index = "{}_{:08d}".format(basename, index)
        image_path = os.path.join(self.output_dir, "{}.{}".format(basename_with_index, self.image_extension))
        cv2.imwrite(image_path, image)
        self.print("- saved frame {} to {}".format(index, image_path))

        if response is None: return # don't save annotation if not given a response object

        if not self.annotation_dir_ok:
            os.makedirs(self.annotation_dir, exist_ok=True)
            self.annotation_dir_ok = True

        if self.save_json:
            annotation_path = os.path.join(self.annotation_dir, basename_with_index + ".json")
            save_annotation(annotation_path, response, indent=2, sort_keys=True)
        elif self.save_xml:
            annotation_path = os.path.join(self.annotation_dir, basename_with_index + ".xml")
            self.savePascalVocFormat(annotation_path, response, image_path, image.shape)

        self.print("- saved annotation {} to {}".format(index, annotation_path))

    def savePascalVocFormat(self, filename, response, imagePath, imageShape, lineColor=None, fillColor=None, databaseSrc=None):
        imgFolderPath = os.path.dirname(imagePath)
        imgFolderName = os.path.split(imgFolderPath)[-1]
        imgFileName = os.path.basename(imagePath)
        writer = PascalVocWriter(imgFolderName, imgFileName, imageShape, localImgPath=imagePath)

        for item in response['dogs']:
            # difficult = int(shape['difficult'])
            label = 'dog-sleep' if item['state'] == 'sleep' else 'dog'

            x1 = round(item['x1'] * imageShape[1])
            x2 = round(item['x2'] * imageShape[1])
            xmin = min(x1, x2)
            xmax = max(x1, x2)

            y1 = round(item['y1'] * imageShape[0])
            y2 = round(item['y2'] * imageShape[0])
            ymin = min(y1, y2)
            ymax = max(y1, y2)

            writer.addBndBox(xmin, ymin, xmax, ymax, label, difficult=0, rate=item.get('rate'))

        writer.save(targetFile=filename)
