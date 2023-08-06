# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 12:54:14 2016

@author: siniz_000
"""

import time

class Timer(object):
    def __init__(self, verbose=False):
        self.verbose = verbose

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000
        if self.verbose:
            print ('Время выполения: %f ms' % self.msecs)
