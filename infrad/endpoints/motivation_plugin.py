#! /usr/bin/env python

"""
    File name: motivation_plugin.py
    Author: Dimitar Petrov
    Date created: 2019/27/07
    Python Version: 3.6
    Description: Plugin that helps me motivate
"""
import logging
from infrad.endpoints.plugin_endpoint import Plugin
import subprocess
import random
import requests
import json

logger = logging.getLogger(__name__)  # pylint: disable-msg=C0103


class MotivationPlugin(Plugin):  # pylint: disable-msg=R0903
    """Plugin used to assist with motivation"""
    def __init__(self):
        logger.info("Initialize Motivation Plugin")
        self.module = 'motivation'
        self.kodi_url = 'http://durden:8080/jsonrpc'
        self.videos = [
            'wnHW6o8WMas',
            'gMFc7agO09w',
            'pVxuKxK-Og4',
            'kPbr8mNVycQ',
            'c4FSVjdoADk',
        ]

    def rpc_payload(self, videoid):
        return [{
            "id": 383,
            "jsonrpc": "2.0",
            "method": "Playlist.Clear",
            "params": {
                "playlistid": 1
            }}, {
                "id": 587,
                "jsonrpc": "2.0",
                "method": "Playlist.Add",
                "params": {
                    "playlistid": 1,
                    "item": {
                        "file": "plugin://plugin.video.youtube/play/?video_id={}".format(videoid)
                    }
            }}, {
                "id": 250,
                "jsonrpc": "2.0",
                "method": "Player.Open",
                "params": {
                    "item": {
                        "playlistid": 1,
                        "position": 0
                    }
            }}]

    def kodi_play_motivational_video(self, videoid=None):
        if not videoid:
            videoid = random.choice(self.videos)

        requests.post(
            self.kodi_url, data=json.dumps(
                self.rpc_payload(videoid)))

    def do_work(self, action, *args, **kwargs):
        if action == 'kodi_video':
            self.kodi_play_motivational_video(**kwargs)
            return "Success"

        return "Fail"
