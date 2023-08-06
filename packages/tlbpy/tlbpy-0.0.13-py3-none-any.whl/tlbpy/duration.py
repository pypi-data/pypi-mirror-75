#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from time import time_ns

__all__ = ['Duration']

def current_time():
    return time.time_ns() / (10**9)

class Duration:
    def __init__(self):
        self.start = 0.0
        self.duree = 0.0
        self.top = True

    def __call__(self):
        if self.top:
            self.start = current_time()
            self.duree = 0.0
            self.top = False
        else :
            self.duree = current_time() - self.start
            self.start = current_time()
            self.top = True
        return self.duree
    
    def st(self):
        self.top = False
        self.start = current_time()

    def sp(self):
        self.top = True
        self.duree = current_time() - self.start

    def get(self):
        return self.duree

    def evaluate(self, func, *args, **kwargs):
        self.st()
        r = func(*args, **kwargs)
        self.sp()
        return (self.get(), r)
    