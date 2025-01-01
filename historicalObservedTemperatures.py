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

def historical_observed_highs(location, table_identifier, end_date):
    driver = webdriver.Chrome()
    months = months_between_today_and_date(end_date)

    for i in range(months):
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

        # Identifying the 'year,' 'month,' 'day' dropdowns
        year = Select(driver.find_element(By.NAME, 'year'))
        month = Select(driver.find_element(By.NAME, 'month'))
        day = Select(driver.find_element(By.NAME, 'day'))

        # Get the current date
        today = datetime.today()

        if i == 0:
            # Format the date as 'YYYY Mon DD'
            formatted_date = today.strftime('%Y %b %d')
            formatted_date = formatted_date.split()

            year.select_by_visible_text(formatted_date[0])
            month.select_by_visible_text(formatted_date[1])
            day.select_by_visible_text(formatted_date[2])
        else:
            date = get_date_n_months_before(i-1).split()
            year.select_by_visible_text(date[0])
            month.select_by_visible_text(date[1])
            day.select_by_visible_text('1')

        give_me_button = driver.find_element(By.XPATH, '//*[@id="main-content"]/div/form/div/div[3]/input')
        give_me_button.click()

        report = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="{table_identifier}"]/a')))
        report.click()

        table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-content"]/div/pre'))).text.split('\n')

        daily_highs = []

        for line in table:
            if line == 'DY MAX MIN AVG DEP HDD CDD  WTR  SNW DPTH SPD SPD DIR MIN PSBL S-S WX    SPD DR' and i+1 != months:
                index = table.index(line) + 3

                while table[
                    index] != '================================================================================':
                    daily_high = table[index].split()[1]

                    daily_highs.append(daily_high)
                    index += 1
            elif line == 'DY MAX MIN AVG DEP HDD CDD  WTR  SNW DPTH SPD SPD DIR MIN PSBL S-S WX    SPD DR' and i+1 == months:
                index = table.index(line) + 3

                while table[
                    index] != '================================================================================':
                    day_date = table[index].split()[0]

                    if int(day_date) >= int(end_date.split()[2]):
                        daily_high = table[index].split()[1]
                        daily_highs.append(daily_high)

                    index += 1

        for high in reversed(daily_highs):
            print(high)

def months_between_today_and_date(date_str):
    # Parse the input date string
    input_date = datetime.strptime(date_str, '%Y %b %d')
    today = datetime.today()

    # Calculate the difference in months
    months_difference = (today.year - input_date.year) * 12 + (today.month - input_date.month)

    return abs(months_difference) + 1

def get_date_n_months_before(n):
    # Get today's date
    today = datetime.today()

    # Calculate the target year and month
    year = today.year
    month = today.month - n

    # Adjust year and month if month goes below 1
    while month < 1:
        month += 12
        year -= 1

    # Calculate the day, ensuring it doesn't exceed the last day of the new month
    day = min(today.day,
              [31, 29 if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30,
               31, 30, 31][month - 1])

    # Create the new date
    new_date = datetime(year, month, day)
    # Format the new date as 'YYYY Mon DD'
    return new_date.strftime('%Y %b')



end_date = input("Enter the end date in the format '2024 Dec 24' (inclusive): ")

# Calling method for New York
#historical_observed_highs("New York", 'sectCF6NYC', end_date)

# Calling method for Miami
#historical_observed_highs("Miami", 'sectCF6MIA', end_date)

# Calling method for Philadelphia
#historical_observed_highs("Mount Holly", 'sectCF6PHL', end_date)

# Calling method for Denver
#historical_observed_highs('Denver', 'sectCF6DEN', end_date)

# Calling method for Chicago
#historical_observed_highs('Chicago', 'sectCF6MDW', end_date)

# Calling method for Austin
#historical_observed_highs('Austin', 'sectCF6AUS', end_date)

