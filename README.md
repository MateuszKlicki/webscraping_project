# webscraping_project

To run soup and selenium scraper you have to download it to your computer and run it through your command line or you can copy-paste it's code to your python interpreter. Additionaly, to run selenium scraper you need to change variable gecko_path to path to geckodriver on your computer.

To run scrapy scraper you have to download both files to your computer. You need to put them into spider folder in scrapy project folder. Then you have to run them by scrapy commmands. At first, you need to run offer_links, because it create a csv file which flats_scrapper needs to run. You can run it by command: scrapy crawl links -o links.csv . Then you can run flats_scrapper by command: scrapy crawl flat -o flats.csv .
