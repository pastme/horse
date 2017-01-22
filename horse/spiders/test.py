import scrapy


class QuotesSpider(scrapy.Spider):
    name = "races"
    start_urls = [
        'https://www.betbright.com/horse-racing/today',
    ]

    def parse_partisipants(self, response):
        for row in response.css('.horse-datafields'):
            race = response.meta['race']
            race['partisipants'].append({
                'part_id': row.css('div.cloth-number::text').extract_first(),
                'horse_name': row.css('div.horse-information-name::text').extract_first(),
                'odds': row.xpath('./li/a[@class="bet_now_btn"]/text()').extract_first()
            })
        return race

    def parse(self, response):
        for row in response.xpath('//table[@class="racing"]/tr'):
            name = row.css('td a.blue_link2_sports.country_flag::text').extract_first()
            if not name: continue
            races = row.xpath('./td/a[@class="event_time "]')
            for race in races:
                time = race.xpath('./text()').extract_first()
                link = race.xpath('./@href').extract_first()
                uniq_id = link.split('/')[-1]
                race = {
                    'name': name,
                    'time': time,
                    'link': link,
                    'uniq_id': uniq_id,
                    'partisipants':[]
                    }
                get_partisipants = scrapy.Request(link, callback=self.parse_partisipants)
                get_partisipants.meta['race'] = race
                yield get_partisipants