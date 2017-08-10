# -*- coding: utf-8-*-
import sys, requests
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool
from progressbar import ProgressBar
global bar
class HtmlParser:
    def __init__(self,url='http://mebook.cc/'):
        self.session = requests.session()
        self.entry_url = url
        self.datas = []
        self.pages= []
        self.bar = ProgressBar()

    def get_latest_page(self):
        # html = BeautifulSoup(self.session.get(self.entry_url).content,'html.parser')
        # page = html.find_all('a',title=u'最末页')[0].string
        page = '431'
        print('total '+page+' pages')
        return int(page)

    def parse(self, pages=None):
        self.bar = ProgressBar(total=len(pages))
        pool = ThreadPool(64)
        pool.map(self.parse_page, pages)
        pool.close()
        pool.join()

    def parse_page(self,page):
        User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
        header = {}
        header['User-Agent'] = User_Agent
        prx = {'http':'http://111.9.116.225:8080',
               'http':'http://113.140.43.136:80',
               'http':'http://117.90.2.178:9000',
               'http':'http://182.129.240.150:9000',
               'http':'http://111.155.116.196:8123'}
        try:
            resp = requests.get(self.entry_url+'page/'+str(page)).content
            if resp is None:
                sys.stdout.write('NoneResponse @ {0:6}\n'.format(page))
                self.bar.move()
                self.bar.log('{0:0>5}'.format(page))
                return
            html = BeautifulSoup(resp,'html.parser')
            li_row = html.find_all('ul',class_='list')[0].find_all('li')
            count = len(li_row)
            for i in range(0,count):
                url = li_row[i].find('div',class_='content').find('a')['href']
                Id = url[17:-5]
                if Id.isdigit():
                    self.datas.append(Id)
            self.pages.append(page)
        except requests.exceptions.ConnectionError:
            sys.stdout.write('ConnectionError @ {0:6}\n'.format(page))
        except requests.exceptions.ReadTimeout:
            sys.stdout.write('ReadTimeout @ {0:6}\n'.format(page))
        except IndexError:
            sys.stdout.write('IndexError @ {0:6}\n'.format(page))
        self.bar.move()
        self.bar.log('{0:0>5}'.format(page))

    def get_data(self):
        return self.datas

    def get_page(self):
        return self.pages
