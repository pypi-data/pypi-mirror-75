"""
    Module for TensorFlow Object Detection API model wrapper
"""
import os
from abc import abstractmethod
import numpy as np

from PIL import Image
import tensorflow as tf
from tensorflow.python.tools import optimize_for_inference_lib
from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util
from datetime import datetime

from util.geom_tools import rect_overlap, rect_area
from blyzer.server.model_wrappers.base_wrapper import BaseModelWrapper

class ObjectDetectionModelWrapper(BaseModelWrapper):
    """
        Wrapper for TensorFlow Object Detection API model
    Parameters
    ----------
    BaseModelWrapper : [type]
        [description]
    """
    def __init__(self, model_root, config):
        super().__init__()
        self._config = config
        path = model_root

        self._model_path_detector_graph = os.path.join(path, self._config['detector_graph'])
        self._model_path_detector_label_map = os.path.join(path, self._config['detector_label_map'])
        self._target_classes = self._config["target_classes"]
        self._box_overlap_threshold = self._config.get('box_overlap_threshold', 0.9)
        print("Current directory:", os.getcwd())

        self._label_map = label_map_util.load_labelmap(self._model_path_detector_label_map)
        self._categories = label_map_util.convert_label_map_to_categories(self._label_map, max_num_classes=10,
                                                                          use_display_name=True)
        self.category_index = label_map_util.create_category_index(self._categories)

        print("loading detection model")
        memory_limit = self._config.get('memory_limit', 0.5)
        self._detection_graph = self._load_detector(self._model_path_detector_graph, "object")
        with self._detection_graph.as_default():
            gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=memory_limit)
            self._sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))

    def _load_detector(self, graph_path, tag):
        graph = tf.Graph()

        with graph.as_default():
            od_graph_def = tf.GraphDef()
            print("Loading {} detection graph from {}".format(tag, graph_path))
            with tf.gfile.GFile(graph_path, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

            od_graph_def = optimize_for_inference_lib.optimize_for_inference(
                od_graph_def,
                ['image_tensor'],  # an array of the input node(s)
                ['num_detections', 'detection_boxes', 'detection_scores', 'detection_classes'],
                # an array of output nodes
                tf.int32.as_datatype_enum)

        return graph

    def run_detector(self, graph, sess, image_np):

        ops = graph.get_operations()
        all_tensor_names = {output.name for op in ops for output in op.outputs}
        tensor_dict = {}
        for key in ['num_detections',
                    'detection_boxes',
                    'detection_scores',
                    'detection_classes',
                    'detection_masks']:
            tensor_name = key + ':0'
            if tensor_name in all_tensor_names:
                tensor_dict[key] = graph.get_tensor_by_name(tensor_name)
        if 'detection_masks' in tensor_dict:
            detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
            detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
            real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
            detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
            detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
            detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(detection_masks, detection_boxes,
                                                                                  image_np.shape[0], image_np.shape[1])
            detection_masks_reframed = tf.cast(tf.greater(detection_masks_reframed, 0.5), tf.uint8)
            tensor_dict['detection_masks'] = tf.expand_dims(detection_masks_reframed, 0)

        image_tensor = graph.get_tensor_by_name('image_tensor:0')
        # Запуск поиска объектов на изображении
        output_dict = sess.run(tensor_dict, feed_dict={image_tensor: np.expand_dims(image_np, 0)})

        # Преобразуем выходные тензоры типа float32 в нужный формат
        output_dict['num_detections'] = int(output_dict['num_detections'][0])
        output_dict['detection_classes'] = output_dict['detection_classes'][0].astype(np.uint8)
        output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
        output_dict['detection_scores'] = output_dict['detection_scores'][0]
        if 'detection_masks' in output_dict:
            output_dict['detection_masks'] = output_dict['detection_masks'][0]

        return output_dict

    def _full_image_process(self, image_np):
        # Используем модель (граф TensorFlow), которую ранее загрузили в память
        # with self._detection_graph.as_default():
        # Все операции в TensorFlow выполняются в сессии
        # Готовим операции и входные данные
        # print("image shape:", image_np.shape)
        # if self._convert_to_grayscale and image_np.shape[2] > 1:
        #     image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
        #     print("image shape after conversion:", image_np.shape)
        #     image_np = image_np.reshape(image_np.shape[0], image_np.shape[1], 1)
        #     print("image shape after second conversion:", image_np.shape)
        #     # image_np = cv2.cvtColor(image_np, cv2.COLOR_GRAY2BGR)
        #     # print("image shape after third conversion:", image_np.shape)

        output_dict = self.run_detector(self._detection_graph, self._sess, image_np)

        result = []
        for i in range(output_dict['num_detections']):
            if (output_dict['detection_classes'][i] in self._target_classes
                    and output_dict['detection_scores'][i] > 0.5):

                children = None
                # cropped_img = self._crop_image(image_np, output_dict['detection_boxes'][:][i])

                result.append((output_dict['detection_boxes'][:][i],
                               output_dict['detection_scores'][i],
                               output_dict['detection_classes'][i],
                               children))

        result = self._remove_overlapping_boxes(result)
        return result

    # TODO what is bourder parameter
    def _crop_image(self, image_np, bourder):
        y1 = int(image_np.shape[0] * bourder[0])
        x1 = int(image_np.shape[1] * bourder[1])
        y2 = int(image_np.shape[0] * bourder[2])
        x2 = int(image_np.shape[1] * bourder[3])

        return np.copy(image_np[y1:y2, x1:x2])

    def _remove_overlapping_boxes(self, report):
        remove = set()
        for i in range(len(report)):
            for j in range(i + 1, len(report)):
                box_i = report[i][0]
                box_j = report[j][0]
                area_i = rect_area(box_i)
                area_j = rect_area(box_j)
                common_area = rect_overlap(box_i, box_j)
                if report[i][2] != report[j][2] and (
                        common_area / area_i > self._box_overlap_threshold or
                        common_area / area_j > self._box_overlap_threshold):
                    # Too much overlap between boxes
                    # Remove the box with the smaller detection rate
                    # If detection rates identical, remove the smaller box
                    # If the area is also identical, we leave both boxes
                    if report[i][1] < report[j][1]:
                        remove.add(i)
                    elif report[j][1] < report[i][1]:
                        remove.add(j)
                    elif area_i < area_j:
                        remove.add(i)
                    elif area_j < area_i:
                        remove.add(j)

        return [r for i, r in enumerate(report) if i not in remove]

    @abstractmethod
    def predict(self, data: np.array) -> dict:
        """ Make model predict on Image

        Parameters
        ----------
        data : np.array
            Image or batch of images
        Returns
        -------
        dict
            Models' predict
        """
        return self._full_image_process(data)
