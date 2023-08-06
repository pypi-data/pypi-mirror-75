import pandas as pd
import cv2
import numpy as np

"""
A class that create generators for frames and annotations 
"""


class Generator:

    def __init__(self, path_video, path_annotation, batch_size):  # path for the .csv
        self._filename = None
        self._batch_size = batch_size
        self._path_video = path_video
        self._path_annotation = path_annotation

    def data_detection(self):
        """generates data for the detection model"""
        for row in self.data_generator():
            arr = []
            for i, num in enumerate(row):
                if i in [40, 41, 42, 43, 84, 85, 86, 87, 128, 129, 130, 131]:
                    arr.append(num)
            yield (np.array(arr))

    def get_generator(self, detection_only=False, pose=False):
        """ generates tuple generator, each tuple contains (frames, annotations)... runs infinitely"""
        if self._filename is None:
            print("please set filename")
            return

        while True:

            if detection_only:
                data_generator = self.data_detection()  # get all data needed
            else:
                data_generator = self.data_generator()

            frame_generator = self.frame_generator()
            batch_size = self._batch_size

            frames = []
            annotations = []
            for frame, annotation in zip(frame_generator, data_generator):  # yield tuple with a batch size list inside
                frames.append(frame)
                annotations.append(annotation)
                if len(frames) == batch_size:
                    yield ((np.array(frames), np.array(annotations)))
                    frames.clear()
                    annotations.clear()
            if frames:  # yield what is left that is less then batch size
                yield ((np.array(frames), np.array(annotations)))
                frames.clear()
                annotations.clear()

    def data_generator(self):  # generator for annotations
        if self._filename is not None:
            path = self._path_annotation + self._filename
            for i in pd.read_csv(path, chunksize=1):
                yield (self.get_points(i.values[0]))
        else:
            print("please set filename, using set_filename")
            return False

    def frame_generator(self):  # generator for frames
        if self._filename is not None:
            path = self._path_video + self._filename.replace('.csv', '.mp4')
            cap = cv2.VideoCapture(path)  # open video file
            index = 0

            while cap.isOpened() and index < self._len - 1:  # keep ruining till all frames used
                ret, image = cap.read()  # give frames
                yield (image)
                index = index + 1
            cap.release()
        else:
            print("please set filename, using set_filename")
            return False

    def set_filename(self, filename):
        self._filename = filename
        vcap = cv2.VideoCapture(self._path_video + self._filename.replace('csv', 'mp4'))

        if vcap.isOpened():
            self._width = vcap.get(cv2.CAP_PROP_FRAME_WIDTH)  # gets width and height for the frames in the video
            self._height = vcap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            self._len = int(vcap.get(cv2.CAP_PROP_FRAME_COUNT))  # later will be used as a flag to stop
            vcap.release()

    # get points for BB
    def point_for_BB(self):
        for row in self.frame_generator():
            arr = []
            for i, num in enumerate(row):
                if i in [40, 41, 42, 43, 84, 85, 86, 87, 128, 129, 130, 131]:
                    arr.append(num)
            yield (np.array(arr))

    # converts values from csv to tuple list -- helper method
    def get_points(self, csv_array):
        points = []

        """
        read csv and convert it to Numpy array [x,y,x,y,x,y....]
        normalize array according to frame size 
        
        """

        for cell in csv_array:
            cell = str(cell)
            if cell == 'nan':
                x = 0
                y = 0
                points.append([x, y])
            elif ',' in cell:
                str_point = cell.split(',')
                x = float(str_point[0]) / self._width
                y = float(str_point[1]) / self._height
                points.append([x, y])

        points = np.array(points)

        return points.flatten()


if __name__ == "__main__":  # Testing
    # pathes for dirs
    ROOT = r'C:\Users\gabi9\Desktop\Lab\Auto\OKETZ'
    SRC_DIR = ROOT + '/rounds'
    ANNOTATION_DIR = ROOT + '/csv'

    from os import listdir


    def find_csv_filenames(path_to_dir, suffix=".csv"):
        filenames = listdir(path_to_dir)
        return ["/" + filename for filename in filenames if filename.endswith(suffix)]


    filenames = find_csv_filenames(ANNOTATION_DIR)

    # Get generator for each video
    generator = Generator(SRC_DIR, ANNOTATION_DIR, 32)
    generator.set_filename(filenames[0])
    i = generator.get_generator()

    for frame in i:
        print(frame)
