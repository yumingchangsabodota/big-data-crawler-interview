import scrapy
import json

class YahooTWSpider(scrapy.Spider):
    name = 'line_today'
    base_url = "https://today.line.me/tw/v2/tab/{}"
    areas = ['top','recommendation','entertainment',
            'domestic','life','global','subscription',
            'movie','music','NBA','CPBL','sports','finance',
            'health','fun','relationship','horoscope','parenting',
            'food','travel','fashion','tech','auto','living',
            'ACG','pet','shopping']

    def start_requests(self):

        for area in self.areas:
            url = self.base_url.format(area) #將事先存好的新聞類別與新聞root網址結合
            yield scrapy.Request(url, meta={'filename':area})

    def parse(self, response):
 
        path = "//div[@class='listModule']/a"

        extracted = []
        #loops 擷取到的新聞並抓取需要內容
        for news in response.xpath(path):
            print(news.extract())
            title = news.xpath(".//div[@class='articleCard-content']/span/text()").get()

            n = {'title':title}
            extracted.append(n)
            with open(response.meta['filename']+".json",'w') as f:
                data = json.dumps(extracted)
                f.write(data)
            f.close()
            with open(response.meta['filename']+".txt",'w') as f:
                f.write(str(extracted))
            f.close()
            yield n