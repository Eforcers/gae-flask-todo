import logging
import unittest
import os
import subprocess
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC
import time

class GuiTest(unittest.TestCase):
    APP_ENGINE_SDK = ''
    PROJECT_PATH = ''

    def assertElementByClassIsPresent(self,class_name,message):
        try:
            elem = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
        except:
            assert 0, message

    def assertElementByIdIsPresent(self,id,message):
        try:
            elem = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, id)))
        except:
            assert 0, message

    def assertElementByIdVisible(self,id,message):
        try:
            elem = WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.ID, id)))
        except:
            assert 0, message



    def setUp(self):
        #start appengine server
        dev_server = os.path.join(self.APP_ENGINE_SDK,"dev_appserver.py")
        command = ['python',dev_server, self.PROJECT_PATH, "--clear_datastore=yes" ]
        self.dev_server = subprocess.Popen(command, stdin = subprocess.PIPE, stdout = subprocess.PIPE)
        self.browser = webdriver.Firefox()


    def tearDown(self):
        self.browser.close()
        self.dev_server.kill()

    def test_login(self):
        self.browser.get("http://localhost:8080") # Load page
        self.browser.find_element_by_tag_name("a").click()
        self.browser.find_element_by_id('admin').click()
        self.browser.find_element_by_id('submit-login').click()
        id = "todo-title"
        self.assertElementByIdVisible(id,"%s never show up" % id)
        todo_name = "Todo 1"
        self.browser.find_element_by_id('new-title-input').send_keys(todo_name)
        self.browser.find_element_by_id('add-todo-btn').click()
        self.assertElementByClassIsPresent("todo-title-cls","Todo was not created")





