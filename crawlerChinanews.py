# -*- coding = utf-8 -*-


from bs4 import BeautifulSoup   #网页解析，获取数据
import re   #正则表达式，进行文字匹配
import urllib.request,urllib.error  #指定URL，获取网页数据
import xlwt     #进行excel操作
import time

def sleep(int):
    time.sleep(int)


def main():
    # 首先构建一个url
    baseurl = "https://www.chinanews.com/scroll-news/2020/120"


    # 1.爬取网页
    datalist = getData(baseurl)
    savepath = "newsChinanews.xls"
    # 2.逐一解析数据
    # 3.保存数据
    saveData(datalist,savepath)
    askURL(baseurl)

findLink = re.compile(r'<a href="(.*?)">')         #创建正则表达式对象，表示字符串的模式，即规则
# findImgSrc = re.compile(r'src="(.*?)" width="100"/>',re.S)            #re.s,让换行符包含在字符中
findTitle = re.compile(r'.shtml">(.*?)</a>')


# 爬取网页
def getData(baseurl):
    datalist = []
    for i in range(1,10):
        print(i)
        followurl = str(i)+"/news.shtml"
        url = baseurl +followurl    #str(i*25)
        html = askURL(url)  #保存获取到的网页源码
        # 2.逐一解析数据
        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="dd_bt"):
            data1 = []
            data2 = []
            item = str(item)
            # print(item)
            # break
            links = re.findall(findLink,item)
            for link in links:
                linkReal = "www.chinanews.com"+link
                data1.append(linkReal)
                print(linkReal)
            #link = re.findall(findLink,item)
            titles = re.findall(findTitle,item)
            
            
            for title in titles:
                data2.append(title)
                print(title)

            # datalist.append(data1)
            datalist.append(data2)
        # sleep(3)

    return datalist


# 得到指定 一个URL的网页内容
def askURL(url):
    headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "Cookie":"cnsuuid=091ff1f6-5c33-6890-78b7-c8304f990a901084.5823721810248_1608665896323; Hm_lvt_0da10fbf73cda14a786cd75b91f6beab=1608721796; Hm_lpvt_0da10fbf73cda14a786cd75b91f6beab=1608721796"
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
    for i in range(0,9):
        print("第%d条"%i)
        data = datalist[i]
        for j in range(0+i*(len(data)),+i*(len(data))+len(data)):
            k=i%2
            m = j - i*(len(data))
            n =(i//2)*len(data) + j - i*len(data)
            sheet.write(n+1,k,data[m])

    book.save(savepath)


# 保存数据

if __name__ == "__main__":
    main()
