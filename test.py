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

driver = webdriver.Chrome()

driver.get('https://mesonet.agron.iastate.edu/wx/afos/p.php?pil=PFMLOT&e=202405010815')

table = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-content"]/div/pre'))).text

table = table.splitlines()

print(table)


