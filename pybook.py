# -*- coding: utf-8-*-
import time, json, csv,io
from datetime import datetime
from parsehtml import HtmlParser
from downparser import DownloadParser
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool  # 线程池

if __name__ == '__main__':
    start = time.time()
    books=[]
    pages=[]
    error=[]
    try:
        # 读取books.json文件
        with open('./data/books.json') as data_file:
            books = json.load(data_file)
        # 读取PageErrors.json
        with open('./data/pages.json') as data_file:
            pages = json.load(data_file)
        # 读取BookErrors.json
        with open('./data/error.json') as data_file:
            error = json.load(data_file)
    except FileNotFoundError:
        print('FileNotFoundError')

    # 检索页面范围去除之前已经检索过的页面
    parseRange=list(range(1,432))
    for i in pages:
        parseRange.remove(i)
    # 分析页面
    parser = HtmlParser()
    parser.parse(pages=parseRange)

    for p in parser.get_page():
        pages.append(p)

    #加上之前检索出错的页面
    for i in parser.get_data():
        error.append(i)
    # 分析书本信息页面
    downParser = DownloadParser()
    downParser.parse(error)

    for d in downParser.get_data():
        if d not in books:
            books.append(d)
    # 保存本信息
    with io.open('./data/books.json', 'w', encoding='utf8') as outfile:
        data = json.dumps(books, indent = 4, ensure_ascii=False)
        outfile.write(data)
        outfile.close()
    # 保存已检索页面
    with io.open('./data/pages.json', 'w', encoding='utf8') as outfile:
        data = json.dumps(pages, sort_keys = True, indent = 4, ensure_ascii=False)
        outfile.write(data)
        outfile.close()
    # 保存分析出错书本信息页面
    with io.open('./data/error.json', 'w', encoding='utf8') as outfile:
        data = json.dumps(downParser.get_errors(), sort_keys = True, indent = 4, ensure_ascii=False)
        outfile.write(data)
        outfile.close()

    if len(books)>0:
        datacsv = []
        for book in books:
            datac=[]
            datac.append(book["_id"])
            datac.append(book["Title"])
            datac.append(book["Pass"])
            datac.append(book["Paswrd"])
            datac.append(book["Links"])
            datacsv.append(datac)

        with open('./data/books.csv', 'w', encoding='utf-8') as csvfile:
            spamwriter = csv.writer(csvfile)
            spamwriter.writerow(['ID','书名','密码','Pass','链接'])
            spamwriter.writerows(datacsv)

    print('\n'+str(len(books))+' books saved! '+ str(len(parser.get_page()))+' pages parsed! '+str(len(downParser.get_errors()))+' books error')
    end = time.time()
    print('cost '+str(end-start))
