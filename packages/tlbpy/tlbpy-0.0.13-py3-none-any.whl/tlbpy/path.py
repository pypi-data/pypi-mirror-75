#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

__all__ = ['get_file_ext', 'get_files']

def get_file_ext(file):
    return file.split(".")[-1]

def get_files(dirpath, ext = [], basename=False):
    return [os.path.join(os.path.basename(dirpath), file) if not basename else file for file in os.listdir(dirpath) 
        if get_file_ext(file) in ext or 
            ext == [] or 
            (ext == ["*"] and os.path.isfile(os.path.join(dirpath, file)))]