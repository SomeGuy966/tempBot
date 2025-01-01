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

def historical_forecasted_highs(location, region, table_identifier, link_identifier, time_length):
    # Sets the desired date as today's date
    desired_date = datetime.now()

    historical_forecasted_highs = []

    for i in range(time_length):
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
        year = Select(driver.find_element(By.XPATH, '//*[@id="main-content"]/div/form/div/div[2]/select[1]'))
        month = Select(driver.find_element(By.XPATH, '//*[@id="main-content"]/div/form/div/div[2]/select[2]'))
        day = Select(driver.find_element(By.XPATH, '//*[@id="main-content"]/div/form/div/div[2]/select[3]'))

        # Format the date as ['YYYY', 'Mon', 'DD']
        formatted_date = desired_date.strftime('%Y %b %d').replace(' 0', ' ').split()

        # Inputting the dates
        year.select_by_visible_text(formatted_date[0])
        month.select_by_visible_text(formatted_date[1])
        day.select_by_visible_text(formatted_date[2])

        # Clicking "Giveme giveme!" button
        give_me_button = driver.find_element(By.XPATH, '//*[@id="main-content"]/div/form/div/div[3]/input')
        give_me_button.click()

        # Calling method to identify forecast, identify daily high; adding daily high to daily high list
        daily_high = max_min_identifier(table_identifier, link_identifier, desired_date, region)
        print(daily_high)
        historical_forecasted_highs.append(daily_high)

        # Subtracting a day from the date and setting that as the desired date
        desired_date = desired_date - timedelta(days=(1))

def max_min_identifier(table_identifier, link_identifier, desired_date, region):
    # Waiting for the box of links as identified by ID
    box_of_links = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, table_identifier)))
    box_of_links = box_of_links.text

    # Converting the table into timestamps
    timestamps = [link.split('@')[1].strip() for link in box_of_links.strip().split('\n')]
    timestamps = [datetime.strptime(time, "%H:%M") for time in timestamps]

    # Calling method to determine which timestamp is closest to 8:00 am EST
    best_index = closest_to_window(timestamps, desired_date) + 1

    best_time = driver.find_element(By.XPATH, f'//*[@id="{table_identifier}"]/a[{best_index}]')
    best_time.click()

    table = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-content"]/div/pre')))
    table = table.text
    table = table.splitlines()

    for line in table:
        if region == line:
            max_min_row = table[table.index(line) + 8]
            max_min_row = max_min_row.split()
            forecasted_high = max_min_row[1]

            return forecasted_high

def closest_to_window(timestamps, desired_date):
    timeshift = 5

    daylight_savings = is_in_daylight_savings(desired_date)

    if daylight_savings == True:
        timeshift = 4
    elif daylight_savings == False:
        timeshift = 5

    shifted_times = []
    for time in timestamps:
        shifted_time = time - timedelta(hours=timeshift)
        shifted_times.append(shifted_time)

    # Define the target time (8:00 AM)
    target_time = datetime.strptime("08:00", "%H:%M")

    # Find the index of the closest time to the target
    closest_index = -1
    min_diff = float('inf')  # Start with a large difference

    for i, time in enumerate(shifted_times):
        if time < target_time:
            diff = abs((target_time - time)).total_seconds()  # Calculate the difference in seconds
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

def is_in_daylight_savings(desired_date) -> bool:
    # Convert the desired_date "date" object into a "datetime" object set at 00:00 (midnight)
    converted_datetime_object = datetime.combine(desired_date, datetime.min.time())

    # Creates a "timezone" object that sets the timezone to New York
    timezone = pytz.timezone("America/New_York")

    # Converts the desired_date datetime object into a datetime object that has the timezone attached
    localized_datetime = timezone.localize(converted_datetime_object)

    # Check if it's in DST
    return bool(localized_datetime.dst())









time_length = int(input("Please enter how many days back you would like the data to go (including today): "))

# Initializing webdriver
driver = webdriver.Chrome()

# Calling method for New York
#historical_forecasted_highs("New York", 'Central Park-New York NY', 'sectPFMOKX', 'PFMOKX', time_length)

# Calling method for Miami
historical_forecasted_highs("Miami", 'Miami-Miami Dade FL','sectPFMMFL', 'PFMMFL', time_length)

# Calling method for Philadelphia
#historical_forecasted_highs("Mount Holly", 'Philadelphia-Philadelphia PA', 'sectPFMPHI', 'PFMPHI', time_length)

# Calling method for Chicago
#historical_forecasted_highs("Chicago", 'Chicago Midway Airport-Cook IL', 'sectPFMLOT', 'PFMLOT', time_length)

# Calling method for Austin
#historical_forecasted_highs("Austin", "Austin Bergstrom-Travis TX ", 'sectPFMEWX', 'PFMEWX', time_length)

# Calling method for Denver
#historical_forecasted_highs("Denver", "Denver Int'l Airport-Denver CO", 'sectPFMBOU', 'PFMBOU', time_length)



