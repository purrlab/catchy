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
scrapy crawl cvpr
"""

class CVPRSpider(scrapy.Spider):
    name = "cvpr"

    def __init__(self, **kwargs):

        """
        Instantiate the spider.
        @param kwargs: keyword arguments
        """        
        # flag to signal if the crawl is in persistent mode
        self.is_persistent = False
        self.start_url = [
            "https://openaccess.thecvf.com/CVPR2013",
            "https://openaccess.thecvf.com/CVPR2014",
            "https://openaccess.thecvf.com/CVPR2015",
            "https://openaccess.thecvf.com/CVPR2016",
            "https://openaccess.thecvf.com/CVPR2017",
            "https://openaccess.thecvf.com/CVPR2018?day=2018-06-19",
            "https://openaccess.thecvf.com/CVPR2018?day=2018-06-20",
            "https://openaccess.thecvf.com/CVPR2018?day=2018-06-21",
            "https://openaccess.thecvf.com/CVPR2019?day=2019-06-18",
            "https://openaccess.thecvf.com/CVPR2019?day=2019-06-19",
            "https://openaccess.thecvf.com/CVPR2019?day=2019-06-20",
            "https://openaccess.thecvf.com/CVPR2020?day=2020-06-16",
            "https://openaccess.thecvf.com/CVPR2020?day=2020-06-17",
            "https://openaccess.thecvf.com/CVPR2020?day=2020-06-18",
            "https://openaccess.thecvf.com/CVPR2021?day=all",
            "https://openaccess.thecvf.com/CVPR2022?day=all",
            "https://openaccess.thecvf.com/CVPR2023?day=all"
        ]
        super().__init__(**kwargs)

    def start_requests(self):
        urls = self.start_url
        for url in urls:
            venue = url.split("?")[0].split("/")[-1]
            yield scrapy.Request(url=url, meta={"venue":venue},callback=self.parse)

    def parse(self, response):

        for article in response.xpath('.//dt[*]'):
            try:
                url = response.url.removesuffix(f"/{response.meta['venue']}") + "/" + article.xpath('a/@href').get().replace("/html/","/papers/").replace(".html",".pdf")
                yield Request(
                    url=url,
                    meta={
                        "title": article.xpath('a/text()').get(),
                        "venue": response.meta['venue']
                        },
                    callback=self.save_pdf
                )
            except Exception as e:
                print(e)

    def save_pdf(self, response):
        try:
            title = response.meta['title'].replace("/"," ").removesuffix(".")+".pdf"
            venue = response.meta['venue']
            os.makedirs(f"../../../data/pdfs/{venue}/", exist_ok=True)
            self.logger.info('Saving PDF %s', title)
            save_path = f"../../../data/pdfs/{venue}/{title}"
            with open(save_path, 'wb') as f:
                f.write(response.body)
        except Exception as e:
            print(e)