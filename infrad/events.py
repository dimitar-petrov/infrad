#! /usr/bin/env python

"""
    File name: events.py
    Author: Dimitar Petrov
    Date created: 2018/03/04
    Python Version: 3.6
    Description: Define all events
"""

from enum import Enum

EVENT_TYPE = Enum("EVENT_TYPE", "REQUEST RESPONSE")

class Event:
    """Base event"""
    def __init__(self, event_type):
        self.type = event_type

class RequestEvent(Event):
    def __init__(self, method, kwargs, sync=True):
        super().__init__(EVENT_TYPE.REQUEST)
        self.method = method
        self.kwargs = kwargs
        self.sync = sync

class ResponseEvent(Event):
    def __init__(self, response):
        super().__init__(EVENT_TYPE.RESPONSE)
        self.text = response
