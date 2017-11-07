#get quali results from tables
# 2016;bresil;22;Felipe NASR;Sauber;Ferrari;1'13''681;2.945;210.535;104.163
# year; gp$ number of result; name; team; engine; time; gap; avg speed; per cent

import scrapy
import re

class get_quali(scrapy.Spider):
    name = 'get_quali'
    my_urls = []
    with open('f1scraper/links.txt', 'r') as fl:
        for line in fl:
            line1 = line.split('/fr/')
            line = '/en/'.join(line1)
            my_urls.append(line[:-6]+ '/qualification.aspx')
    start_urls = my_urls
    warnings = 0

    def parse(self, response):
        country = response.url.split('/')[-2]
        year = response.url.split('/')[-3]
        #get rows in html
        rows = response.xpath('//*[@id="ctl00_CPH_Main_GV_Stats"]/tbody/tr')
        for row in rows:
            line_ext = row.extract()
            line_ext_sp = re.findall(r'>["\'. \w\d]*<', line_ext)
            #split rows
            results = [a[1:-1] for a in line_ext_sp if not a=='><']
            #make every row equal
            if len(results)==6 and results[0] == '1':
                results.insert(-1, '0.0')
                results.append('100.0')
            if len(results)==7 and results[0] == '1':
                results.append('100.0')
            if not len(results)==8:
                while not len(results)==8:
                    results.append('nan')
            if not len(results)==8:
                print('')
                print('WARNING!')
                print('')
                self.warnings +=1
            results = [year, country] + results
            with open('quali.txt', 'a') as file:
                file.write(';'.join(list(results))+ '\n')

        if self.warnings > 0:
            print('Warnings: ' + str(self.warnings))

