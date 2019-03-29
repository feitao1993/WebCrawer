# -*- coding: utf-8 -*-
"""
Created on 2019/3/27 下午 9:57

@author: FeiTao
@Email: feitao_sydx@163.com
@Software: PyCharm
"""
import requests
from bs4 import BeautifulSoup
import os
import re

def get_content(part_name, chapter_name, chapter_link):
    try:
        response = requests.get(chapter_link)
        soup = BeautifulSoup(response.text, "lxml")
        contents = soup.select("div#nr1 p")
        path = part_name + "/" + chapter_name + ".txt"
        # 去除文件名中的不合法字符
        p = re.compile(r'[\\:*?"<>|\r\n]+')
        path = re.sub(p, "_", path)
        with open(path, "w", encoding="utf-8") as f:
            for content in contents:
                f.write("  " + content.text + "\n")
    except Exception as e:
        print(e)

def get_chapter(part_name, part_link):
    try:
        response = requests.get(part_link)
        soup = BeautifulSoup(response.text, "lxml")
        chapters = soup.select("div.book-list.clearfix ul li a")
        for chapter in chapters:
            chapter_name = chapter["title"]
            chapter_link = chapter["href"]
            get_content(part_name, chapter_name, chapter_link)
    except Exception as e:
        print(e)

def get_part(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        parts = soup.select("div.title.clearfix h3 a")
        for part in parts:
            part_name = part["title"]
            part_link = part["href"]
            if not os.path.exists(part_name):
                os.mkdir(part_name)
            print("正在下载：", part_name)
            get_chapter(part_name, part_link)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    root_url = "http://www.luoxia.com/santi/"
    get_part(root_url)
    print("下载完成")



