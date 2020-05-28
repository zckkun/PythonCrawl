#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2020/5/28 1:51 PM
# @Author  : zhengchangkun
# @File    : main.py
# @Function: 豆瓣爬虫

"""
你们需要根据你们chrome浏览器的版本找到对应的chromedriver
本地查看chrome版本：chrome://settings/help
下载地址：http://npm.taobao.org/mirrors/chromedriver
"""
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BASE_URL = "https://book.douban.com/"
chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(executable_path="./chromedriver", chrome_options=chrome_options)  # 生成浏览器驱动


def parse_home_info():
    """
    解析主页面信息
    :return:
    """
    driver.get(BASE_URL)

    new_book_ul = driver.find_element_by_class_name('carousel').find_elements_by_tag_name('ul')  # 获取新书速速递信息
    data = list()
    for item in new_book_ul:
        title_info = item.find_elements_by_class_name('info')
        for _item in title_info:
            url = _item.find_element_by_class_name('title').find_element_by_tag_name('a').get_attribute("href")
            title = _item.find_element_by_class_name('title').find_element_by_tag_name('a').get_attribute("title")

            """
            注意：selenium 有时获取不了标签文本，由于WebDriver规范定义selenium WebDriver只能与可见元素交互,所以获取隐藏文件到空文本
            返回空字符，我们可以通过is_displayed()方便判断，如果打印出来为false说明被隐藏了，如果想获取文本到信息可以通过，
            element.attribute('attributeName')
            attributeName: textContent, innerText, innerHTML
            """
            author = _item.find_element_by_class_name('author').get_attribute("textContent")
            data.append((url, title, author))
    return data


def save_data(data):
    """
    保存数据
    :return:
    """
    with open('./data.txt', 'a') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


def crawl_run():
    data = parse_home_info()  # 解析主页面信息
    save_data(data)
    driver.close()  # 关闭浏览器驱动


if __name__ == '__main__':
    print("===============start===========")
    crawl_run()
    print("===============end===========")
