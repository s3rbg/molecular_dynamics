#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 11:09:57 2021

@author: dgiron
"""

from common_modules.imports import *
from common_modules.units_dicts import *
from common_modules.errors import InputError

def check_type(df):
    check_float = [i for i, j in zip(keywords, default_data) if type(j) == float]
    check_int = [i for i, j in zip(keywords, default_data) if type(j) == int]
    for i in check_float:
        try:
            float(df[i].iloc[0])
        except:
            raise InputError('Wrong type detected in "{}". Expected float, but got string'.format(i))
            
    for i in check_int:
        try:
            int(df[i].iloc[0])
        except:
            raise InputError('Wrong type detected in "{}". Expected int, but got string'.format(i))
            
def check_type_gui(lec):
    for i in ("Density", "Number of cells", "Temperature", 'Max steps', 'Step'):
        
        try:
            if i == 'Number of cells' or i == 'Max steps':
                a = 'int'
                lec.lee_int(i)
            else:
                a = 'float'
                lec.lee_float(i)
        except ValueError:
            raise InputError('Invalid type introduced in "{}". Expected {}. Remember to use "." as separator'.format(i, a))
            
def remove_comments(df):
    if (len(df) < 2):
        raise InputError('Wrong number of columns. {} instead of 3 (or more counting comments)'.format(len(df)+1))
    df = df.iloc[:2]
    return df

def check_keywords(df):
    for i in df.columns:
        if i not in keywords:
            raise InputError('"{}" is not a valid keyword'.format(i))
