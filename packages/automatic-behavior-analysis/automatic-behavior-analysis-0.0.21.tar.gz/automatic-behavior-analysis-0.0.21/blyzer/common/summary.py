import numpy as np
from scipy.ndimage import filters
import pdb

def get_object_name(object_names, index):
    name = object_names.get(index)
    return name if name else "Id {}".format(index + 1)

def title_case(word):
    return word[0].upper() + word[1:] if len(word) > 0 else word

def summarize_video_annotation(annotation, options):
    num_dogs = 0
    statistics = []
    max_targets = options.get('max_detection_targets', 2)
    object_names = options.get('object_names') or {}

    # for index in sorted(self._response_cache.keys()):
        # response = self.get_cached_item(index)
    for index, response in annotation.frame_annotations():
        statistics.append([0] * max_targets)
        items = response['dogs'][:max_targets]
        num_dogs = max(num_dogs, len(items))
        for item in items:
            try:
                statistics[-1][item['id']] = 1 if item['state'] == 'sleep' else -1
            except Exception as ex:
                # pdb.set_trace()
                pass

    dogs_state = np.asarray(statistics)
    if len(dogs_state) <= 0: return
    # print('dogs_state:', os.linesep, dogs_state)

    def make_item(label, value, **kwargs):
        entry = { 'label': label, 'value': value }
        if kwargs: entry.update(kwargs)
        return entry

    def add_dict_item(container, key, label, value, **kwargs):
        container[key] = make_item(label, value, **kwargs)

    def add_list_item(container, label, value, **kwargs):
        container.append(make_item(label, value, **kwargs))

    result = {}
    total_frames = len(statistics)
    add_dict_item(result, 'num_frames_total', "Total frames", total_frames)

    frames_w_dogs = np.sum(np.abs(dogs_state[:, 0]))
    per_w_dog = frames_w_dogs / total_frames
    add_dict_item(result, 'num_frames_with_dogs', "Frames with one or more dogs", frames_w_dogs, ratio=per_w_dog)
    # add_dict_item(result, 'ratio_frames_with_dogs', "Percentage of frames with one or more dogs", per_w_dog)

    dog_statistics = []

    def collect_block_lengths(data, target):
        prev = None
        result = []
        block_start = 0
        block_open = False

        for index, elem in enumerate(data):
            if elem == target and elem != prev:
                block_start = index
                block_open = True
            elif elem != target and prev == target:
                result.append(index - block_start)
                block_open = False
            prev = elem

        if block_open:
            result.append(len(data) - block_start)

        return result

    for i in range(num_dogs):
        dog_statistic = {}
        dog_i_state = dogs_state[:, i]
        # print("dog_i_state[{}]: {}".format(i, dog_i_state))
        if total_frames > 100:
            dog_i_state = filters.median_filter(dog_i_state, size=30)
            # print("dog_i_state[{}] after filter: {}".format(i, dog_i_state))

        dog_i_name = get_object_name(object_names, i)
        add_dict_item(dog_statistic, 'dog_name', "Dog name", dog_i_name, hidden=True)
        frames_w_dog_i = np.sum(np.abs(dog_i_state))
        per_w_dog = frames_w_dog_i / total_frames
        add_dict_item(dog_statistic, 'num_frames_with_dog', "Frames with {}".format(dog_i_name), frames_w_dog_i, ratio=per_w_dog)
        # add_dict_item(dog_statistic, 'ratio_frames_with_dog', "Percentage of frames with {}".format(dog_i_name), per_w_dog)

        frames_w_dog_i_sleep = np.sum(np.equal(dog_i_state, np.ones(dog_i_state.shape)))
        per_w_dog_i_sleep = frames_w_dog_i_sleep / total_frames
        add_dict_item(dog_statistic, 'num_frames_with_dog_asleep', "Frames with {} asleep".format(dog_i_name), frames_w_dog_i_sleep, ratio=per_w_dog_i_sleep)

        add_dict_item(dog_statistic,
            'sleep_amount',
            "Amount of time {} spent sleeping".format(dog_i_name),
            frames_w_dog_i_sleep / options.video_fps, unit='sec')

        # Count sleep bouts
        dog_i_sleep_blocks = collect_block_lengths(dog_i_state, 1)
        add_dict_item(dog_statistic, 'num_sleep_bouts', "Number of sleeping bouts for {}".format(dog_i_name), len(dog_i_sleep_blocks))

        dog_i_frames_per_block = np.mean(dog_i_sleep_blocks) if len(dog_i_sleep_blocks) > 0 else 0

        add_dict_item(dog_statistic,
            'num_frames_per_sleep_bout',
            "Average frames per sleeping bout for {}".format(dog_i_name),
            dog_i_frames_per_block)

        add_dict_item(dog_statistic,
            'time_units_per_sleep_bout',
            "Average length of sleeping bout for {}".format(dog_i_name),
            dog_i_frames_per_block / options.video_fps, unit='sec')

        add_list_item(dog_statistics, "{}".format(title_case(dog_i_name)), dog_statistic)

    add_dict_item(result, 'dog_statistics', 'Dog statistics', dog_statistics)
    return result