# -*- coding: utf-8-*-
import time, json, csv,io
from datetime import datetime
from parsehtml import HtmlParser
from downparser import DownloadParser
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool  # 线程池

if __name__ == '__main__':
    start = time.time()
    parser = HtmlParser()
    # parser.parse(range=[1,431])
    #
    # with open('./Err.txt') as data_file:
    #     pageList = json.load(data_file)
    # parser.parseList(pageList)

    seconds = (datetime.utcnow() - datetime(1, 1, 1)).total_seconds()
    # with io.open('./Err-new.txt', 'w', encoding='utf8') as outfile:
    #     data = json.dumps(parser.get_errors(), sort_keys = True, indent = 4, ensure_ascii=False)
    #     outfile.write(data)
    #     outfile.close()

    downParser = DownloadParser()
    downList = parser.get_data()
    with open('./downErr.txt') as data_file:
        downList = json.load(data_file)
    downParser.parse(downList)
    end = time.time()

    datacsv = []
    for book in downParser.get_data():
        datac=[]
        datac.append(book["_id"])
        datac.append(book["Title"])
        datac.append(book["Pass"])
        datac.append(book["Links"])
        datacsv.append(datac)

    with open('./books-'+str(seconds)+'.csv', 'w', encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(['ID','书名','密码','链接'])
        spamwriter.writerows(datacsv)

    with io.open('./books-'+str(seconds)+'.txt', 'w', encoding='utf8') as outfile:
        data = json.dumps(downParser.get_data(), sort_keys = True, indent = 4, ensure_ascii=False)
        outfile.write(data)
        outfile.close()

    with io.open('./downErr-new.txt', 'w', encoding='utf8') as outfile:
        data = json.dumps(downParser.get_errors(), sort_keys = True, indent = 4, ensure_ascii=False)
        outfile.write(data)
        outfile.close()

    print(str(len(datacsv))+' books saved! '+ str(len(parser.get_errors()))+' pages error! '+str(len(downParser.get_errors()))+' books error')
    print('cost '+str(end-start))
