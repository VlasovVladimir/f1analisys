# get race results from table
# 2017;etats-unis;1;44;Lewis HAMILTON;Mercedes;Mercedes;56;1h 33m 50.991s; 25;finished
# 2016;etats-unis;ab;33;Max VERSTAPPEN;Red Bull;TAG Heuer;28;nan;0;Gearbox
# year; gp; place/tag; № of car; name; team; engine; laps completed; total time ('nan'
#                                                                           if dont finish, 'few laps' if gap to winner
#                                                                           is more than lap); cause of retirement

import scrapy
import re

class get_race(scrapy.Spider):
    name = 'get_race'
    my_urls = []
    with open('f1scraper/links.txt', 'r') as fl:
        for line in fl:
            line1 = line.split('/fr/')
            line = '/en/'.join(line1)
            my_urls.append(line[:-6]+ '/classement.aspx')
            print(line[:-6]+ '/classement.aspx')
    start_urls = my_urls
    warnings = 0
    warnings_arr = []

    def parse(self, response):
        country = response.url.split('/')[-2]
        year = response.url.split('/')[-3]
        rows = response.xpath('//*[@id="ctl00_CPH_Main_GV_Stats"]/tbody/tr')
        for row in rows:
            line_ext = row.extract()
            line_ext_sp = re.findall(r'>?["\'. \w\d]*<', line_ext)
            results1 = [a[:-1] for a in line_ext_sp if not (a=='><' or a[1:-1]=='')]
            results = [a[1:] if a[0]=='>' else a for a in results1]

            if len(results)>2:
                results = [a for a in results if not (a=='.00' or a == r'*penalty')]
                if len(results[0])>3:
                    results.insert(0, 'ch')
                flag = False
                try:
                    float(results[0])
                    flag = True
                except ValueError:
                    flag = False
                if flag:

                    flags = [False, False, False]
                    try:
                        float(results[-1])
                        flags[0] = True
                    except ValueError:
                        flags[0] = False
                    try:
                        int(results[-2])
                        flags[1] = True
                    except ValueError:
                        flags[1] = False
                    try:
                        int(results[-3])
                        flags[2] = True
                    except ValueError:
                        flags[2] = False

                    if flags[0] and (not flags[1]) and (not flags[2]):
                        results = results + ['few laps', '0']
                    elif flags[0] and flags[1] and (not flags[2]):
                        results.insert(-1, 'few laps')
                    elif not flags[0]:
                        results.append('0')

                    results = results + ['finished']
                else:
                    if results[0]=='ab':
                        try:
                            int(results[-2])
                            while len(results) < 8:
                                results.append('nan')
                            results.append('not finished')
                        except ValueError:
                            results.append(results[-2])
                            results[-3] = 'nan'
                            results[-2] = '0'

                    elif results[0]=='dsq':
                        results.append('disqualificated')
                    else:
                        results = results[:5]
                        while len(results) < 8:
                            results.append('nan')
                        results.append('not started')
                results = [year, country] + results
                print(results)
                if not len(results)==11:
                    self.warnings_arr.append(results)
                    self.warnings+=1
                else:
                    with open('race.txt', 'a') as file:
                        file.write(';'.join(list(results))+ '\n')

        if self.warnings > 0:
            print('Warnings: ' + str(self.warnings))
            print(self.warnings_arr)