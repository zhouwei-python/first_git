# coding:utf-8
#@Time : 2019/10/01  16:19
#author : Around
import os
from requests_html import HTML,HTMLSession

def main():
    session = HTMLSession()
    url = 'http://www.shicimingju.com/book'
    response = session.get(url)
    # 解析出书名
    book_name = response.html.xpath("//html/body/div[4]/div[2]/div[1]/div/div[2]/ul/li/h2/a")
    # 解析出书籍对应的url
    book_url = response.html.xpath("//html/body/div[4]/div[2]/div[1]/div/div[2]/ul/li/h2/a/@href")
    for i in range(len(book_url)):
        # 创建文件夹，名称为书名
        if not os.path.exists( book_name[i].text ):
            os.makedirs( book_name[i].text )
        print('正在下载%s'%book_name[i].text)
        # 将书籍的rul补全
        book_full_url = "http://www.shicimingju.com"+book_url[i]
        # 根据书籍url，发送请求，接收响应
        response1 = session.get(book_full_url)
        # 解析出每本书籍的章节的名字
        chater_name = response1.html.xpath("//html/body/div[4]/div[2]/div[1]/div/div[4]/ul/li/a")
        # 解析出每本书籍章节的url
        chater_url = response1.html.xpath("//html/body/div[4]/div[2]/div[1]/div/div[4]/ul/li/a/@href")
        # 遍历 章节名和url
        for j in range(len(chater_url)):
            print( '正在下载第%d章节' % (j+1) )
            # 将章节名字补全
            chater_full_url = "http://www.shicimingju.com"+chater_url[j]
            # 根据章节名发请求，接响应
            response2 = session.get(chater_full_url)
            # 解析每个章节对应的内容
            content = response2.html.xpath("//html/body/div[4]/div[2]/div[1]/div[1]/div/p/text()")
            # 开启一个流，将内容保存到文件
            with open('名著/'+book_name[i].text+"/"+chater_name[j].text+'.txt','w',encoding='utf-8') as w:
                for page in range(1,len(content)):
                    w.write('\xa0\xa0'+content[page].strip("\xa0")+'\n')
                print("第%s章下载完成"%(j+1))
if __name__ == '__main__':
    if not os.path.exists('名著'):
        os.makedirs('名著')
    main()
