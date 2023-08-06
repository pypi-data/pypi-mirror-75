import numpy as np
import scipy.spatial as spt
import matplotlib.pyplot as plt
from matplotlib.path import Path
import blyzer.analitics.trajectory.lineintersect as li

def simplify(df):
    p1 = 0
    p2 = 1
    path = [df[0, :]]
    while True:
        if p1 >= len(df) or p2 >= len(df):
            break
        if np.linalg.norm(df[p2, :] - df[p1, :]) >= 15:
            path.append(df[p2, :])
            p1 = p2
        p2 += 1
    return np.array(path)

def angle(dir):
    dir2 = dir[1:]
    dir1 = dir[:-1]
    return np.arccos((dir1*dir2).sum(axis=1)/(np.sqrt((dir1**2).sum(axis=1)*(dir2**2).sum(axis=1))))


def turn_number(s, min_angle, max_angle=None):
    directions = np.diff(s, axis=0)
    theta = angle(directions)

    min_angle = min_angle * np.pi / 180

    if max_angle == None:
        idx = np.where(theta >= min_angle)[0] + 1
    else:
        max_angle = max_angle * np.pi / 180
        idx = theta[(theta >= min_angle) & (theta <= max_angle)]
    return len(idx)


def calc_distance(s):
    lengths = np.sqrt(np.sum(np.diff(s, axis=0) ** 2, axis=1))
    total_length = np.sum(lengths)
    return total_length


def PolyArea(x, y):
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


def GetFirstPoint(dataset):
    ''' Returns index of first point, which has the lowest y value '''
    # todo: what if there is more than one point with lowest y?
    imin = np.argmin(dataset[:, 1])
    return dataset[imin]


def GetNearestNeighbors(dataset, point, k):
    ''' Returns indices of k nearest neighbors of point in dataset'''
    # todo: experiment with leafsize for performance
    mytree = spt.cKDTree(dataset, leafsize=10)
    distances, indices = mytree.query(point, k)
    # todo: something strange here, we get more indices than points in dataset
    #       so have to do this
    return dataset[indices[:dataset.shape[0]]]


def SortByAngle(kNearestPoints, currentPoint, prevPoint):
    ''' Sorts the k nearest points given by angle '''
    angles = np.zeros(kNearestPoints.shape[0])
    i = 0
    for NearestPoint in kNearestPoints:
        # calculate the angle
        angle = np.arctan2(NearestPoint[1] - currentPoint[1],
                           NearestPoint[0] - currentPoint[0]) - \
                np.arctan2(prevPoint[1] - currentPoint[1],
                           prevPoint[0] - currentPoint[0])
        angle = np.rad2deg(angle)
        # only positive angles
        angle = np.mod(angle + 360, 360)
        # print NearestPoint[0], NearestPoint[1], angle
        angles[i] = angle
        i = i + 1
    return kNearestPoints[np.argsort(angles)]


def plotPoints(dataset):
    plt.plot(dataset[:, 0], dataset[:, 1], 'o', markersize=10, markerfacecolor='0.75',
             markeredgewidth=1)
    plt.axis('equal')
    plt.axis([min(dataset[:, 0]) - 0.5, max(dataset[:, 0]) + 0.5, min(dataset[:, 1]) - 0.5,
              max(dataset[:, 1]) + 0.5])
    plt.show()


def plotPath(dataset, path):
    plt.plot(dataset[:, 0], dataset[:, 1], 'o', markersize=8, markerfacecolor='0.65',
             markeredgewidth=0)
    path = np.asarray(path)
    plt.plot(path[:, 0], path[:, 1], 'o', markersize=8, markerfacecolor='0.55',
             markeredgewidth=0)
    plt.plot(path[:, 0], path[:, 1], '-', lw=1.4, color='k')
    plt.axis('equal')
    plt.axis([min(dataset[:, 0]) - 0.5, max(dataset[:, 0]) + 0.5, min(dataset[:, 1]) - 0.5,
              max(dataset[:, 1]) + 0.5])
    # plt.axis('off')
    # plt.savefig('./doc/figure_1.png', bbox_inches='tight')
    # plt.show()


