import scrapy

# creating a class that would be storing output links to offers
class Link(scrapy.Item):
    link = scrapy.Field()

# creating a spider class
class LinksSpider(scrapy.Spider):
    name = 'links'
    allowed_domains = ['https://www.olx.pl/']

    # defining a list containing links to pages with offers
    start_urls = ['https://www.olx.pl/nieruchomosci/mieszkania/wynajem/warszawa/?page=' + str(number) for number in range(1, 7)]
    start_urls[0] = 'https://www.olx.pl/nieruchomosci/mieszkania/wynajem/warszawa/'

    # defining a function that gather links to offers
    def parse(self, response):
        # printing response to easier find potential crashes
        print(response)

        # defining xpath
        xpath = '/html/body/div[1]/div[3]/section/div[3]/div/div[1]/table[2]/tbody/tr/td/div/table/tbody/tr[1]/td[2]/div/h3/a/@href'
        selection = response.xpath(xpath)

        # for loop that gather links to offers
        for s in selection:
            l = Link()
            l['link'] = s.get()
            print(l)
            yield l
