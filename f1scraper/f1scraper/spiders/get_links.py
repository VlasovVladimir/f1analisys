#get links from sitemapgp



import scrapy

class get_links(scrapy.Spider):
    name = 'get_links'
    start_urls = ['http://www.statsf1.com/sitemapgp.xml']

    def parse(self, response):
        a = ''
        for line in response.body:
            a = a + chr(line)
        lines = a.split('<loc>')
        print(len(lines))
        with open('f1scraper/links.txt', 'a') as fl:
            for line in lines:
                fl.write(line.split('</loc>')[0] + '\n')