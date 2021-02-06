#! /usr/bin/env python

"""
    File name: browser_plugin.py
    Author: Dimitar Petrov
    Date created: 2020/03/31
    Python Version: 3.7
    Description: Plugin that helps automate the boring stuff
"""
import logging
from infrad.endpoints.plugin_endpoint import Plugin
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import subprocess
import random
import requests
import json
import time
from infrad.passtore import PassStore

logger = logging.getLogger(__name__)  # pylint: disable-msg=C0103


class BrowserPlugin(Plugin):  # pylint: disable-msg=R0903
    """Plugin used to automate the boring mundane stuff with browser"""
    def __init__(self):
        logger.info("Initialize Browser Plugin")
        self.pstore = PassStore()
        self.module = 'browser'
        self._driver = None

    def _find_elements(self, by, value, timeout=10):
        try:
            element_present = EC.presence_of_element_located(
                (by, value))
            WebDriverWait(self._driver, timeout).until(element_present)
        except TimeoutException:
            logger.exception(
                '[{}] failed locating element [{}]'.format(
                    self.__class__.__name__, value))
        finally:
            return self._driver.find_elements(by, value)

    def _configure_selenium(self):
        return webdriver.Chrome()

    def pay_health_insuranse(self):
        self._driver.get('https://inetdec.nra.bg/index.html')
        pik_login_link = [
            x for x in self._find_elements(By.CLASS_NAME, 'list-links') if '(ПИК)' in x.text][0]
        pik_login_link.click()

        input_id = self._find_elements(By.NAME, 'ipID')[0]
        input_id.send_keys(
            self.pstore.getkey("nap.bg", "egn")
        )

        input_pic = self._find_elements(By.NAME, 'ipPIC')[0]
        input_pic.send_keys(
            self.pstore.getkey("nap.bg", "pass"))

        submit_btn = self._find_elements(By.ID, 'idSubmit')[0]
        submit_btn.click()

        self._find_elements(By.TAG_NAME, 'html', timeout=15)
        time.sleep(2)
        person_link = [
            x for x in self._find_elements(By.TAG_NAME, 'a') if 'ДИМИТЪР ПЕНКОВ ПЕТРОВ' in x.text][0]
        person_link.click()

        time.sleep(2)
        parent_link = [
            x for x in self._find_elements(By.CLASS_NAME, 'parent')
            if 'Предоставяне на данъчна и осигурителна информация' in x.text][0]
        parent_link.click()

        time.sleep(2)
        check_link = [
            x for x in self._find_elements(By.CLASS_NAME, 'shown_list')
            if 'Справка за задълженията с възможност за извършване на плащане' in x.text][0]
        check_link.click()

    def login_bank(self):
        self._driver.execute_script("window.open('');")
        self._driver.switch_to_window(self._driver.window_handles[-1])
        # self._driver.get('https://bankonweb.expressbank.bg/page/default.aspx?xml_id=/bg-BG/.login')
        self._driver.get("https://dskdirect.bg/page/default.aspx?xml_id=/bg-BG/.login")

        # user = self._find_elements(By.ID, 'userName')[0]
        user = self._find_elements(By.ID, 'Text1')[0]
        user.send_keys(
            self.pstore.getkey("dskdirect.bg", "username"))

        password = self._find_elements(By.ID, 'Password1')[0]
        password.send_keys(
            self.pstore.getkey("dskdirect.bg", "pass"))

        submit_btn = self._find_elements(By.ID, 'btn_login')[0]
        submit_btn.click()

    def do_work(self, action, *args, **kwargs):
        self._driver = self._configure_selenium()
        if action == 'health_insurance':
            self.pay_health_insuranse(**kwargs)
            self.login_bank(**kwargs)
            return "Success"
        elif action == "bank":
            self.login_bank(**kwargs)

        return "Fail"
