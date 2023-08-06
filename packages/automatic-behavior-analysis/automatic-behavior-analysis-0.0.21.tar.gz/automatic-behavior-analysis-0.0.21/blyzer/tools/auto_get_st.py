import argparse
import os
import sys
from matplotlib import pyplot as plt
from get_st import main as get_st
import xlwings as xw
import pandas as pd

from numpy import double


def main():
    """
    this file runs get_st and updates the xlsx.
    from the .xlsx file we get the results of the average time and bout diff for each threshold.
    at the end we present a graph that shows the result for each threshold tried
    """
    parser = argparse.ArgumentParser(description="Statistic analysis")
    parser.add_argument('-threshold', help="threshold used for this process", type=double)
    parser.add_argument('-dir', help="dir path", type=str)
    args = vars(parser.parse_args())

    if 1 > args['-threshold'] > 0:
        threshold = args['moving_threshold']
    else:
        print("threshold must be between 1 and 0")
        sys.exit(-1)

    if args['-dir'] is None:
        print("no path given")
        sys.exit(-1)

    PATH = args['-dir']
    dog_name = "Atila"
    delta = 0.0002

    wb = xw.Book('report.xlsx')
    ws = wb.sheets[0]

    # get paths of month dir
    dirs = []
    for path in os.listdir(PATH):
        dirs.append(os.path.join(PATH, path))

    time_diff_y = []
    bout_diff_y = []
    threshold_x = []

    # using get_st on every day in month
    if len(dirs) > 1:
        for i in range(25):
            for dire in dirs:
                for path in os.listdir(dire):
                    get_st(threshold, dog_name, os.path.join(dire, path))

            # collecting data for the graph
            average_time_diff = ws.cells(14, 8).value
            average_bout_diff = ws.cells(14, 11).value

            time_diff_y.append(average_time_diff * 100 - 3)
            bout_diff_y.append(average_bout_diff)
            threshold_x.append(threshold)

            threshold = threshold + delta
    else:
        print("no month dirs")

    data = pd.DataFrame({'threshold_x': threshold_x, 'time_diff_y': time_diff_y, 'bout_diff_y': bout_diff_y},
                        columns=['threshold_x', 'time_diff_y', 'bout_diff_y'])
    data.to_csv('stats.csv')

    plt.plot(threshold_x, bout_diff_y, 'bo')
    plt.plot(threshold_x, time_diff_y, 'go')
    plt.legend(["bout diff", "time diff"])
    plt.show()


if __name__ == '__main__':
    main()
