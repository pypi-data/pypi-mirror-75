PORTABLE=False
import os
import sys
import pdb
import json
import shutil
from zipfile import ZipFile, ZIP_DEFLATED
import argparse
from pprint import pprint
import xml.etree.ElementTree as etree
if not PORTABLE:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) # to import util
from util.geom_tools import rect_overlap, rect_area

class Action:
    def xml(self, path, doc):
        pass

    def image(self, path):
        pass

    def summarize(self):
        pass

class FileRemover(Action):
    def __init__(self):
        self.failed = []
        self.removed_annotations = 0
        self.removed_images = 0

    def remove(self, path):
        try:
            os.remove(path)
            print("- removed {}".format(path))
        except:
            self.failed.append(path)
            print("- failed to remove {}".format(path))

    def xml(self, path, _):
        self.remove(path)
        self.removed_annotations += 1

    def image(self, path):
        self.remove(path)
        self.removed_images += 1

    def summarize(self):
        if self.removed_annotations > 0 or self.removed_images > 0:
            print("Removed {} annotations and {} images".format(self.removed_annotations, self.removed_images))

        if len(self.failed) > 0:
            print("Failed to remove {} files".format(len(self.failed)))

class FileLister(Action):
    def xml(self, path, _):
        print(os.path.basename(path))

class FileCounter(Action):
    def __init__(self):
        self.value = 0

    def xml(self, path, _):
        self.value += 1

    def summarize(self):
        print("Count:", self.value)

class ClassReplacer(Action):
    def __init__(self, target, replacement):
        self.target = target
        self.replacement = replacement

    def xml(self, path, doc):
        modified = False

        for obj in doc.iter('object'):
            name = obj.find('name')
            if name is not None and name.text == self.target:
                name.text = self.replacement
                modified = True

        if modified:
            with open(path, 'wb') as f:
                f.write(etree.tostring(doc, encoding='utf-8'))
                print("Wrote changes to {}".format(path))

class ClassCollector(Action):
    def __init__(self):
        self.classes = set()

    def xml(self, path, doc):
        modified = False

        for obj in doc.iter('object'):
            self.classes.add(get_prop(obj, 'name'))

    def summarize(self):
        # print("Found {} distinct classes".format(len(self.classes)))
        for label in sorted(self.classes):
            print(label)

class FileMover(Action):
    def __init__(self, target_dir, remove_original = False):
        self.target_dir = target_dir
        self.target_dir_annotations = os.path.join(target_dir, "annotations")
        self.dir_created = set()
        self.removed_annotations = 0
        self.removed_images = 0
        self.remove_original = remove_original
        self.file_op = shutil.move if remove_original else shutil.copy

    def ensure_dir(self, target_dir):
        if target_dir not in self.dir_created:
            os.makedirs(target_dir, exist_ok=True)
            self.dir_created.add(target_dir)

    def xml(self, path, _):
        self.ensure_dir(self.target_dir_annotations)
        if os.path.exists(path):
            self.file_op(path, self.target_dir_annotations)
            self.removed_annotations += 1

    def image(self, path):
        self.ensure_dir(self.target_dir)
        if os.path.exists(path):
            self.file_op(path, self.target_dir)
            self.removed_images += 1

    def summarize(self):
        verb = "Moved" if self.remove_original else "Copied"
        print("{} {} annotations and {} images".format(verb, self.removed_annotations, self.removed_images))

class FilePacker(Action):
    def __init__(self, output_file, image_dir, prefix):
        assert output_file is not None and len(output_file) > 0
        self.output_file = output_file
        self.len_image_dir = len(image_dir)
        self.prefix = prefix
        self.file_list = []

    @staticmethod
    def short_name(path, chop_off):
        return path[chop_off:].lstrip(os.path.sep)

    def xml(self, path, _):
        self.file_list.append(os.path.normpath(path))

    def image(self, path):
        self.file_list.append(os.path.normpath(path))

    def summarize(self):
        print("Collected {} files".format(len(self.file_list)))
        output = ZipFile(self.output_file, 'w', compression=ZIP_DEFLATED)
        for path in self.file_list:
            short_name = self.short_name(path, self.len_image_dir)
            short_name = os.path.join(self.prefix, short_name)
            output.write(path, short_name)
            print("Adding {}".format(short_name))

