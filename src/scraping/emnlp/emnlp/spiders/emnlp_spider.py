# import urlparse
import scrapy

from scrapy.http import Request
import urllib
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from pydispatch import dispatcher
import os
"""
Exemple of usage
scrapy crawl emnlp
"""

class EMNLPSpider(scrapy.Spider):
    name = "emnlp"

    def __init__(self, **kwargs):

        """
        Instantiate the spider.
        @param kwargs: keyword arguments
        """        
        # flag to signal if the crawl is in persistent mode
        self.is_persistent = False
        self.start_url = [
            "https://aclanthology.org/volumes/2023.emnlp-main/",
            "https://aclanthology.org/volumes/2022.emnlp-main/",
            "https://aclanthology.org/volumes/2021.emnlp-main/",
            "https://aclanthology.org/volumes/2020.emnlp-main/",
            "https://aclanthology.org/volumes/D19-1/",
            "https://aclanthology.org/volumes/D18-1/",
            "https://aclanthology.org/volumes/D17-1/",
            "https://aclanthology.org/volumes/D16-1/",
            "https://aclanthology.org/volumes/D15-1/",
            "https://aclanthology.org/volumes/D14-1/",
            "https://aclanthology.org/volumes/D13-1/",
        ]

        self.years = [2023,2022,2021,2020,2019,2018,2017,2016,2015,2014,2013]
        super().__init__(**kwargs)

    def start_requests(self):
        urls = self.start_url
        for i,url in enumerate(urls):
            yield scrapy.Request(url=url,meta={"year":self.years[i]},callback=self.parse)

    def parse(self, response):
        for article in response.xpath(".//p[@class='d-sm-flex align-items-stretch']"):
            try:
                title = ""
                for title_part in article.xpath(".//strong/a/descendant-or-self::*/text()"):
                    title += title_part.get()                
                url = article.xpath(".//a/@href")[0].get()

                yield Request(
                    url=url,
                    meta={
                        "title": title,
                        "year": response.meta['year']
                        },
                    callback=self.save_pdf
                )
            except Exception as e:
                print(e)

    def save_pdf(self, response):
        try:
            title = response.meta['title'].replace("/"," ").removesuffix(".")+".pdf"
            year = response.meta['year']
            os.makedirs(f"../../../data/pdfs/EMNLP{year}/", exist_ok=True)
            self.logger.info('Saving PDF %s', title)
            save_path = f"../../../data/pdfs/EMNLP{year}/{title}"
            with open(save_path, 'wb') as f:
                f.write(response.body)
        except Exception as e:
            print(e)