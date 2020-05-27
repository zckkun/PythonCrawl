#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/5/27 12:57 PM
# @Author  : zhengchangkun
# @File    : main.py
# @Function: 星座爬虫
import requests
import logging
import json
from bs4 import BeautifulSoup

BASE_URL = "https://www.xzw.com"


def save_data(data):
    """
    保存用户信息
    :param data:
    :return:
    """
    with open('./constellation.txt', 'a', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')


def request_data_by_url(url):
    """
    获取请求数据
    :param url:
    :return:
    """
    try:
        resp = requests.get(url)
        resp.encoding = resp.apparent_encoding
        result = resp.text if resp.status_code == 200 else ""
    except requests.RequestException:
        result = ""
        logging.error('请求报错')
    return result


def get_title_info():
    """
    获取标题和详情url信息
    :return:
    """
    html = request_data_by_url(BASE_URL)
    soup = BeautifulSoup(html, 'lxml')
    data = list()
    soup = soup.find("div", attrs={"class": "a-nav"}).children
    for item in soup:
        if "href" in item.attrs:
            data.append((item.attrs['href'], item.attrs['title']))
    return data


def get_detail_info(item):
    """
    获取详情信息
    :param item:
    :return:
    """
    url, title = item
    url = BASE_URL + url
    data = parse_detail_info_by_url(url)
    return dict(title=title, data=data)


def parse_detail_info_by_url(url):
    """
    解析页面信息
    :param url:
    :return:
    """
    resp_data = request_data_by_url(url)
    soup = BeautifulSoup(resp_data, 'lxml')  # 获取详情信息
    soup = soup.find('div', attrs={'class': 'info_box'})
    title = soup.find('h1').find('strong').text  # 星座标题
    time = soup.find('h1').find('small').text  # 星座时间
    character = [(item.find('label').text, item.text) for item in soup.find('ul').children]  # 获取属性信息
    detail = soup.find('dd').find('p').text  # 获取详情信息
    return dict(title=title, time=time, character=character, detail=detail)


def run_crawl():
    """
    开始爬取数据
    :return:
    """
    print('================start==============')
    title_info = get_title_info()  # 获取标题详情信息
    result = [get_detail_info(item) for item in title_info]
    save_data(result)
    print('================end==============')


if __name__ == '__main__':
    run_crawl()
