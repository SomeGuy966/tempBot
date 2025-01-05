from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime, timedelta
import gspread
from google.oauth2.service_account import Credentials

def time_of_temperature_high_scraper(location, link_identifier, start_date, end_date):
    # Parse the strings into datetime objects
    date_format = "%Y %b %d"  # Matches format '2024 Dec 23'

    formatted_start_date = datetime.strptime(start_date, date_format)
    formatted_end_date = datetime.strptime(end_date, date_format)

    desired_date = formatted_start_date

    # Calculate the difference in days (inclusive)
    time_length = abs((formatted_end_date - formatted_start_date).days) + 1


    for i in range(time_length):
        driver.get('https://mesonet.agron.iastate.edu/wx/afos/list.phtml')

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

        link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{link_identifier}"]/a[1]')))
        link.click()

        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main-content"]/div/pre')))
        table = table.text

        lines = table.splitlines()



        for line in lines:
            if 'MAXIMUM' in line:
                data = line.split()
                time = str(data[2] + " " + data[3])

                if location == 'Denver' or location == 'New York':
                    print(time_converter(time))
                else:
                    print(time)

                break

        desired_date = desired_date - timedelta(days=(1))

def time_converter(time):
    if 'MM' in time:
        return time

    # Extract the period (AM/PM) and the numeric part
    period = time[-2:]  # Extract "AM" or "PM"
    numeric_part = time[:-3]  # Extract the numeric part (e.g., "426" or "1126")

    # Ensure the numeric part has at least three digits (to handle cases like "426")
    numeric_part = numeric_part.zfill(3)

    # Extract hour and minute
    if len(numeric_part) == 3:
        hour = int(numeric_part[0])  # Single digit for hour
        minute = int(numeric_part[1:])  # Remaining two digits for minute
    elif len(numeric_part) == 4:
        hour = int(numeric_part[:2])  # First two digits for hour
        minute = int(numeric_part[2:])  # Last two digits for minute
    else:
        raise ValueError("Invalid time format")

    # Format as "H:MM AM/PM"
    formatted_time = f"{hour}:{minute:02d} {period}"
    return formatted_time


start_date = str(input('Please enter the inclusive ending date in the following format (2024 Dec 31): '))
end_date = str(input('Please enter the inclusive starting date in the following format (2024 Jan 1): '))

driver = webdriver.Chrome()

# Calling method for New York
#time_of_temperature_high_scraper('New York', 'sectCLINYC', start_date, end_date)

# Calling method for Miami
#time_of_temperature_high_scraper('Miami', 'sectCLIMIA', start_date, end_date)

# Calling method for Austin
#time_of_temperature_high_scraper('Austin', 'sectCLIAUS', start_date, end_date)

# Calling method for Houston
#time_of_temperature_high_scraper('Houston', 'sectCLIHOU', start_date, end_date)

# Calling method for Philadelphia
#time_of_temperature_high_scraper('Mount Holly', 'sectCLIPHL', start_date, end_date)

# Calling method for Chicago
time_of_temperature_high_scraper('Chicago', 'sectCLIMDW', start_date, end_date)
