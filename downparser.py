# -*- coding: utf-8-*-
import sys, requests
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool
from progressbar import ProgressBar
class DownloadParser:
    def __init__(self,url='http://mebook.cc/download.php?id='):
        self.session = requests.session()
        self.entry_url = url
        self.datas = []
        self.errors = []
        self.bar= ProgressBar()

    def parse(self, ids):
        self.bar = ProgressBar(total=len(ids))
        pool = ThreadPool(256)
        pool.map(self.parse_page, ids)
        pool.close()
        pool.join()

    def parse_page(self,ID):
        User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
        header = {}
        header['User-Agent'] = User_Agent
        prx = {'http':'http://121.40.199.105:80',
               'http':'http://120.26.140.95:81',
               'http':'http://61.130.97.212:8099',
               'http':'http://42.81.11.22:8088',
               'http':'http://124.238.235.135:81'}
        try:
            resp = requests.get(self.entry_url+str(ID)).content
            if resp is None:
                self.errors.append(ID)
                self.bar.move()
                self.bar.log('{0:0>5}'.format(ID))
                return
            html = BeautifulSoup(resp,'html.parser')
            title = html.find('div',class_='desc').find('p').string[5:]
            password = html.find('div',class_='desc').find_all('p')[5].string[5:].strip(' ')
            pws = password
            paswrd = {}
            while '：' in pws:
                index = pws.index('：')
                paswrd[pws[0:index]]=pws[index+1:index+5]
                pws = pws[index+5:].strip('     ')
            links=html.find('div',class_='list').find_all('a')
            dls={}
            for l in links:
                dls[l.text]=str(l['href'].strip(' '))

            if title == '':
                self.errors.append(ID)
            else:
                data = {
                    '_id':ID,
                    'Title':title,
                    'Pass':password,
                    'Paswrd':paswrd,
                    'Links':dls
                }
                self.datas.append(data)
        except requests.exceptions.ConnectionError:
            self.errors.append(ID)
        except requests.exceptions.ReadTimeout:
            self.errors.append(ID)
        except AttributeError:
            self.errors.append(ID)
        except IndexError:
            self.errors.append(ID)
        self.bar.move()
        self.bar.log('{0:0>5}'.format(str(ID)))

    def get_data(self):
        return self.datas

    def get_errors(self):
        return self.errors
