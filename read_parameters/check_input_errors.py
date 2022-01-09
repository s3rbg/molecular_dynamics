#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 11:09:57 2021

@author: dgiron
"""

from common_modules.imports import *
from common_modules.units_dicts import *
from common_modules.errors import InputError


def check_str(list_of_options, element, err_msg):
    """
    Checks if an input string is in a given list

    Parameters
    ----------
    list_of_options : array
        list with the valid options.
    element : str
        element to look for in the list.
    err_msg : str
        error message to be displayed.

    Raises
    ------
    InputError
        If the elements is not in the list.

    Returns
    -------
    None.

    """
    if (element not in list_of_options):
        raise InputError(err_msg)

def check_type(df):
    """
    Check if the input parameters are of the correct type, i.e. float/string...

    Parameters
    ----------
    df : pandas.DataFrame
        dataframe with the parameters.

    Raises
    ------
    InputError
        If there is any type incorrect.

    Returns
    -------
    None.

    """
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
    """
    Checks if the parameters introduced in the GUI are valid

    Parameters
    ----------
    lec : object
        object of the class 'lectura'.

    Raises
    ------
    InputError
        If there is any type incorrect.

    Returns
    -------
    None.

    """
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
    """
    Removes columns from the 3rd one, i.e, the ones with comments.

    Parameters
    ----------
    df : pandas.DataFrame
        dataframe with parameters.

    Raises
    ------
    InputError
        If the number of columns is less than the minimum required.

    Returns
    -------
    df : pandas.DataFrame
        new dataframe with only parameters columns.

    """
    if (len(df) < 2):
        raise InputError('Wrong number of columns. {} instead of 3 (or more counting comments)'.format(len(df)+1))
    df = df.iloc[:2]
    return df

def check_keywords(df):
    """
    Check if all the keywords given are correctly typed

    Parameters
    ----------
    df : pandas.DataFrame
        dataframe with parameters.

    Raises
    ------
    InputError
        If any keyword is not correctly spelled.

    Returns
    -------
    None.

    """
    for i in df.columns:
        if i not in keywords:
            raise InputError('"{}" is not a valid keyword'.format(i))
