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
        pool = ThreadPool(64)
        pool.map(self.parse_page, ids)
        pool.close()
        pool.join()

    def parse_page(self,ID):
        User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
        header = {}
        header['User-Agent'] = User_Agent
        prx = {'http':'http://111.9.116.225:8080',
               'http':'http://113.140.43.136:80',
               'http':'http://117.90.2.178:9000',
               'http':'http://182.129.240.150:9000',
               'http':'http://111.155.116.196:8123'}
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
