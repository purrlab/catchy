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
scrapy crawl pmlr -a start_url=202,162,139,119,97,80,70,48,37,32,28
143 and 121 being the volume number of the venue
"""

class PMLRSpider(scrapy.Spider):
    name = "pmlr"

    def __init__(self, start_url, **kwargs):

        """
        Instantiate the spider.
        @param kwargs: keyword arguments
        """
        # the base url common to all urls; just a convenience variable so that we do not have to repeat it
        self.base_url = 'https://proceedings.mlr.press/v'

        # flag to signal if the crawl is in persistent mode
        self.is_persistent = False
        self.start_url = start_url.split(',')
        self.years = [2023,2013]
        # self.years = [2023,2022,2021,2020,2019,2018,2017,2016,2015,2014,2013]
        super().__init__(**kwargs)

    def start_requests(self):
        urls = self.start_url
        for i,volume_id in enumerate(urls):

            yield scrapy.Request(url=f"https://proceedings.mlr.press/v{volume_id}",meta={"year":self.years[i]}, callback=self.parse)

    def parse(self, response):

        for article in response.xpath('/html/body/main/div/div[*]'):
            try:
                yield Request(
                    url=article.xpath('p[3]/a[2]/@href').get(),
                    meta={
                        "title": article.xpath('p[1]/text()').get(),
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
            os.makedirs(f"../../data/pdfs/ICML{year}/", exist_ok=True)

            self.logger.info('Saving PDF %s', title)
            with open(f"../../data/pdfs/ICML{year}/{title}", 'wb') as f:
                f.write(response.body)
        except Exception as e:
            print(e)