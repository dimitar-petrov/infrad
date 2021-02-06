#! /usr/bin/env python

"""
    File name: screenlock_plugin.py
    Author: Dimitar Petrov
    Date created: 2018/04/09
    Python Version: 3.6
    Description: Plugin that helps me meditate
"""
import logging
from infrad.endpoints.plugin_endpoint import Plugin
import subprocess

logger = logging.getLogger(__name__)  # pylint: disable-msg=C0103


class MeditationPlugin(Plugin):  # pylint: disable-msg=R0903
    """Plugin used to assist in meditation"""
    def __init__(self):
        logger.info("Initialize Meditation Plugin")
        self.module = 'meditation'
        self.links = {
            "short_daily": "https://www.youtube.com/watch?v=i50ZAs7v9es",
            # 'alarm': "https://www.youtube.com/watch?v=kRoNkbWpwOQ",
            "alarm": "https://www.youtube.com/watch?v=mE1aEDmcRMg", # ludovico einaudi - ancora
            'proactive': "/home/dpetrov/bin/countdown.mp4"
        }

    def play_youtube_audio(self, link):
        subprocess.Popen(["/usr/bin/mpv", link, "--no-video"])

    def schedulle_wake_up(self, link, wait=14400):
        subprocess.Popen(["/home/dpetrov/bin/alarm.sh", str(wait), link])

    def killall(self):
        subprocess.Popen(["/usr/bin/pkill", 'qutebrowser'])
        subprocess.Popen(["/usr/bin/pkill", 'urxvt'])
        subprocess.Popen(["/usr/bin/pkill", 'firefox'])
        subprocess.Popen(["/usr/bin/pkill", 'evince'])

    def proactive(self, filename):
        subprocess.Popen(["/usr/bin/mpv", filename])

    def do_work(self, action, *args, **kwargs):
        if action == 'short_daily':
            self.play_youtube_audio(self.links[action])
            return "Success"
        elif action == 'alarm':
            self.schedulle_wake_up(self.links[action], **kwargs)
            return "Success"
        elif action == 'killall':
            self.killall()
            return "Success"
        elif action == 'proactive':
            self.proactive(self.links[action])
            return "Success"

        return "Fail"
