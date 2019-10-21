import re
import requests
from urllib import parse
import os
from bs4 import BeautifulSoup


def crawler(url, regex):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'Host': 'baike.baidu.com',
        'Cookie': '0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Upgrade-Insecure-Requests': '1',
    }
    page = str(requests.get(url=url, headers=headers, allow_redirects=False).text.encode('utf-8'))
    return [page[i.start():i.end()] for i in re.finditer(regex, page)]


def crawler_table(url, regex):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'Host': 'baike.baidu.com',
        'Cookie': '0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Upgrade-Insecure-Requests': '1',
    }
    page = str(requests.get(url=url, headers=headers, allow_redirects=False).text.encode('utf-8'))
    table = re.findall('<table .*></table>', page)[0]
    return [table[i.start():i.end()] for i in re.finditer(regex, table)]


def collect_station_data(path):
    os.remove(path)
    file = open(path, 'w')
    file.write('id,line,station\n')
    num = 1
    content = []
    for i in crawler('https://baike.baidu.com/item/%E5%8C%97%E4%BA%AC%E5%9C%B0%E9%93%81/408485',
                     '/item/%E5%8C%97%E4%BA%AC%E5%9C%B0%E9%93%81(([0-9]+%E5%8F%B7)|(%[A-Za-z0-9][A-Za-z0-9])+)%E7%BA%BF'):
        stations = crawler_table('https://baike.baidu.com' + i, '/item/(%[A-Za-z0-9][A-Za-z0-9])+%E7%AB%99')
        line = parse.unquote(i.split('/item/')[1])
        for j in stations:
            station = parse.unquote(j.replace('/item/', ''))
            if str(line + ',' + station + '\n') not in content:
                content += [str(line + ',' + station + '\n')]
    for i in content:
        file.write(str(num) + ',' + i)
        num += 1
    file.close()


if __name__ == '__main__':
    collect_station_data('../../data/subway/stations.csv')
