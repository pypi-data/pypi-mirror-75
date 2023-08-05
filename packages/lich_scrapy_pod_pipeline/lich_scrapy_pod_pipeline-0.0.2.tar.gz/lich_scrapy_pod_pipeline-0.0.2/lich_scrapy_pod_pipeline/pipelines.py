# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from typing import Optional
import logging

from scrapy.utils.serialize import ScrapyJSONEncoder
from scrapy.utils.python import to_bytes
from scrapy import signals

from .sender import HttpSender
from .utils import as_deferred

class PodPipeline:
    def __init__(self, crawler):
        self.sender = HttpSender()
        self.encoder = ScrapyJSONEncoder()
        self.logger = logging.getLogger(self.__class__.__name__)
        crawler.signals.connect(self.spider_closed, signals.spider_closed)
    def _get_request(self,urls,depth):
        d=None
        try:
            d=int(depth)
        except Exception as e:
            d=-1
            self.logger.error("depth illegal %s",e)
        return {'URLS':list(urls),
                'meta':{'depth':d+1}
                }

    def _get_extracted_links(self,item)->Optional[bytes]:
        reqs=None
        if "meta" in item and isinstance(item["meta"], dict) and "extractor.links" in item["meta"]:
            links = item["meta"]["extractor.links"]
            depth = item["meta"]["depth"]
            s = set()
            for value in links.values():
                for link in value:
                    s.add(link)
            if len(s)>0:
                reqs=to_bytes(self.encoder.encode(self._get_request(s,depth)))
        return reqs


    def _get_addr(self,item)->Optional[str]:
        addr=None
        if "meta" in item and isinstance(item["meta"], dict):
            meta = item["meta"]
            addr = meta.get("pod.addr", None)
        return addr
    def process_item(self, item, spider):
        addr=self._get_addr(item)
        requests=self._get_extracted_links(item)
        d = as_deferred(self.sender.send(addr,requests))
        d.addBoth(lambda _: item)
        return d

    def spider_closed(self, spider):
        return self.sender.close()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)