class BoxReplacer(Action):
    def __init__(self, boxes):
        self.boxes = boxes
        self.num_patched = 0
        self.ambiguous = []

    @staticmethod
    def get_box_size(obj):
        box = obj.find('bndbox')
        ymin = int(get_prop(box, 'ymin'))
        xmin = int(get_prop(box, 'xmin'))
        ymax = int(get_prop(box, 'ymax'))
        xmax = int(get_prop(box, 'xmax'))
        return abs(xmax - xmin), abs(ymax - ymin)

    def xml(self, path, doc):
        image_name = os.path.splitext(os.path.basename(path))[0]
        new_boxes = self.boxes.get(image_name)
        if new_boxes is None: return

        modified = False
        objects = list(doc.iter('object'))
        size_dict, size_count = {}, {}

        for obj in objects:
            size = self.get_box_size(obj)
            size_dict[size] = obj
            size_count[size] = size_count.get(size, 0) + 1

        for box in new_boxes:
            size = (box['width'], box['height'])
            target = size_dict.get(size)
            count = size_count.get(size, 0)
            if count == 1:
                name = obj.find('name')
                name.text = box['label']
                self.num_patched += 1
                modified = True
            elif count > 1:
                self.ambiguous.append(path)

        if modified:
            with open(path, 'wb') as f:
                f.write(etree.tostring(doc, encoding='utf-8'))
                print("Wrote changes to {}".format(path))

    def summarize(self):
        print("Patched {} files".format(self.num_patched))
        if len(self.ambiguous) > 0:
            print("The following files were not patched due to containing bounding boxes of equal sizes:")
            for item in self.ambiguous:
                print(item)

def get_prop(elem, key, default=None):
    prop = elem.find(key)
    return default if prop is None else prop.text

def object_to_rect(obj):
    box = obj.find('bndbox')
    return int(get_prop(box, 'ymin')), int(get_prop(box, 'xmin')), int(get_prop(box, 'ymax')), int(get_prop(box, 'xmax'))

def count_overlapping_boxes(doc, threshold):
    count = 0
    objects = list(doc.iter('object'))
    for i in range(len(objects)):
        for j in range(i + 1, len(objects)):
            box_i = object_to_rect(objects[i])
            box_j = object_to_rect(objects[j])
            area_i = rect_area(box_i)
            area_j = rect_area(box_j)
            common_area = rect_overlap(box_i, box_j)
            if common_area / area_i > threshold or common_area / area_j > threshold:
                count += 1
    return count

def collect_buckets(items, get_key):
    buckets = {}
    for item in items:
        key = get_key(item)
        bucket = buckets.get(key)
        if not bucket:
            buckets[key] = bucket = []
        bucket.append(item)
    return buckets

def predicate_all(doc, config, input_dir, annotation_dir):
    return True

def predicate_verified(doc, config, input_dir, annotation_dir):
    return doc.get('verified') == 'yes'

def predicate_empty(doc, config, input_dir, annotation_dir):
    return sum(1 for elem in doc.iter('object')) == 0

def predicate_num_objects_above(doc, config, input_dir, annotation_dir):
    return sum(1 for elem in doc.iter('object')) > config.threshold

def predicate_has_class(doc, config, input_dir, annotation_dir):
    return sum(1 for elem in doc.iter('object') if get_prop(elem, 'name') == config.target_class) > 0

def predicate_orphaned(doc, config, input_dir, annotation_dir):
    return not os.path.exists(os.path.join(input_dir, get_prop(doc, 'filename')))

def predicate_has_overlap(doc, config, input_dir, annotation_dir):
    return count_overlapping_boxes(doc, config.threshold) > 0

def predicate_id_matches(doc, config, input_dir, annotation_dir):
    return os.path.splitext(os.path.basename(get_prop(doc, 'filename')))[0].strip() in config.param_list

def predicate_orphaned_image(path, config, input_dir, annotation_dir):
    filename = os.path.basename(os.path.splitext(path)[0]) + ".xml"
    return not os.path.exists(os.path.join(annotation_dir, filename))

def get_predicate(target):
    return get_predicate.table[target]

get_predicate.table = {
    'all': predicate_all,
    'verified': predicate_verified,
    'empty': predicate_empty,
    'num-objects-above': predicate_num_objects_above,
    'has-class': predicate_has_class,
    'orphaned': predicate_orphaned,
    'orphaned-images': predicate_orphaned_image,
    'has-overlap': predicate_has_overlap,
    'id-matches': predicate_id_matches
}

def iterate_xml(input_dir, annotation_dir, config, action, match):
    for filename in os.listdir(annotation_dir):
        if not filename.endswith(".xml"): continue
        xml_path = os.path.join(annotation_dir, filename)
        with open(xml_path, 'r', encoding='utf-8') as file:
            try:
                xml = etree.fromstring(file.read())
            except Exception as ex:
                print(xml_path)
                continue
        if match(xml, config, input_dir, annotation_dir):
            if action.__class__.image != Action.image: # the action has a non-empty callback for images
                for image_filename in xml.iter('filename'):
                    image_path = os.path.join(input_dir, image_filename.text)
                    action.image(image_path)
            action.xml(xml_path, xml)

