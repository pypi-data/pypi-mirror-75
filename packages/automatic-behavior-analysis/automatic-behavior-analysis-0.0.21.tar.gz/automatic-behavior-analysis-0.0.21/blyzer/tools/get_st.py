#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Скрипт сводит файлы со статистикой следующего формата: Bob_01_20180118110000.csv
	DateTime	y1	y2	x1	x2	state	rate
0	2018-01-18 11:00:00.000	0.05515958368778229	0.3669011890888214	0.45685988664627075	0.7031605839729309	sleep	0.999748170375824
1	2018-01-18 11:00:00.100	0.05515958368778229	0.3669011890888214	0.45685988664627075	0.7031605839729309	sleep	0.999748170375824
2	2018-01-18 11:00:00.200	0.05515958368778229	0.3669011890888214	0.45685988664627075	0.7031605839729309	sleep	0.999748170375824
3	2018-01-18 11:00:00.300	0.05515958368778229	0.3669011890888214	0.45685988664627075	0.7031605839729309	sleep	0.999748170375824
4	2018-01-18 11:00:00.400	0.05515958368778229	0.3669011890888214	0.4568598866462708	0.7031605839729309	awake	0.999748170375824
5	2018-01-18 11:00:00.500	0.05515958368778229	0.3669011890888214	0.45685988664627086	0.7031605839729309	awake	0.999748170375824
...

в файл со статистикой следующего формата: st_Bob.csv
   state               start time                 end time                interval
0  sleep  2018-01-18 11:00:00.000  2018-01-18 11:00:00.400  0 days 00:00:00.400000
1  awake  2018-01-18 11:00:00.400  2018-01-18 11:00:00.600  0 days 00:00:00.200000
2  sleep  2018-01-18 11:00:00.600  2018-01-18 11:00:01.000  0 days 00:00:00.400000
3  awake  2018-01-18 11:00:01.000  2018-01-18 11:00:11.100  0 days 00:00:10.100000
...

для корректной работы необходимо поместить скрипт в папку с файлами dog_name*.csv,
при запуске передать в командной строке имя собаки (пример: python3 ./get_st.py Bob)
'''

import pandas as pd
import xlwings as xw
import glob
import sys
import os

from tqdm import tqdm
from datetime import timedelta


def main(threshold, dog_name, dirc_path):
    # best results till 21/8/19 got with this threshold 0.2
    if 1 > threshold > 0:
        moving_threshold = threshold
    else:
        print("threshold need to between 0 and 1")
        sys.exit(-1)

    if len(dog_name) > 0:
        name = dog_name
    else:
        print("for correct work enter: python3 ./get_st.py dog_name")
        sys.exit(-1)

    dir_path = ""
    if dirc_path is not None:
        dir_path = dirc_path
    all_files = glob.glob(os.path.join(dir_path, name) + "*.csv")
    if len(all_files) == 0:
        print("csv file not found")
        sys.exit(1)

    output_statistic = pd.DataFrame(columns=['state', 'start time', 'end time', 'interval'])
    output_statistic_list = []
    input_statistic = None
    bouts_count = 0

    for filename in all_files:
        df = pd.read_csv(filename, index_col='DateTime', parse_dates=True)
        df = df.resample('1S').max()
        df = df.dropna()
        df = df[df.y1 > 0]

        if input_statistic is not None:
            input_statistic = pd.concat([input_statistic, df])
        else:
            input_statistic = df
    input_statistic = input_statistic.sort_index()

    interval_state = input_statistic.iloc[0]['moving_rate'] > moving_threshold
    interval_start_time = input_statistic.index[0]
    prev_state = interval_state
    last_time = input_statistic.index[0]
    # output_statistic.loc[0] = [prev_state, prev_time, None, None, None, None, None]
    # print(input_statistic)
    for i in tqdm(range(1, len(input_statistic))):
        cur_time = input_statistic.index[i]
        time_between_frames = pd.to_datetime(cur_time) - pd.to_datetime(last_time)

        # frames with a moving_rate above 0.99 considered a false state (no movement)
        state = (input_statistic.iloc[i]['moving_rate'] > moving_threshold) and (
                input_statistic.iloc[i]['moving_rate'] < 0.99)

        if (state != interval_state):
            # Если смена интервала в следствии изменения состояния
            # Собака пропадала из кадра надолго, ее состояние было не известно и это разные интервалы
            # или cостояние собаки изменилось
            # Заканчиваем интервал
            interval_length = pd.to_datetime(cur_time) - pd.to_datetime(interval_start_time)
            #  сохраняем

            if ((not interval_state and interval_length.total_seconds() > 30)  # none active minimum length
                    or (interval_state and interval_length.total_seconds() > 10)  # active minimum length
                    or len(output_statistic_list) == 0):
                # bouts_count +=1
                new_period = {'state': interval_state,
                              'start time': interval_start_time,
                              'end time': cur_time,
                              'interval': interval_length}
                output_statistic_list.append(new_period)
                # Выставляем новое начало и тип интервала
                interval_start_time = cur_time
                interval_state = state
            else:
                prev_interval = output_statistic_list.pop()
                interval_start_time = prev_interval['start time']
                interval_state = prev_interval['state']

        last_time = cur_time
        prev_state = state
    interval_length = pd.to_datetime(last_time) - pd.to_datetime(interval_start_time)
    new_period = {'state': interval_state,
                  'start time': interval_start_time,
                  'end time': last_time,
                  'interval': interval_length}
    output_statistic_list.append(new_period)

    output_statistic = pd.DataFrame(output_statistic_list, columns=['state', 'start time', 'end time', 'interval'])
    # output_statistic = pd.concat(output_statistic_list, ignore_index=True)
    output_statistic.to_csv(os.path.join(dir_path, 'st_' + name + '.csv'))
    print('statistic save into st_' + name + '.csv')

    sleep_intervals = output_statistic.loc[output_statistic['state'] == False]
    total_sleep_time = timedelta()
    bouts_count = len(output_statistic_list) // 2

    for k, i in tqdm(sleep_intervals.iterrows()):
        total_sleep_time += i['interval']

    date = os.path.basename(dir_path)

    with open(os.path.join(dir_path, 'summary_statistic_' + name + ".txt"), "w") as text_file:
        print(date)
        text_file.write("Total sleep time: {}".format(total_sleep_time))
        print("Total sleep time: {}".format(total_sleep_time))

        text_file.write("Bouts count: {}".format(bouts_count))
        print("Bouts count: {}".format(bouts_count))

    update_report(int(date), total_sleep_time, bouts_count)


# updates the report file
def update_report(date, total_sleep, bouts):
    date_to_row = {13: 3, 14: 4, 15: 5, 16: 6, 17: 7, 18: 8, 20: 9, 21: 10, 22: 11, 23: 12, 31: 13}

    inactive_time_column = 6
    bouts_column = 9

    row = date_to_row.get(date)
    wb = xw.Book('report.xlsx')
    ws = wb.sheets[0]

    ws.cells(row, inactive_time_column).value = convert(total_sleep.total_seconds())
    ws.cells(row, bouts_column).value = bouts


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)

