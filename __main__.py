import urllib
from itertools import count
import pandas as pd
from bs4 import BeautifulSoup
import xml.etree.ElementTree as et
import collection.crawler as cw
from collection.data_dict import sido_dict, gungu_dict

RESULT_DIRECTORY = '__result__/crawling'


def crawling_pelicana():
    results = []

    for page in count(start=1):
        url = 'http://www.pelicana.co.kr/store/stroe_search.html?branch_name=&gu=&si=&page=%d' % page
        html = cw.crawling(url=url)

        bs = BeautifulSoup(html, 'html.parser')

        tag_table = bs.find('table', attrs={'class': 'table mt20'})
        tag_tbody = tag_table.find('tbody')
        tags_tr = tag_tbody.findAll('tr')

        # 끝 검출
        if len(tags_tr) == 0:
            break

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)

            name = strings[1]
            address = strings[3]
            sidogu = address.split()[:2]

            results.append((name, address) + tuple(sidogu)) # 튜플로 만듬 데이터 수정 불가능하게 하기 위해 튜플

    # store
    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gungu'])

    table['sido'] = table.sido.apply(lambda v: sido_dict.get(v, v))
    table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))
    table.to_csv('{0}/pelicana_table.csv'.format(RESULT_DIRECTORY), encoding='utf-8', mode='w', index=True)


# proc_nene
def proc_nene(xml):
    root = et.fromstring(xml)
    results = []

    for el in root.findall('item'):
        name = el.findtext('aname1')
        sido = el.findtext('aname2')
        gungu = el.findtext('aname3')
        address = el.findtext('aname5')

        results.append((name, address, sido, gungu))

    return results


def store_nene(data):
    table = pd.DataFrame(data, columns=['name', 'address', 'sido', 'gungu'])

    table['sido'] = table.sido.apply(lambda v: sido_dict.get(v, v))
    table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))
    table.to_csv('{0}/nene.csv'.format(RESULT_DIRECTORY), encoding='utf-8', mode='w', index=True)


def crawling_kyochon():
    results = []

    while True:
        for sido1 in range(1, 18):
            for sido2 in count(start=1):
                url = 'http://www.kyochon.com/shop/domestic.asp?sido1=%d&sido2=%d' % (sido1, sido2)
                html = cw.crawling(url=url)
                if html == None:
                    break

                bs = BeautifulSoup(html, 'html.parser')

                # tag_table = bs.find('div', attrs={'class': 'shopSchList'})
                # tag_tbody = tag_table.find('ul', attrs={'class': 'list'})
                # tags_tr = tag_tbody.findAll('li')
                tag_table = bs.find('ul', attrs={'class': 'list'})
                tags_tr = tag_table.findAll('li')

                for tag_tr in tags_tr:
                    strings = list(tag_tr.strings)
                    if '검색결과가 없습니다.' not in strings:
                        name = strings[3]

                        # address = strings[5].replace('\t', '').replace('\r', '').replace('\n', '')
                        temp_address = strings[5]
                        print(temp_address)
                        address = ','.join(temp_address.split()).replace(',', ' ')

                        sido = address.split()[:2]

                        results.append((name, address) + tuple(sido))

            # store
            table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gungu'])

            table['sido'] = table.sido.apply(lambda v: sido_dict.get(v, v))
            table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))
            table.to_csv('{0}/kyochon_table.csv'.format(RESULT_DIRECTORY), encoding='utf-8', mode='w', index=True)

        if sido1 == 17:
            break


if __name__ == '__main__':
    # pelicana
    # crawling_pelicana()

    # nene
    # cw.crawling(url='http://nenechicken.com/subpage/where_list.asp?target_step2=%s&proc_type=step1&target_step1=%s'
    #             % (urllib.parse.quote('전체'), urllib.parse.quote('전체')),
    #             proc=proc_nene,
    #             store=store_nene)

    # kyochon
    crawling_kyochon()