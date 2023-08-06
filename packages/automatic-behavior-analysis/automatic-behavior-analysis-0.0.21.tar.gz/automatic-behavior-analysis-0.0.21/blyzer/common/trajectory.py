import numpy as np

class Trajectory:
    def __init__(self, max_hole_size = 25):
        self._max_hole_size = max_hole_size
        self._trajectory = []
        self._last_detected_index = -1


    def get_trajectory_points(self):
        return self._trajectory.copy()

    def get_trajectory_np(self):
        return np.array(self.get_trajectory_points())

    def get_point(self, index):
        try:
            return self._trajectory[index] 
        except IndexError:
            return (np.NaN, np.NaN)

    def len(self):
        return len(self._trajectory)

    def add_point(self, index, coordinates):
        x, y = coordinates
        if index < len(self._trajectory):
            return

        while index > len(self._trajectory):
            self._trajectory.append((np.NaN, np.NaN))

        self._save_point(index, x, y)
        if self._last_detected_index == -1:
            self._last_detected_index = index
        if ((self._last_detected_index != index - 1)
                and (self._last_detected_index != index)
                and (index - self._last_detected_index < self._max_hole_size)):
            self._interpolate_between(self._last_detected_index, index)

            self._last_detected_index = index

    def _save_point(self, i, x, y):
        x = int(x)
        y = int(y)
        if i == len(self._trajectory):
            self._trajectory.append((x, y))
        else:
            self._trajectory[i] = (x, y)

    def _interpolate_between(self, index_1, index_2, method='linear'):
        # Make method unsensible to index sequence
        if index_2 < index_1:
            index_1, index_2 = index_2, index_1
        if index_1 == index_2:
            return

        try:
            y_start, x_start = self._trajectory[index_1]
        except TypeError:
            y_start, x_start = self._trajectory[index_2]
        y_end, x_end = self._trajectory[index_2]
        length = index_2 - index_1

        x = np.linspace(x_start, x_end, length, endpoint=False)
        y = np.linspace(y_start, y_end, length, endpoint=False)

        for i, x_i, y_i in zip(range(index_1, index_2), x, y):
            self._save_point(i, y_i, x_i)
