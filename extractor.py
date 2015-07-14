#!/usr/bin/env python2.7
from bs4 import BeautifulSoup
import requests
from pyvirtualdisplay import Display
from selenium import webdriver
import time

display = Display().start()
browser = webdriver.Firefox()
root_url = "https://www.google.com/flights/#search;f=SIN;t=BKK,DMK;d=2015-07-20;r=2015-07-22"

def get_data():
    browser.get(root_url)
    time.sleep(1)
    html = browser.page_source
    browser.quit()
    soup = BeautifulSoup(html)
    return soup.prettify()

