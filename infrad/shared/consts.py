#! /usr/bin/env python

"""
    File name: consts.py
    Author: Dimitar Petrov
    Date created: 2018/04/09
    Python Version: 3.6
    Description: Constants used in infrad
"""
from enum import IntEnum


class JobState(IntEnum):
    """Stores the action state."""
    COMPLETED = 0
    RUNNING = 1
    FAILED = -1
