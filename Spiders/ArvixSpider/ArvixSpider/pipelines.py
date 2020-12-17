# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from kafka import KafkaProducer
import json
class ArvixspiderPipeline:

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            topic=crawler.settings.get('KAFKA_TOPIC'),
            kafka_server=crawler.settings.get('KAFKA_BOOTSTRAP_SERVER')
        )

    def __init__(self, topic, kafka_server):
        self.topic = topic
        self.kafka_server = kafka_server
        # self.producer = None
        self.producer = KafkaProducer(bootstrap_servers=kafka_server)
        
    
    def process_item(self, item, spider):
        msg = json.dumps(dict(item)).encode(encoding='utf-8')
        self.producer.send(self.topic, msg)
        return item

    def close_spider(self, spider):
        if self.producer != None:
            self.producer.close()
        
