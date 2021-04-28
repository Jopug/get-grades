#!/usr/bin/env python

import time
from datetime import datetime
from getpass import getpass
from sys import platform

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

if platform == "win32":
    from win10toast import ToastNotifier
    