def iterate_images(input_dir, annotation_dir, config, action, match):
    for filename in os.listdir(input_dir):
        if not filename.lower().endswith(".jpg"): continue
        image_path = os.path.join(input_dir, filename)
        if match(image_path, config, input_dir, annotation_dir):
            # action.xml(image_path, None) # FIXME: this is needed for standard actions such as list, count, ... to work
            action.image(image_path)

def load_config(portable):
    if portable:
        from types import SimpleNamespace

        class MyNamespace(SimpleNamespace):
            def update(self, value_dict):
                self.__dict__.update(value_dict)

        return MyNamespace(
            frame_dump_dir = "data/client-saved-frames",
            json_annotation_dir = "{frame_dump_dir}/annotations-json",
            xml_annotation_dir = "{frame_dump_dir}/annotations",
            annotation_format = "pascal-voc",
            video_extension = "mp4"
        )
    else:
        from server.server import load_config
        from client.config import ClientConfig
        return load_config(ClientConfig, "client/config.json")

def main():
    parser = argparse.ArgumentParser(description='Labeled data cleanup/modification tool')

    parser.add_argument('action', help="Action to take (default: %(default)s)", default='remove',
        choices=['remove', 'count', 'list', 'list-classes', 'replace-class', 'move', 'copy', 'pack', 'patch-box-labels'])

    targets = ['verified', 'empty', 'all', 'has-class', 'num-objects-above', 'orphaned', 'orphaned-images', 'has-overlap', 'id-matches']
    parser.add_argument('target', help="Which files will be [re]moved (default: %(default)s)", default='unverified',
        choices=targets + ['!' + elem for elem in targets])

    parser.add_argument('input_dir', help="Directory with the data to be cleaned (default: as specified in client config)", nargs='?', default=argparse.SUPPRESS)
    parser.add_argument('--replace-what', help="The class to replace")
    parser.add_argument('--replace-with', help="The new class")
    parser.add_argument('--target-class', help="Target class argument for actions that require one")
    parser.add_argument('--target-dir', help="The directory where files will be placed")
    parser.add_argument('--threshold', type=float, help="Threshold argument for actions that require one")
    parser.add_argument('--output-file', help="The location of the output file for actions that produce one")
    parser.add_argument('--param-file', help="The location of a data file with additional parameters for actions that make use of one")
    parser.add_argument('--param-list', help="List of additional parameters for actions that make use of one", nargs='?')
    args = vars(parser.parse_args())

    config = load_config(PORTABLE)
    config.input_dir = os.path.normpath(config.frame_dump_dir)
    config.update(args)
    config.annotation_dir = os.path.normpath(config.xml_annotation_dir.replace('{frame_dump_dir}', config.input_dir))

    if config.param_file:
        with open(config.param_file) as file:
            config.param_list = json.load(file)
            assert isinstance(config.param_list, list)
    elif config.param_list:
        config.param_list = json.loads(config.param_list.replace("'", '"'))
        assert isinstance(config.param_list, list)

    # pprint(config)

    if config.action == 'remove':
        action = FileRemover()
    elif config.action == 'move':
        action = FileMover(config.target_dir, remove_original=True)
    elif config.action == 'copy':
        action = FileMover(config.target_dir, remove_original=False)
    elif config.action == 'pack':
        action = FilePacker(config.output_file, config.input_dir, os.path.basename(os.path.normpath(config.frame_dump_dir)))
    elif config.action == 'count':
        action = FileCounter()
    elif config.action == 'list':
        action = FileLister()
    elif config.action == 'replace-class':
        action = ClassReplacer(config.replace_what, config.replace_with)
    elif config.action == 'list-classes':
        action = ClassCollector()
    elif config.action == 'patch-box-labels':
        action = BoxReplacer(collect_buckets(config.param_list, lambda item: item['image']))

    if config.target.startswith('!'):
        pos_pred = get_predicate(config.target[1:])
        predicate = lambda doc, config, input_dir, annotation_dir: not pos_pred(doc, config, input_dir, annotation_dir)
    else:
        predicate = get_predicate(config.target)

    if config.target in {'orphaned-images'}:
        process = iterate_images
    else:
        process = iterate_xml

    process(config.input_dir, config.annotation_dir, config, action, predicate)
    action.summarize()

if __name__ == "__main__":
    main()