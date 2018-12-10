#! /usr/bin/env python

"""
    File name: domain_model.py
    Author: Dimitar Petrov
    Date created: 2018/04/09
    Python Version: 3.6
    Description: Abstract classes for models
"""
from abc import ABCMeta


class DomainModel(metaclass=ABCMeta):  # pylint: disable-msg=R0903
    """Abstract Base Class for Domain Model"""
