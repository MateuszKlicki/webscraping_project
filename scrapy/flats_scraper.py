import scrapy

# setting up a boolean parameter that if it is True, it will limit the number of pages to scrap to 100
limiter = True

# creating a class that would be storing output data
class Flat(scrapy.Item):
    price = scrapy.Field()
    floor = scrapy.Field()
    furnishings = scrapy.Field()
    building_type = scrapy.Field()
    area = scrapy.Field() 
    rooms = scrapy.Field()
    rent = scrapy.Field()

# creating a spider class
class FlatsSpider(scrapy.Spider):
    name = 'flat'
    allowed_domains = ['https://www.olx.pl/']
    
    # trying to read links to offers from csv file. If error is raised urls list is empty.
    try:
        with open("links.csv", "rt") as f:
            urls = [url.strip() for url in f.readlines()][1:]
    except:
        urls = []
    
    # defining a list that contain start urls
    start_urls = []

    # for loop to remove links to otodom.pl, because some offers on olx.pl have links to otodom.pl offer not olx.pl offer
    # if link is to olx.pl offer, append to the start_urls list
    for url in urls:
        if 'olx' in url:
            start_urls.append(url)

    # checking if limiter is True. If so, the list containing start urls is limited to 100 links
    if limiter:
        start_urls = start_urls[:100]

    # defining a function that gather data about flats
    def parse(self, response):
        # creating a Flat object
        fl = Flat()

        # defining a xpaths to the variables
        price_xpath = '/html/body/div[1]/div[1]/div[3]/div[2]/div[1]/div[2]/div[3]/h3/text()'
        floor_xpath = '/html/body/div[1]/div[1]/div[3]/div[2]/div[1]/div[2]/ul/li[2]/p/text()'
        furnishings_xpath = '/html/body/div[1]/div[1]/div[3]/div[2]/div[1]/div[2]/ul/li[3]/p/text()'
        building_type_xpath = '/html/body/div[1]/div[1]/div[3]/div[2]/div[1]/div[2]/ul/li[4]/p/text()'
        area_xpath = '/html/body/div[1]/div[1]/div[3]/div[2]/div[1]/div[2]/ul/li[5]/p/text()' 
        rooms_xpath = '/html/body/div[1]/div[1]/div[3]/div[2]/div[1]/div[2]/ul/li[6]/p/text()'
        rent_xpath = '/html/body/div[1]/div[1]/div[3]/div[2]/div[1]/div[2]/ul/li[7]/p/text()'

        # gathering data
        fl['price'] = response.xpath(price_xpath).getall()
        fl['floor'] = response.xpath(floor_xpath).getall()
        fl['furnishings'] = response.xpath(furnishings_xpath).getall()
        fl['building_type'] = response.xpath(building_type_xpath).getall()
        fl['area'] = response.xpath(area_xpath).getall()
        fl['rooms'] = response.xpath(rooms_xpath).getall()
        fl['rent'] = response.xpath(rent_xpath).getall()
        
        yield fl

# scrapy crawl flat -o flat.csv