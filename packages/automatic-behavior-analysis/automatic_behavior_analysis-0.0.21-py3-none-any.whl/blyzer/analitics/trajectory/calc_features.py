import os
import numpy as np
import imageio

from blyzer.analitics.trajectory.helper import *


FEATURES_NAMES = ['turn30_60',
                  'turn60_90',
                  'turn90_120',
                  'turn120',
                  'area',
                  'IU',
                  'ST',
                  'MSD',
                  'SI',
                  'FD']

def split_data(points):
    res = []
    nan_inds = np.where(np.isnan(points).any(axis=1))
    seq_start = 0
    for nan_ind in nan_inds[0]:
        chunk = points[seq_start:nan_ind]
        if chunk.shape[0]>0:
            print(seq_start, nan_ind)
            print(chunk.shape)
            res.append(chunk)
        seq_start = nan_ind+1
    return res



def trajectory_features(points, distance, k_nearest=7):

    # calc features
    turn30_60 = 0
    turn60_90 = 0
    turn90_120 = 0
    turn120 = 0

    #res = split_data(points)
    #print(len(res))
    #for s in res:
    s = simplify(points)
    turn30_60 += turn_number(s, 30, 60)
    turn60_90 += turn_number(s, 60, 90)
    turn90_120 += turn_number(s, 90, 120)
    turn120 += turn_number(s, 120)

    usefull_points = points[~np.isnan(points).any(axis=1)]

    if points.shape[0] < 3:
        hull = 0
        area = 0
        IU = 0
    else:
        ch = concaveHull(usefull_points, k_nearest)
        if ch is not None:
            hull = np.array(ch)
            area = PolyArea(hull[:, 0], hull[:, 1])
            IU = distance / np.sqrt(area)
        else:
            hull = 0
            area = 0
            IU = 0


    #plt.figure()
    #plt.grid()
    #plt.xlabel('x')
    #plt.ylabel('y')
    #plotPath(points, hull)
    #plt.show()

    # straightness
    ST = np.linalg.norm(usefull_points[1, :] - usefull_points[-1, :]) / distance

    # Mean Square Displacement
    r = np.sqrt(usefull_points[:, 0] ** 2 + usefull_points[:, 1] ** 2)
    diff = np.diff(r)
    diff_sq = diff ** 2
    MSD = np.mean(diff_sq)

    # sinuosity
    steps = []
    for idx, k in enumerate(usefull_points[:-1]):
        steps.append(np.linalg.norm(usefull_points[idx + 1, :] - k))
    directions = np.diff(points, axis=0)
    angles = angle(directions)
    angles = [x for x in angles if str(x) != 'nan']
    p = np.mean(steps)
    b = np.std(steps) / p
    s = np.mean(list(map(np.sin, angles)))
    c = np.mean(list(map(np.cos, angles)))
    SI = 2 / np.sqrt(p * ((1 - c ** 2 - s ** 2) / ((1 - c) ** 2 + s ** 2) + b ** 2))

    # fractal dimension
    fig, ax = plt.subplots()
    ax.plot(usefull_points[:, 0], usefull_points[:, 1], 'k')
    ax.axis('off')
    plt.savefig('1.png')
    I = imageio.imread("1.png") / 256.0
    FD = fractal_dimension(rgb2gray(I))
    os.remove('1.png')

    return [turn30_60,
            turn60_90,
            turn90_120,
            turn120,
            area,
            IU,
            ST,
            MSD,
            SI,
            FD]
