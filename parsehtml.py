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
        self.latest_page = self.get_latest_page()
        self.datas = []
        self.errors = []

    def get_latest_page(self):
        # html = BeautifulSoup(self.session.get(self.entry_url).content,'html.parser')
        # page = html.find_all('a',title=u'最末页')[0].string
        page = '431'
        print('total '+page+' pages')
        return int(page)

    def parseList(self, li):
        global bar
        bar = ProgressBar(total=len(li))
        pages = []
        for p in li:
            pages.append(p['page'])
        pool = ThreadPool(64)
        pool.map(self.parse_page, pages)
        pool.close()
        pool.join()

    def parse(self, count=1, range=None):
        global bar
        if range is not None:
            self.latest_page = range[1]
            count = range[1] - range[0]
        elif count <= 0:
            count = self.latest_page
        bar = ProgressBar(total=count+1)
        pages = []
        while count >= 0:
            pages.append(str(self.latest_page-count))
            count -= 1
            # self.parse_page(str(self.latest_page-count))
        pool = ThreadPool(64)
        pool.map(self.parse_page, pages)
        pool.close()
        pool.join()

    def parse_page(self,page):
        global bar
        User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
        header = {}
        header['User-Agent'] = User_Agent
        prx = {'http':'http://121.40.199.105:80',
               'http':'http://120.26.140.95:81',
               'http':'http://61.130.97.212:8099',
               'http':'http://42.81.11.22:8088',
               'http':'http://124.238.235.135:81'}
        try:
            resp = requests.get(self.entry_url+'page/'+page,proxies=prx).content

        except requests.exceptions.ConnectionError:
            data = {
                'page':page,
                '_id':0,
                'error':'ConnectionError'
            }
            self.errors.append(data)
            return
        except requests.exceptions.ReadTimeout:
            data = {
                'page':page,
                '_id':0,
                'error':'ReadTimeout'
            }
            self.errors.append(data)
            return
        if resp is None:
            data = {
                'page':page,
                '_id':0,
                'error':'Null'
            }
            self.errors.append(data)
            return
        try:
            html = BeautifulSoup(resp,'html.parser')
            li_row = html.find_all('ul',class_='list')[0].find_all('li')
            count = len(li_row)
            for i in range(0,count):
                url = li_row[i].find('div',class_='content').find('a')['href']
                Id = url[17:-5]
                self.datas.append(Id)
        except IndexError:
            data = {
                'page':page,
                '_id':0,
                'error':'Null'
            }
            self.errors.append(data)
        bar.move()
        bar.log('{0:0>5}'.format(page))

    def get_data(self):
        return self.datas

    def get_errors(self):
        return self.errors
