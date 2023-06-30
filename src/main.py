"""
@version: 3.11
@author: victor
@file: main.py
@date: 2023/6/9-15:58
"""
import requests
import json
from lxml import etree
import os
import time
import random

# (1) 获取cookie，通过登录，或者直接到网页中取静态cookie值

# (2) 爬取书架上的书籍信息
def get_shelf_books():
    '''
    params:
    return: books [{},{},{}]
    '''
    url = 'https://user.17k.com/ck/author/shelf?page=1&appKey=2406394919'
    cookie = 'GUID=b685a4d6-fcd2-4745-98bb-1faf21ee3fb5; accessToken=nickname%3D%25E4%25B9%25A6%25E5%258F%258Bi5125da26%26avatarUrl%3Dhttps%253A%252F%252Fcdn.static.17k.com%252Fuser%252Favatar%252F06%252F86%252F80%252F100268086.jpg-88x88%253Fv%253D1686296914568%26id%3D100268086%26e%3D1701848915%26s%3D505b90eab14f8dfb; c_channel=0; c_csc=web'
    headers = {
        "User Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "referer": "https://user.17k.com/www/bookshelf/index.html",
        "cookie": cookie
    }
    res=requests.get(url, headers=headers)
    shelf_books = res.json().get("data")
    return shelf_books
novels = get_shelf_books()
print(novels)

# (3) 创建书架文件夹
root_path = "My Book Shelf"
if not os.path.exists(root_path):
    os.mkdir(root_path)

def get_books(novels):
    for bookDict in novels:
        # 循环处理每一本书籍
        bookID = bookDict.get("bookId")
        bookName = bookDict.get("bookName")
        # 创建书籍文件夹
        book_path = os.path.join("My Book Shelf", bookName)
        if not os.path.exists(book_path):
            os.mkdir(book_path)
        get_chapters(bookID,bookName,book_path)

def get_chapters(bookID,bookName,book_path):
    # 爬取每一本书的章节页面
    bookHref = requests.get(f"https://www.17k.com/list/{bookID}.html")
    bookHref.encoding = "utf8"
    # 解析书籍的章节链接
    selector = etree.HTML(bookHref.text)
    items = selector.xpath('//dl[@class="Volume"]/dd/a')
    for i in items:
        # 处理书籍每一章节信息
        charpter_href = i.xpath("./@href")[0]
        chapter_title = i.xpath("./span/text()")[0].strip()
        # print(chapter_title,charpter_href)
        # 爬取章节页面
        res = requests.get('https://www.17k.com/' + charpter_href)
        res.encoding = "utf8"
        chapter_html = res.text
        # print(chapter_html)
        # 爬取章节文本内容
        selector = etree.HTML(res.text)
        chapter_text = selector.xpath('//div[contains(@class,"content")]/div[@class="p"]/p[position()<last()]/text()')
        download(bookName,chapter_title,chapter_text,book_path)

def download(bookName,chapter_title,chapter_text,book_path):
    # 章节下载
    chapter_path = os.path.join(book_path, chapter_title)
    with open(chapter_path, "w") as f:
        for line in chapter_text:
            f.write(line + "\n")
    time.sleep(random.randint(1, 3))
    print(f"{bookName}这本书的{chapter_title}章节下载完成！")

# (4) 下载每本书每一章节信息
get_books(novels)

# novels_list=json.loads(novels.text)["data"]
# print(novels_list)
# for item in novels_list:
#     books=item["bookName"]
#     # href=item[]
#     print(books)