def removePoint(dataset, point):
    delmask = [np.logical_or(dataset[:, 0] != point[0], dataset[:, 1] != point[1])]
    newdata = dataset[delmask]
    return newdata


def concaveHull(dataset, k):
    assert k >= 3, 'k has to be greater or equal to 3.'
    if k >= 300: return None
    points = dataset
    # todo: remove duplicate points from dataset
    # todo: check if dataset consists of only 3 or less points
    # todo: make sure that enough points for a given k can be found

    firstpoint = GetFirstPoint(points)
    # init hull as list to easily append stuff
    hull = []
    # add first point to hull
    hull.append(firstpoint)
    # and remove it from dataset
    points = removePoint(points, firstpoint)
    currentPoint = firstpoint
    # set prevPoint to a Point righ of currentpoint (angle=0)
    prevPoint = (currentPoint[0] + 10, currentPoint[1])
    step = 2

    while ((not np.array_equal(firstpoint, currentPoint) or (step == 2)) and points.size > 0):
        if (step == 5):  # we're far enough to close too early
            points = np.append(points, [firstpoint], axis=0)
        kNearestPoints = GetNearestNeighbors(points, currentPoint, k)
        cPoints = SortByAngle(kNearestPoints, currentPoint, prevPoint)
        # avoid intersections: select first candidate that does not intersect any
        # polygon edge
        its = True
        i = 0
        while ((its == True) and (i < cPoints.shape[0])):
            i = i + 1
            if (np.array_equal(cPoints[i - 1], firstpoint)):
                lastPoint = 1
            else:
                lastPoint = 0
            j = 2
            its = False
            while ((its == False) and (j < np.shape(hull)[0] - lastPoint)):
                its = li.doLinesIntersect(hull[step - 1 - 1], cPoints[i - 1],
                                          hull[step - 1 - j - 1], hull[step - j - 1])
                j = j + 1
        if (its == True):
            print("all candidates intersect -- restarting with k = ", k + 1)
            return concaveHull(dataset, k + 1)
        prevPoint = currentPoint
        currentPoint = cPoints[i - 1]
        # add current point to hull
        hull.append(currentPoint)
        points = removePoint(points, currentPoint)
        step = step + 1
    # check if all points are inside the hull
    p = Path(hull)
    pContained = p.contains_points(dataset, radius=0.0000000001)
    if (not pContained.all()):
        print("not all points of dataset contained in hull -- restarting with k = ", k + 1)
        return concaveHull(dataset, k + 1)

    print("finished with k = ", k)
    return hull


def fractal_dimension(Z, threshold=0.5):
    # Only for 2d image
    assert(len(Z.shape) == 2)

    # From https://github.com/rougier/numpy-100 (#87)
    def boxcount(Z, k):
        S = np.add.reduceat(
            np.add.reduceat(Z, np.arange(0, Z.shape[0], k), axis=0),
                               np.arange(0, Z.shape[1], k), axis=1)

        # We count non-empty (0) and non-full boxes (k*k)
        return len(np.where((S > 0) & (S < k*k))[0])

    # Transform Z into a binary array
    Z = (Z < threshold)

    # Minimal dimension of image
    p = min(Z.shape)

    # Greatest power of 2 less than or equal to p
    n = 2**np.floor(np.log(p)/np.log(2))

    # Extract the exponent
    n = int(np.log(n)/np.log(2))

    # Build successive box sizes (from 2**n down to 2**1)
    sizes = 2**np.arange(n, 1, -1)

    # Actual box counting with decreasing size
    counts = []
    for size in sizes:
        counts.append(boxcount(Z, size))

    # Fit the successive log(sizes) with log (counts)
    coeffs = np.polyfit(np.log(sizes), np.log(counts), 1)
    return -coeffs[0]


def rgb2gray(rgb):
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray
