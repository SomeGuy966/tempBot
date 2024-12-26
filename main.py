from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta
import gspread
from google.oauth2.service_account import Credentials

current_date = datetime.now()
previous_date = current_date - timedelta(days=1)
desired_date = previous_date.strftime("%b %d")

path = r"/Users/anthonyge/Downloads/chromedriver-mac-arm64/chromedriver"
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)




#Central Park temperatures
driver.get('http://www.weather.gov/wrh/timeseries?site=knyc')

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'highcharts-subtitle')))

dates = []
temps = []

counter = 1

while True:
    try:
        date = driver.find_element(By.XPATH, '//*[@id="OBS_DATA"]/tbody/tr[' + str(counter) + ']/td[1]')

        if desired_date in date.text:
            dates.append(driver.find_element(By.XPATH, '//*[@id="OBS_DATA"]/tbody/tr[' + str(counter) + ']/td[1]'))
            temps.append(driver.find_element(By.XPATH, '//*[@id="OBS_DATA"]/tbody/tr[' + str(counter) + ']/td[2]'))

        counter += 1
    except:
        break


# Converting lists to text
for i in range(len(dates)):
    dates[i] = dates[i].text
for i in range(len(temps)):
    temps[i] = temps[i].text







# LaGuardia temperatures
driver.get('https://www.weather.gov/wrh/timeseries?site=klga')

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="dataToggle"]'))).click()
time.sleep(3)

datesLGA = []
tempsLGA = []

counter = 1

while True:
    try:
        dateLGA = driver.find_element(By.XPATH, '//*[@id="OBS_DATA"]/tbody/tr[' + str(counter) + ']/td[1]')

        if desired_date in dateLGA.text:
            datesLGA.append(driver.find_element(By.XPATH, '//*[@id="OBS_DATA"]/tbody/tr[' + str(counter) + ']/td[1]'))
            tempsLGA.append(driver.find_element(By.XPATH, '//*[@id="OBS_DATA"]/tbody/tr[' + str(counter) + ']/td[2]'))

        counter += 1
    except:
        break

# Converting lists to text
for i in range(len(datesLGA)):
    datesLGA[i] = datesLGA[i].text
for i in range(len(tempsLGA)):
    tempsLGA[i] = tempsLGA[i].text



dummyDatesLGA = datesLGA[:]

for date in dummyDatesLGA:
    if (date in dates) == False:
        index = datesLGA.index(date)
        tempsLGA.pop(index)
        datesLGA.pop(index)

dummyDates = dates[:]

for date in dummyDates:
    if (date in datesLGA) == False:
        index = dates.index(date)
        temps.pop(index)
        dates.pop(index)




# Writing to Google Sheets
# Define the scope
SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

# Load the service account key
credentials = Credentials.from_service_account_file(r"/Users/anthonyge/Downloads/keen-enigma-445900-c8-2eaccc8cc1a4.json", scopes=SCOPES)

# Authorize gspread
client = gspread.authorize(credentials)

# Open the Google Sheet by name or URL
spreadsheet = client.open("NYTempData")

# Select a worksheet (by name or index)
worksheet = spreadsheet.worksheet("Sheet1")

# Write a row of data
counter = len(dates) - 1

for i in range(len(dates)):
    row = [datesLGA[counter], dates[counter], tempsLGA[counter], temps[counter]]
    worksheet.insert_row(row, 2)

    counter -= 1

