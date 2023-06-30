import requests
import json
from lxml import etree
import os
import time
import random

url = 'https://user.17k.com/ck/author/shelf?page=1&appKey=2406394919'
cookie = 'GUID=b685a4d6-fcd2-4745-98bb-1faf21ee3fb5; accessToken=nickname%3D%25E4%25B9%25A6%25E5%258F%258Bi5125da26%26avatarUrl%3Dhttps%253A%252F%252Fcdn.static.17k.com%252Fuser%252Favatar%252F06%252F86%252F80%252F100268086.jpg-88x88%253Fv%253D1686296914568%26id%3D100268086%26e%3D1701848915%26s%3D505b90eab14f8dfb; c_channel=0; c_csc=web'
headers = {
        "User Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "referer": "https://user.17k.com/www/bookshelf/index.html",
        "cookie": cookie
}
res=requests.get(url, headers=headers)
shelf_books = res.json().get("data")

for bookDict in shelf_books:
    # 循环处理每一本书籍
    bookID = bookDict.get("bookId")
    bookName = bookDict.get("bookName")
    # print(bookName,bookID)

# 爬取每一本书的章节页面
bookHref = requests.get("https://www.17k.com/list/3543515.html")
bookHref.encoding = "utf8"
# print(bookHref.text)
# 解析书籍的章节链接
selector = etree.HTML(bookHref.text)
items = selector.xpath('//dl[@class="Volume"]/dd/a')

for bookDict in shelf_books:
    # 循环处理每一本书籍
    bookID = bookDict.get("bookId")
    bookName = bookDict.get("bookName")
    # 创建书籍文件夹
    book_path = os.path.join("My Book Shelf", bookName)
    if not os.path.exists(book_path):
        os.mkdir(book_path)

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
    break

chapter_path = os.path.join(book_path, chapter_title)
print(chapter_path)
# for line in chapter_text:
#     print(line + "\n")