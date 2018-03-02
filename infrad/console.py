# -*- coding: utf-8 -*-
#! /usr/bin/env python

"""
    File name: console.py
    Author: Dimitar Petrov
    Date created: 2018/03/02
    Python Version: 3.6
    Description: Entry point for infrad
"""

from __future__ import unicode_literals, absolute_import, print_function
import click


@click.command()
def main():
    """Console application"""
    print('I am console')
