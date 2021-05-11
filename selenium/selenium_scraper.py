# importing necessary libraries
from selenium import webdriver
import time
import getpass
import datetime
import pandas as pd

# setting up a boolean parameter that if it is True, it will limit the number of pages to scrap to 100
limiter = True

# defining path to geckodriver
gecko_path = '/usr/local/bin/geckodriver'

# defining whether the browser should be run visible. If it's False, browser will be run visible.
options = webdriver.firefox.options.Options()
options.headless = True
driver = webdriver.Firefox(options = options, executable_path = gecko_path)

# creating a list containing links to pages with offers
page_links = ['https://www.olx.pl/nieruchomosci/mieszkania/wynajem/warszawa/?page=' + str(number) for number in range(1, 25)]
page_links[0] = 'https://www.olx.pl/nieruchomosci/mieszkania/wynajem/warszawa/'

# creating a list containing links to offers
offer_links = []

# for loop to get links to offers
for page_link in page_links:
    driver.get(page_link)

    # finding links to offers 
    elements = driver.find_elements_by_xpath('/html/body/div[1]/div[3]/section/div[3]/div/div[1]/table[2]/tbody/tr/td/div/table/tbody/tr[1]/td[2]/div/h3/a')

    # for loop to get links to offers and remove links to otodom.pl, because some offers on olx.pl have links to otodom.pl offer, not to olx.pl offer 
    for element in elements:
        link = element.get_attribute('href')
        if 'olx' in link:
            offer_links.append(link)

    # checking if the limiter is True and if number of links to scrap is bigger than 100. If so, limit offer links to 100 and break the for loop
    if limiter == True and len(offer_links) > 100:
        offer_links = offer_links[:100]
        break

    # time break to not overload server
    time.sleep(2)

# creating a dataset to store scraped data
flat_dataset = pd.DataFrame({'Price':[], 'Floor':[], 'Furnishings':[], 'Type of building': [], 'Area':[], 'Number of rooms':[],'Additional rent':[]})

# for loop to get data from offer links
for link in offer_links:
    driver.get(link)

    # printing actual link to inspect if code work properly
    print(link)

    # time break, because because the page (at least on my link) is loading too slow and scraper is downloading data for the previous offer
    # which creates duplicates instead of downloading data for the next offer
    time.sleep(3)

    # Try to get a variables values, if error will raise then the variable is equal to nothing
    try:
        price = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[3]/div[2]/div[1]/div[2]/div[3]/h3').text
    except:
        price = ''
    try:
        floor = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[3]/div[2]/div[1]/div[2]/ul/li[2]/p').text
    except:
        floor = ''
    try:
        furnishings = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[3]/div[2]/div[1]/div[2]/ul/li[3]/p').text
    except:
        furnishings = ''
    try:
        building = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[3]/div[2]/div[1]/div[2]/ul/li[4]/p').text
    except:
        building = ''
    try:
        area = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[3]/div[2]/div[1]/div[2]/ul/li[5]/p').text
    except:
        area = ''
    try: 
        rooms = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[3]/div[2]/div[1]/div[2]/ul/li[6]/p').text
    except:
        rooms = ''
    try:
        rent = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[3]/div[2]/div[1]/div[2]/ul/li[7]/p').text
    except:
        rent = ''

    # store all scraped information into flat variable and append to the flat dataset
    # scraped variable contains its name so I transmit to the flat variable only parts of scraped variables. For example, variable floor contain string: 'Poziom: 1'. 
    # by passing the string from index 8, we only have a number in the dataset etc.
    flat = {'Price':price, 'Floor':floor[8:], 'Furnishings':furnishings[12:], 'Type of building': building[17:], 'Area':area[14:], 'Number of rooms':rooms[14:],'Additional rent':rent[20:]}
    flat_dataset = flat_dataset.append(flat, ignore_index = True)

    
    # print scraped data about actual flat to inspect if code work properly
    print(flat)

# printing a final dataset
print(flat_dataset)

# saving a dataframe into csv file
flat_dataset.to_csv('flats_selenium.csv', index = False)

driver.quit()
