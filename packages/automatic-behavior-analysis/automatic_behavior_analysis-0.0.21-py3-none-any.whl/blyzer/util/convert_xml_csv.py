import xml.etree.ElementTree as ET
import csv
import argparse
import sys

"""
to convert xml to csv format pass the path of the 
xml file and run.
"""



def data_to_csv(list, name):
    with open(name.replace('.xml', '.csv'), 'w', newline='', encoding='utf_8_sig') as file_test:
        writer = csv.writer(file_test)
        writer.writerows(list)
        file_test.close()


def separate_to_groups(root):
    dog_groups = {}
    for track in root.findall("track"):
        if track.attrib['group_id'] in dog_groups:
            dog_groups.get(track.attrib['group_id']).append(track)
        else:
            dog_groups[track.attrib['group_id']] = [track]

    return dog_groups


def label_columns(dog_groups):
    labels = ["H1", "H2", "H3", "EL1", "EL2", "ER1", "ER2", "FR1", "FR2", "FL1", "FL2", "T1", "T2", "T3", "BR1", "BR2",
              "BR3", "BL1", "BL2", "BL3", "Dog_TL","Dog_BR"]
    data_f = [["frame"]]

    dog_labels = []
    for key in dog_groups.keys():
        for lb in labels:
            dog_labels.append(key + "_" + lb)

    data_f[0] = data_f[0] + dog_labels
    return data_f


def create_data_matrix(position_key, dog_groups, data_f, frames_num):
    data = [[None] * len(data_f[0]) for x in range(frames_num)]

    # translating the xml to csv
    for group_key in dog_groups:
        for track in dog_groups.get(group_key):
            if track.attrib["label"] == "Dog":
                label1 = group_key + "_" + track.attrib["label"] + "_TL"
                label2 = group_key + "_" + track.attrib["label"] + "_BR"
                for box in track:
                    data[int(box.attrib["frame"])][position_key.get("frame")] = box.attrib["frame"]
                    data[int(box.attrib["frame"])][position_key.get(label1)] = box.attrib["xtl"] + "," + box.attrib["ytl"]
                    data[int(box.attrib["frame"])][position_key.get(label2)] = box.attrib["xbr"] + "," + box.attrib["ybr"]

            else:
                label = group_key + "_" + track.attrib["label"]
                for box in track:
                    data[int(box.attrib["frame"])][position_key.get("frame")] = box.attrib["frame"]
                    data[int(box.attrib["frame"])][position_key.get(label)] = box.attrib["xtl"] + "," + box.attrib["ytl"]
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-path", type=str, help="contain full path to xml file")
    args = parser.parse_args()

    if args.path is None:
        print("no path given")
        sys.exit(-1)
    run(args.path)


def run(p):
    dom = ET.parse(p)
    root = dom.getroot()
    frames_num = int(root.find("meta").find("task").find("size").text)

    # separate to 3 groups
    dog_groups = separate_to_groups(root)

    # create label for columns in csv
    data_f = label_columns(dog_groups)
    position_key = {}

    for index, label in enumerate(data_f[0]):
        position_key[label] = index

    data = create_data_matrix(position_key, dog_groups, data_f, frames_num)
    data_to_csv(data_f + data, p)
    print("converted")


if __name__ == "__main__":
    main()
