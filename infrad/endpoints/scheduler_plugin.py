#! /usr/bin/env python
"""
    File name: scheduler_plugin.py
    Author: Dimitar Petrov
    Date created: 2018/06/19
    Python Version: 3.6
    Description: Plugin that stores activity for latter time
"""

import logging
import pytz
import datetime as dt
import collections
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from infrad.endpoints.plugin_endpoint import Plugin
from infrad.shared.events import EventHook

logger = logging.getLogger(__name__)  # pylint: disable-msg=C0103


class SchedulerPlugin(Plugin):  # pylint: disable-msg=R0903
    """Plugin that schedules activities"""

    def __init__(self):
        logger.info('Initialize Scheduler Plugin')
        self.module = 'scheduler'
        self.datefmt = '%Y-%m-%dT%H:%M'
        self.scheduler = BackgroundScheduler(
            jobstores={
                'default': MemoryJobStore(),
            },
            executors={'default': ThreadPoolExecutor(5)},
            job_defaults={
                'coalesce': False,
                'max_instances': 3
            },
            timezone=pytz.timezone('Europe/Sofia'))
        self.scheduler.start()
        self.callbacks = collections.defaultdict(EventHook)

    def add_callback(self, name, fun):
        self.callbacks[name] += fun

    def add_job(self, *args, **kwargs):
        if 'timestamp' in kwargs:
            if 'method' in kwargs:
                timestamp = dt.datetime.strptime(
                    kwargs.pop('timestamp'), self.datefmt)
                method = kwargs.pop('method')
                self.scheduler.add_job(
                    self.callbacks[method],
                    args=args,
                    kwargs=kwargs,
                    trigger='date',
                    run_date=timestamp)
                return "Success"

        logger.warning('Missing timestamp %s', kwargs)
        return "Fail"

    def do_work(self, action, *args, **kwargs):
        if action == 'add':
            return self.add_job(*args, **kwargs)

        return "Fail"


if __name__ == '__main__':

    def callback(*args, **kwargs):
        print(args)
        print(kwargs)

    plug = SchedulerPlugin()
    plug.add_callback('cb', callback)
    tstamp = '2018-06-19T15:32'
    plug.add_job(*['arg1'], **{
        'timestamp': tstamp,
        'method': 'cb',
        'kwarg1': 'value1'
    })
    import time
    while True:
        time.sleep(1)
