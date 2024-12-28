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

import random

def historical_forecasted_highs(location, region, table_identifier, link_identifier, time_length, timeshift):
    # Get today's date
    today = datetime.now()
    # Format the date as ['YYYY', 'Mon', 'DD']
    current_date = [today.strftime('%Y'), today.strftime('%b'), today.strftime('%d')]

    historical_forecasted_highs = []

    for i in range(time_length):
        #time.sleep(random.randint(1, 10))

        driver.get("https://mesonet.agron.iastate.edu/wx/afos/list.phtml")

        # Selecting the choose station dropdown
        choose_station_dropdown = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="main-content"]/div/form/div/div[1]/span[1]/span[1]/span')))
        choose_station_dropdown.click()

        # Entering which station we would like to select
        choose_station_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/span/span/span[1]/input')))

        choose_station_input.send_keys(location)
        choose_station_input.send_keys(Keys.ENTER)

        # Identifying drop-downs by name
        year = Select(driver.find_element(By.NAME, 'year'))
        month = Select(driver.find_element(By.NAME, 'month'))
        day = Select(driver.find_element(By.NAME, 'day'))

        # Inputting the dates
        year.select_by_visible_text(current_date[0])
        month.select_by_visible_text(current_date[1])
        day.select_by_visible_text(current_date[2])

        # Clicking "Giveme giveme!" button
        give_me_button = driver.find_element(By.XPATH, '//*[@id="main-content"]/div/form/div/div[3]/input')
        give_me_button.click()

        # Calling method to identify forecast, identify daily high; adding daily high to daily high list
        daily_high = max_min_identifier(table_identifier, link_identifier, timeshift, region)
        print(daily_high)
        historical_forecasted_highs.append(daily_high)

        # Subtracting a day from the date and setting that as the current date
        past_date = today - timedelta(days=(i+1))
        current_date = [past_date.strftime('%Y'), past_date.strftime('%b'), past_date.strftime('%#d')]

    #write_to_google_sheets(historical_forecasted_highs, location)

def max_min_identifier(table_identifier, link_identifier, timeshift, region):
    # Identifying the table containing those links
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, table_identifier)))
    box_of_links = driver.find_element(By.ID, table_identifier).text

    # Identifying all links that contain the text PFM
    links = driver.find_elements(By.PARTIAL_LINK_TEXT, link_identifier)

    # Converting the table into timestamps
    timestamps = [line.split('@')[1].strip() for line in box_of_links.strip().split('\n')]

    # Calling method to determine which timestamp is closest to 3:00 am
    best_index = closest_to_window(timeshift, timestamps) + 1

    links[best_index].click()

    table = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-content"]/div/pre')))
    table = table.text
    table = table.splitlines()

    for line in table:
        if region == line:
            max_min_row = table[table.index(line) + 8]
            max_min_row = max_min_row.split()

            forecasted_high = max_min_row[1]

            return forecasted_high

            '''
            data = line.split()

            for point in data:
                if point == 'Max/'
            forecastedHigh = table[table.index(element)+1]

            return forecastedHigh
            break
            '''

def closest_to_window(timeshift, timestamps):
    shifted_times = []
    for time in timestamps:
        original_time = datetime.strptime(time, "%H:%M")
        shifted_time = original_time - timedelta(hours=timeshift)
        shifted_times.append(shifted_time)

    # Define the target time (3:00 AM)
    target_time = datetime.strptime("03:00", "%H:%M")

    # Find the index of the closest time to the target
    closest_index = -1
    min_diff = float('inf')  # Start with a large difference

    for i, time in enumerate(shifted_times):
        diff = abs((time - target_time).total_seconds())
        if diff < min_diff:
            min_diff = diff
            closest_index = i

    return closest_index

def write_to_google_sheets(historical_forecasted_highs, location):
    # Writing to Google Sheets
    # Define the scope
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
              'https://www.googleapis.com/auth/drive']

    # Load the service account key
    credentials = Credentials.from_service_account_file(r"keen-enigma-445900-c8-2eaccc8cc1a4.json", scopes=SCOPES)

    # Authorize gspread
    client = gspread.authorize(credentials)

    # Open the Google Sheet by name or URL
    spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1L-Wg1ZqlbkVqMmIiwUg1GimPKLD0-MrFuKUdlfBhNNY/edit?gid=0#gid=0')

    # Select a worksheet (by name or index)
    randomly_generated_worksheet_title = str(random.randint(0, 9999999))
    worksheet = spreadsheet.add_worksheet(title=randomly_generated_worksheet_title, rows="100", cols="20")

    worksheet.update_cell(1, 1, location)
    worksheet.update_cell(1, 2, 'Forecasted')

    # Get today's date
    date = datetime.now()

    for i in range(len(historical_forecasted_highs)):
        try:
            formatted_date = date.strftime('%Y %b %d')

            row = [formatted_date, historical_forecasted_highs[i]]

            worksheet.insert_row(row, i+2)

            date = date - timedelta(days=(1))
        except:
            time.sleep(60)
            i -= 1
            continue

def historical_highs():
    link = input("Please input link: ")
    driver.get(link)

    table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-content"]/div/pre'))).text

    table = table.split()

    print(table)









time_length = int(input("Please enter how many days back you would like the data to go: "))

# Initializing webdriver
driver = webdriver.Chrome()

# Calling method for New York
#historical_forecasted_highs("New York", 'Central Park-New York NY', 'sectPFMOKX', 'PFMOKX', time_length, 5)

# Calling method for Miami
#historical_forecasted_highs("Miami", 'Miami-Miami Dade FL','sectPFMMFL', 'PFMMFL', time_length, 5)

# Calling method for Philadelphia
#historical_forecasted_highs("Mount Holly", 'Philadelphia-Philadelphia PA', 'sectPFMPHI', 'PFMPHI', time_length, 5)

# Calling method for Chicago
#historical_forecasted_highs("Chicago", 'Chicago Midway Airport-Cook IL', 'sectPFMLOT', 'PFMLOT', time_length, 6)

# Calling method for Denver
historical_forecasted_highs("Denver", 'Chicago Midway Airport-Cook IL', 'sectPFMBOU', 'PFMBOU', time_length, 6)
