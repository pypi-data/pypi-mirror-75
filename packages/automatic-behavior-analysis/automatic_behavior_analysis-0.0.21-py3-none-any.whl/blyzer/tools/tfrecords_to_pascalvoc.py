import os
import sys
import cv2
import tensorflow as tf
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # to import util
from server.server import ModelConfig, load_config
from client.config import ClientConfig
from tools.labelImg.libs.pascal_voc_io import PascalVocWriter
import argparse

FEATURES = {
    'image/height': tf.FixedLenFeature((), tf.int64, default_value=0),
    'image/width': tf.FixedLenFeature((), tf.int64, default_value=0),
    'image/filename': tf.FixedLenFeature((), tf.string, default_value=""),
    'image/source_id': tf.FixedLenFeature((), tf.string, default_value=""),
    'image/key/sha256': tf.FixedLenFeature((), tf.string, default_value=""),
    'image/encoded': tf.FixedLenFeature((), tf.string, default_value=""),
    'image/format': tf.FixedLenFeature((), tf.string, default_value=""),
    'image/object/bbox/xmin': tf.VarLenFeature(dtype=tf.float32),
    'image/object/bbox/xmax': tf.VarLenFeature(dtype=tf.float32),
    'image/object/bbox/ymin': tf.VarLenFeature(dtype=tf.float32),
    'image/object/bbox/ymax': tf.VarLenFeature(dtype=tf.float32),
    'image/object/class/text': tf.VarLenFeature(dtype=tf.string),
    'image/object/class/label': tf.VarLenFeature(dtype=tf.int64),
    # 'image/object/difficult': tf.VarLenFeature(dtype=tf.int64)
}

def read_loop(sess, next_object, callback, max_iterations=float("inf")):
    index = 0
    while index < max_iterations:
        try:
            callback(sess.run(next_object))
            index += 1
        except tf.errors.OutOfRangeError:
            return

def decode_feature(feature, value):
    if isinstance(feature, tf.VarLenFeature):
        default_value = "" if feature.dtype == tf.string else 0
        return tf.sparse_tensor_to_dense(value, default_value=default_value)
    return value

def _parse_function(example_proto):
    parsed = tf.parse_single_example(example_proto, FEATURES)
    return { k: decode_feature(v, parsed[k]) for k, v in FEATURES.items() }

class Counter:
    def __init__(self):
        self.value = 0

    def __call__(self, _):
        self.value += 1

class Application:
    def savePascalVocFormat(self, filename, response, imagePath, imageShape):
        imgFolderPath = os.path.dirname(imagePath)
        imgFolderName = os.path.split(imgFolderPath)[-1]
        imgFileName = os.path.basename(imagePath)
        writer = PascalVocWriter(imgFolderName, imgFileName, imageShape, localImgPath=imagePath)

        for item in response['dogs']:
            # difficult = int(shape['difficult'])
            label = 'dog-sleep' if item['state'] == 'sleep' else 'dog'

            x1 = int(round(item['x1'] * imageShape[1]))
            x2 = int(round(item['x2'] * imageShape[1]))
            xmin = min(x1, x2)
            xmax = max(x1, x2)

            y1 = int(round(item['y1'] * imageShape[0]))
            y2 = int(round(item['y2'] * imageShape[0]))
            ymin = min(y1, y2)
            ymax = max(y1, y2)

            # print("box:", [xmin, ymin, xmax, ymax])

            writer.addBndBox(xmin, ymin, xmax, ymax, label, difficult=0, rate=item.get('rate'))

        writer.save(targetFile=filename)

    def process_entry(self, entry):
        filename = os.path.basename(entry['image/filename'].decode('utf-8'))
        image_string = entry['image/encoded']
        image_shape = (entry['image/height'], entry['image/width'], 3)
        image_path = os.path.join(self.image_dir, filename)
        annotation_path = os.path.join(self.annotation_dir, os.path.splitext(filename)[0] + ".xml")
        image_path = os.path.abspath(image_path)
        annotation_path = os.path.abspath(annotation_path)
        print("image_path:", image_path)
        print("annotation_path:", annotation_path)
        items = []
        l_xmin = entry['image/object/bbox/xmin']
        l_xmax = entry['image/object/bbox/xmax']
        l_ymin = entry['image/object/bbox/ymin']
        l_ymax = entry['image/object/bbox/ymax']
        l_label = entry['image/object/class/text']

        items = []
        for xmin, xmax, ymin, ymax, label in zip(l_xmin, l_xmax, l_ymin, l_ymax, l_label):
            label = label.decode('utf-8')
            state = 'sleep' if 'sleep' in label else 'awake'
            item = { 'x1': xmin, 'y1': ymin, 'x2': xmax, 'y2': ymax, 'state': state }
            print(item)
            items.append(item)

        response = { 'dogs': items }
        with open(image_path, 'wb') as f:
            f.write(image_string)
        self.savePascalVocFormat(annotation_path, response, image_path, image_shape)

    def print_entry(self, entry):
        filename = os.path.basename(entry['image/filename'].decode('utf-8'))
        classes = zip(entry['image/object/class/label'], entry['image/object/class/text'])
        print("image: {}, width: {}, height: {}, objects: {}".format(
            filename,
            entry['image/width'],
            entry['image/height'],
            ["{}:{}".format(label, text.decode('utf-8')) for label, text in classes]))

    def main(self):
        parser = argparse.ArgumentParser(description='TFRecord export tool')
        parser.add_argument('input_file', help="Input file")
        parser.add_argument('--output-path', help="Directory where the extracted data will be placed")
        parser.add_argument('--action', help="Action to take (default: %(default)s)", default='extract', choices=['extract', 'count', 'list'])
        args = vars(parser.parse_args())

        if args['action'] == 'extract':
            if args.get('output_path') is None:
                print("{}: error: the following arguments are required: --output-dir".format(os.path.basename(sys.argv[0])))
                return

            self.image_dir = args['output_path']
            self.annotation_dir = os.path.join(self.image_dir, "annotations")
            os.makedirs(self.image_dir, exist_ok=True)
            os.makedirs(self.annotation_dir, exist_ok=True)
            action = self.process_entry
            def summarize(): pass
        elif args['action'] == 'list':
            action = self.print_entry
            def summarize(): pass
        else:
            action = Counter()
            def summarize(): print("Count:", action.value)

        with tf.Session() as sess:
            dataset = tf.data.TFRecordDataset([args['input_file']])
            dataset = dataset.map(_parse_function)
            iterator = dataset.make_one_shot_iterator()
            next_object = iterator.get_next()
            read_loop(sess, next_object, action)

        summarize()

if __name__ == "__main__":
    Application().main()