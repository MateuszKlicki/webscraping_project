# importing necessary libraries
from urllib import request as re
from bs4 import BeautifulSoup as BS
import pandas as pd
import time

# setting up a boolean parameter that if it is True, it will limit the number of pages to scrap to 100
limiter = True

# creating a list containing links to pages with offers
page_links = ['https://www.olx.pl/nieruchomosci/mieszkania/wynajem/warszawa/?page=' + str(number) for number in range(1, 26)]
page_links[0] = 'https://www.olx.pl/nieruchomosci/mieszkania/wynajem/warszawa/'

# creating a list containing links to offers
offer_links = []

# for loop to get links to offers
for link in page_links: 
    html = re.urlopen(link)
    bs = BS(html.read(), 'html.parser')

    # a help list and for loop to extract links to offer from page 
    help_list = bs.findAll('a', {'class':'marginright5 link linkWithHash detailsLink'})
    for element in help_list:
        offer_links.append(element.get('href'))
    
    # checking if the limiter is True and if number of links to scrap is bigger than 100. If so, limit offer links to 100 and break the for loop
    if limiter == True and len(offer_links) > 100:
        offer_links = offer_links[:100]
        break

    # time break to not overload server
    time.sleep(2)

# for loop to remove links to otodom.pl, because some offers on olx.pl have links to otodom.pl offer not olx.pl offer 
for link in offer_links:
    if 'otodom' in link:
        offer_links.remove(link)

# creating a dataset to store scraped data
flat_dataset = pd.DataFrame({'Price':[], 'Floor':[], 'Furnishings':[], 'Type of building': [], 'Area':[], 'Number of rooms':[],'Additional rent':[]})

# for loop to get data from offer links
for offer_link in offer_links:
    html = re.urlopen(offer_link)
    bs = BS(html.read(), 'html.parser')

    # print actual link to inspect if code work properly
    print(offer_link)

    # Try to get a variables values, if error will raise then the variable is equal to nothing
    try:
        price = bs.find('h3', {'class':'css-8kqr5l-Text eu5v0x0'}).get_text()
    except:
        price = ''
    
    # setting a variable which help to navigate through variables indexes
    i = 1
    
    try:
        floor = bs.find('ul', {'class':'css-sfcl1s'}).find_all('li')[i].get_text()
    except:
        floor = ''

    # checking if the word 'Poziom' is in the variable floor. If so, set variable i to 1, otherwise set variable i to 0
    # in some offers there isn't information about floor. In this case, indexes the indexes go down by 1 and the scraper takes the wrong information
    # this condition prevents this from happening
    if 'Poziom' in floor:
        i = 1
    else:
        i = 0
    
    try:
        furnishings = bs.find('ul', {'class':'css-sfcl1s'}).find_all('li')[i+1].get_text()
    except:
        furnishings = ''
    try:
        building_type = bs.find('ul', {'class':'css-sfcl1s'}).find_all('li')[i+2].get_text()
    except:
        building_type = ''
    try:
        area = bs.find('ul', {'class':'css-sfcl1s'}).find_all('li')[i+3].get_text()
    except:
        area = ''
    try:
        rooms = bs.find('ul', {'class':'css-sfcl1s'}).find_all('li')[i+4].get_text()
    except:
        rooms = ''
    try:
        rent = bs.find('ul', {'class':'css-sfcl1s'}).find_all('li')[i+5].get_text()
    except:
        rent = ''

    # store all scraped information into flat variable and append to the flat dataset
    # scraped variable contains its name so I transmit to the flat variable only parts of scraped variables. For example, variable floor contain string: 'Poziom: 1'. 
    # by passing the string from index 8, we only have a number in the dataset etc.
    flat = {'Price':price, 'Floor':floor[8:], 'Furnishings':furnishings[12:], 'Type of building': building_type[17:], 'Area':area[14:], 'Number of rooms':rooms[14:],'Additional rent':rent[20:]}
    flat_dataset = flat_dataset.append(flat, ignore_index = True)

    # print scraped data about actual flat to inspect if code work properly
    print(flat)

    # time break to not overload server
    time.sleep(2)

# printing a final dataset
print(flat_dataset)

# saving a dataframe into csv file
flat_dataset.to_csv('flats.csv', index = False)
