from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta
import gspread
from google.oauth2.service_account import Credentials
from selenium.webdriver.support.ui import Select
import pytz
import random

driver = webdriver.Chrome()

driver.get('https://mesonet.agron.iastate.edu/wx/afos/list.phtml')

box_of_links = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'sectPFMDMX')))

table_identifier = 'sectPFMDMX'

driver.find_element(By.XPATH, f'//*[@id="{table_identifier"]/a[{best_index}]')

print(box_of_links.text)
