#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import sys
import os
import cv2
from abc import abstractmethod
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtCore import Qt, QObject
from PyQt5.QtCore import QCoreApplication

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from video2nnMediaSource import Video2nnMediaSource
from util.video_tools import VideoSaver
from client.config import ClientConfig
import statistic_holder


class DogExtractorVideoSaver(VideoSaver):
    def __init__(self, path, fps, width, height):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # TODO: put video output format into the config file
        print("DogExtractorVideoSaver.__init__: fourcc: {}, fps: {}, width: {}, height: {}".format(fourcc, fps, width,
                                                                                                   height))
        self.writer = cv2.VideoWriter(path, fourcc, fps, (width, height))

    @staticmethod
    def get_base_meta(vidcap):
        """
        get metadata of the video
        Args:
            vidcap: video writer object
        """
        fps = int(vidcap.get(cv2.CAP_PROP_FPS))
        width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return fps, width, height

    @staticmethod
    def make_file_name(base_filename, vidcap):
        fps = int(vidcap.get(cv2.CAP_PROP_FPS))
        pos = round(vidcap.get(cv2.CAP_PROP_POS_FRAMES))

        base_start_time = statistic_holder.filename2time(base_filename)
        start_time = statistic_holder.frame2time(base_start_time, pos, fps)
        return base_filename[0:3] + start_time.strftime('%Y%m%d%H%M%S')

    @staticmethod
    def create(config, output_dir, base_filename, vidcap):
        """

        create video writer object

        Args:
            config: path to folder to config
            output_dir: path to folder
            base_filename: filename  of the video
            vidcap: video writer object

        Returns: creates DogExtractorVideoSaver

        """
        output_dir = output_dir or config.frame_dump_dir

        fps, width, height = DogExtractorVideoSaver.get_base_meta(vidcap)

        file_name = DogExtractorVideoSaver.make_file_name(base_filename, vidcap)
        path = os.path.join(output_dir, "{}.{}".format(file_name, config.video_extension))
        return DogExtractorVideoSaver(path, fps, width, height)

    def open_writer(self, config, output_dir, base_filename, vidcap):
        """
        opens the writer for writing
        Args:
            config: path to folder to config
            output_dir: path to folder
            base_filename: filename  of the video
            vidcap: video writer object
        """
        output_dir = output_dir or config.frame_dump_dir
        fps, width, height = DogExtractorVideoSaver.get_base_meta(vidcap)

        file_name = DogExtractorVideoSaver.make_file_name(base_filename, vidcap)
        path = os.path.join(output_dir, "{}.{}".format(file_name, config.video_extension))

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # TODO: put video output format into the config file
        print("VideoSaver.__init__: fourcc: {}, fps: {}, width: {}, height: {}".format(fourcc, fps, width, height))
        cv2.VideoWriter.open(self.writer, path, fourcc, fps, (width, height))


class DogExtractorMediaSource(Video2nnMediaSource):
    end_file_signal = pyqtSignal()

    def __init__(self, config):
        super().__init__(config)

    def set_video_param(self):
        self._dir_path = self._config.frame_dump_dir
        os.makedirs(self._dir_path, exist_ok=True)

        self._base_filename = os.path.splitext(os.path.basename(self._video_path))[0]
        self._video_saver = DogExtractorVideoSaver.create(self._config, self._dir_path, self._base_filename,
                                                          self._vidcap)
        self.dog_on_prev_frame = False

    @abstractmethod
    def postProcess(self, data):
        image = data['image']
        response = data['response']
        dogs = response['dogs']

        response = self._request_postprocessor.process_frame(image, response)

        if dogs:
            if self._video_saver.writer.isOpened():
                self._video_saver.add_frame(image)
            else:
                self._video_saver.open_writer(self._config, self._dir_path, self._base_filename, self._vidcap)
                self._video_saver.add_frame(image)
            self.dog_on_prev_frame = True
        elif self._video_saver.writer.isOpened():
            if self.dog_on_prev_frame:
                self._video_saver.close()
            self.dog_on_prev_frame = False

        # здесь сохраняется прогресс
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.save_frame(image, data['response']['frame_index'])

        # self.onNewFrameAnnotation.emit(response)
        print(response["frame_index"])

        if response["frame_index"] + self._freq > self._frame_count:
            self.end_file_signal.emit()
        return image

    @abstractmethod
    def get_next_image(self):
        self._freq = int(self._fps / self._config.frequency)  # frame skip frequency
        if self._freq > 0:
            pos = round(self._vidcap.get(cv2.CAP_PROP_POS_FRAMES))
            if self._video_saver.writer.isOpened():
                end_pos = pos + self._freq
                while pos < end_pos:
                    success, image = self._vidcap.read()
                    pos = round(self._vidcap.get(cv2.CAP_PROP_POS_FRAMES))
                    if success:
                        self._video_saver.add_frame(image)
            else:
                self._vidcap.set(cv2.CAP_PROP_POS_FRAMES, pos + self._freq)

        check = True
        while check:
            frame_index = int(self._vidcap.get(cv2.CAP_PROP_POS_FRAMES))
            success, image = self._vidcap.read()
            if not success: return None, None
            self._image_number = frame_index
            check = self.has_cached_image(self._image_number)
        return frame_index, image

    @abstractmethod
    def getFrameLoader(self):
        """
        Возвращает функцию(!) для загрузки следующего фрейма
        """
        return self.get_next_image

    @abstractmethod
    def getFramePostProcessor(self):
        """
        Возвращает функцию для синхронной постобработки фрейма после его получения
        """
        return self.postProcess


class DogExtractor(QObject):
    setVideoSrc = pyqtSignal(str)

    def __init__(self, config):
        super().__init__(None)
        self._config = config
        self._files_for_processsing = []
        if self._config.dir is not None:
            for filename in os.listdir(self._config.dir):
                if not filename.endswith(".mp4"): continue
                self._files_for_processsing.append(os.path.join(self._config.dir, filename))
        else:
            self._files_for_processsing.append(self._config.file)

        self._media_source = DogExtractorMediaSource(config)
        self.setVideoSrc.connect(self._media_source.set_source)
        self._media_source.end_file_signal.connect(self.on_end_file)
        self.start()

    def start(self):
        self.setVideoSrc.emit(self._files_for_processsing.pop())

    @pyqtSlot()
    def on_end_file(self):
        if self._files_for_processsing.count() > 0:
            self.setVideoSrc.emit(self._files_for_processsing.pop())
        else:
            QCoreApplication.instance().quit()


def main():
    config = ClientConfig(os.path.join(os.path.dirname(__file__), "config.json"))
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help="Video file")
    parser.add_argument('-d', '--dir', help="Directory with video files")
    parser.add_argument('--ip', help="Server IP address or hostname", default=argparse.SUPPRESS)
    parser.add_argument('--port', help="Server port", type=int, default=argparse.SUPPRESS)
    parser.add_argument('--protocol', default=config.protocol, help="Server protocol", choices=['tcp', 'websocket'])
    parser.add_argument('--frequency', help="", default=1, type=int)
    parser.add_argument('--verbose', help="Show detailed debug messages", action='store_true')
    parser.add_argument('--media_source_type',
                        default=config.media_source_type,
                        help="Type of mediasource. Can be: simpleCam, nnCam",
                        choices=['simpleCam', 'nnCam', 'nnVideo'])
    parser.add_argument('input_file', nargs='?', help="Input file")
    args = vars(parser.parse_args())
    config.update(args)
    config.inner_detection = False

    app = QCoreApplication(sys.argv)
    dog_extractor = DogExtractor(config)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
