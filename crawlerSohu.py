# -*- coding = utf-8 -*-


from bs4 import BeautifulSoup   #网页解析，获取数据
import re   #正则表达式，进行文字匹配
import urllib.request,urllib.error  #指定URL，获取网页数据
import sqlite3  #进行SQLite数据库操作
import xlwt     #进行excel操作


def main():
    # 首先构建一个url
    baseurl = "http://news.sohu.com/"


    # 1.爬取网页
    datalist = getData(baseurl)
    savepath = "news.xls"
    dbpath = "news.db"
    # 2.逐一解析数据
    # 3.保存数据
    saveData(datalist,savepath)
    #saveData2DB(datalist,dbpath)
    askURL(baseurl)

findLink = re.compile(r'href="(.*?)"')         #创建正则表达式对象，表示字符串的模式，即规则
# findImgSrc = re.compile(r'src="(.*?)" width="100"/>',re.S)            #re.s,让换行符包含在字符中
findTitle = re.compile(r'title="(.*?)"')


# 爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0,1):
        url = baseurl      #str(i*25)
        html = askURL(url)  #保存获取到的网页源码
        # 2.逐一解析数据
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="focus-news"):
            data1 = []
            data2 = []
            item = str(item)
            # print(item)
            # break
            links = re.findall(findLink,item)
            for link in links:
                data1.append(link)
            #link = re.findall(findLink,item)
            titles = re.findall(findTitle,item)
            
            for title in titles:
                data2.append(title)

            datalist.append(data1)
            datalist.append(data2)

    return datalist


# 得到指定 一个URL的网页内容
def askURL(url):
    headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
}
    request = urllib.request.Request(url=url,headers=headers)
    html=""
    try:
        response = urllib.request.urlopen(request)
        html=response.read().decode("utf-8","ignore")
        #print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html
        
def saveData(datalist,savepath):
    print("save....")
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)      #创建workbook对象(文件)
    sheet = book.add_sheet('新闻',cell_overwrite_ok=True)
    col = ('新闻详情链接','新闻名')
    for i in range(0,2):
        sheet.write(0,i,col[i])
    for i in range(0,2):
        print("第%d条"%i)
        data = datalist[i]
        for j in range(0,23):
            sheet.write(j+1,i,data[j])

    book.save(savepath)

def saveData2DB(datalist,dbpath):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    for data in datalist:
        # for index in range(len(data)):
            #data[index] = '"'+data[index]+'"'
        sql = '''
            insert into news(
                news_link,news_title)
                values(%s)
            '''%",".join(data)
        cur.execute(sql)
        conn.commit()

    cur.close()
    conn.close()





def init_db(dbpath):
    sql = '''
        create table news
        (
        id integer primary key autoincrement,
        news_link text,
        news_title text
        )
    '''
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()

# 保存数据
# def saveData(savepath):
#     print("save....")

if __name__ == "__main__":
    main()
