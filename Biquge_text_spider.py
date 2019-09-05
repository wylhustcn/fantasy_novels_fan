# -*- coding:UTF-8 -*-
# 从笔趣阁网站获取小说全集的txt
# Date: 2019-09-04
# BY YULIANG
import requests
from bs4 import BeautifulSoup
# BeautifulSoup is a html parser, Usage:https://beautifulsoup.readthedocs.io/zh_CN/latest/
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# 屏蔽SSL认证警告信息


class biquge_spider(object):

    def __init__(self):
        # 定义class中的全局变量
        self.root_url = 'https://www.biqugex.com'
        self.search_url = 'https://so.biqusoso.com/s.php?ie=utf-8&siteid=biqugex.com&q=search_text'  # 文本中的search_text将由用户输入
        self.book_link_list = {}  # 用户存放搜索出的小说链接的字典
        self.book_name_list = {}  # 用户存放搜索出的小说名的字典
        self.chapter_name = []    # 存放章节名
        self.chapter_link = []    # 存放章节的下载链接
        self.chapter_num = 0      # 存放章节的总数

    # search函数用来搜索小说，并且将小说的序号与链接存入self.search_list中使用，并将搜索的小说清单返回给用户
    def search(self, search_text):
        target = self.search_url.replace("search_text", search_text)
        req = requests.get(url=target, verify=False)
        search_result = BeautifulSoup(req.text, "html.parser")
        span = search_result.find_all("span", attrs={"class":"s2"})
        books = BeautifulSoup(str(span), "html.parser")
        i = 1
        if len(books.find_all("a")) >= 2:
        # 如果搜索到结果，及len(books.find_all("a")) >= 2，返回True否者返回False
            print("\n您搜索到的小说包括：")
            for book in books.find_all("a"):

                self.book_name_list[str(i)] = book.text
                self.book_link_list[str(i)] = book.get("href")
                print(str(i) + ".\t" + book.text)  # 显示搜索结果
                i = i + 1
            return True
        else:
            print("\n没有查询到您要搜索的小说。")
            return False

    # 查询文章的章节名称、下载链接与章节数目，并放入self相关的变量中
    def download_url(self, download_number):
        print("您选择的小说是:" + self.book_name_list[str(download_number)] + "\t小说链接为：" + self.book_link_list[str(download_number)])
        target = self.book_link_list[str(download_number)]
        req = requests.get(url=target, verify=False)
        req_decode = req.text.encode("iso-8859-1")
        # 重要：此时返回的req.text的html文件为GBK编码，用读取为乱码，需要换成UTF-8的格式，此处先使用 req.encode("iso-8859-1")将文件转化为unicode编码,再使用beautiful将文件转化为UTF-8编码
        bf = BeautifulSoup(req_decode, "html.parser")
        div = bf.find_all("div", attrs={"class":"listmain"})
        div_a = BeautifulSoup(str(div), "html.parser")
        i = 0
        # 前面有12章是新的章，后续处理注意
        for chapter in div_a.find_all("a"):
            i = i + 1
            if i <= 12:
                continue
            else:
                self.chapter_name.append(chapter.text)
                self.chapter_link.append((self.root_url+chapter.get("href")))
#                print(str(i-12)+".\t"+chapter.text+" : "+(self.root_url+chapter.get("href")))
        self.chapter_num = i-12

    # 输入下载的章节id，返回每一章的下载结果
    def download_chapter(self, chapter_id):
        target = self.chapter_link[int(chapter_id-1)]
        req = requests.get(url=target, verify=False)
        # print(req.text)
        # 此处读取丢失了大段的小说正文内容，使用urllib.request.urlopen后同样的地方仍然缺失
        # 进行调试时，在bf的text属性中可以看到正文内容，但是print出来后就无法查看
        # 使用Linux系统运行同样的代码，正文不会丢失
        # 在调试页面中丢失，但是在最终write入文件时存在
        bf = BeautifulSoup(req.content, "html.parser")  # 直接读取req.text会造成编码问题，此处使用content二进制文件
        chapter_div = bf.find_all("div", attrs={"class":"showtxt"})
        chapter_text = chapter_div[0].text.replace("<br/>","").replace("  ","")
        chapter_text = self.chapter_name[int(chapter_id-1)]+"\n"+ str(chapter_text)
        return chapter_text

    # 最后新建txt文件，将小说写入txt文件
    def write_chapter(self, chaper_text, file_name):
        file_dict = "download/"+ file_name
        with open(file_dict, 'a+', encoding='UTF-8') as f:
            f.write(chaper_text)
            f.write("\n\n")


if __name__=='__main__':
    '''
    此处用来测试用
    search_name = "诛仙"
    download_name = 1
    '''
    bqg = biquge_spider()
    # 如果小说没有搜索到，则提醒重新输入
    search_name = input("请输入您想搜索的小说名称：")
    flag = bqg.search(search_name)
    while flag is False:
        search_name = input("请重新输入小说名称：")
        flag = bqg.search(search_name)

    # 输入的编号必须为数值，且在编号范围内，否者重新输入
    download_name = input("\n请输入您想下载的小说编号（如:1）:")
    while (str.isdigit(download_name) is False) or (int(download_name) > len(bqg.book_name_list)) or (int(download_name) <=0):
        download_name = input("您输入的编号不正确，请输入您想下载的小说编号（如:1）:")
    print(search_name + "开始下载......")
    bqg.download_url(download_name)
    for i in range(bqg.chapter_num):
        print("正在下载第"+str(i+1)+"章，还剩"+str(bqg.chapter_num-i)+"章。。。")
        chapter_text = bqg.download_chapter(i+1)
        bqg.write_chapter(chapter_text, bqg.book_name_list[str(download_name)]+".txt")