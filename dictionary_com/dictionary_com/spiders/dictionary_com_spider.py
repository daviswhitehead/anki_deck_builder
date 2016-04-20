import scrapy
from dictionary_com.items import DictionaryComItem


class DmozSpider(scrapy.Spider):
    name = 'dictionary_com'
    allowed_domains = ['dictionry.com']
    start_urls = [
        'http://www.dictionary.com/browse/austere'
    ]

    def parse(self, response):
        item = DictionaryComItem()
        item['word'] = response.xpath('//h1/span/text()').extract()[0]
        item['syllables'] = response.xpath('//h1/span/@data-syllable').extract()[0]
        item['pronunciation'] = response.xpath('//*[@id="source-luna"]/div[1]/section/header/div[2]/div[1]/span[1]/text()').extract()[0] + response.xpath('//*[@id="source-luna"]/div[1]/section/header/div[2]/div[1]/span[1]/span/text()').extract()[0] + response.xpath('//*[@id="source-luna"]/div[1]/section/header/div[2]/div[1]/span[1]/text()').extract()[1]
        item['ipa'] = response.xpath('//*[@id="source-luna"]/div[1]/section/header/div[2]/div[1]/span[2]/text()').extract()[0]
        for i in response.xpath('//*[@id="source-luna"]/div[1]/section/div[2]/div[1]'):
            item['functional_label'] = {}
            item['functional_label'][ = {}
            item['functional_label'] = {}

        yield item
