# coding=utf-8
import datetime
import threading
from Driver.handle_init import handle_ini
from requests_html import HTMLSession
import time
import HTMLTestRunner_PY3
class Demo:
    url = "https://www.biduo.cc/biquge/53_53723/"
    file_path = handle_ini.get_value('file_path')
    cur = 0
    def fiction(self):
        ''' 建立Session：'''
        session = HTMLSession()

        # 打开Url检查返回码
        r = session.get(Demo.url)
        if r.status_code==404:
            print("url open failed: {}".format(r.url))
        return r
    def analysis(self,htmls):
        anchors = []
        news = htmls.html.find('div#list dd a')
        #查找内容并检查返回内容
        if news==None:
            print("article empty")
        for value in news:
            '''获取Element内容中的信息(文本/链接)'''
            anchor = {'text':value.text,'links':value.absolute_links}
            anchors.append(anchor)
        return anchors
    def __refine(self,anchors):
        '''数据精炼'''
        l= lambda anchor:{
            'title':anchor['text'].strip(),#strip()去掉字符串多余空格
            'links':anchor['links']
        }
        return map(l,anchors)
    def __sort(self,anchors):
        '''数据排序'''
        anchors=sorted(anchors,key=self.__sort_seed,reverse=True)
        return anchors

    def __sort_seed(self,anchor):
        for rank in range(0, len(anchor)):
            str(rank+1)
        return str(rank+1)


    def __show(self,anchors):
        '''数据显示'''
        for rank in range(0,len(anchors)):
            print('rank'+str(rank+1)
             + ":  " + anchors[rank]['title']
             +'      '+str(anchors[rank]['links'])
                  )
        set = anchors[rank]['links']
        lists = list(set)[0]
        session = HTMLSession()
        r = session.get(lists)
        newss = r.html.find("div.bookname h1")
        news = r.html.find("div#content")
        for texts in news:
            for self.title in newss:
                print('\n')
                print('-------------------'+self.title.text+'-------------------------')
            print(texts.text)
        return texts.text
    def __open(self,texts):
        wwwa = Demo.file_path  + "/{0}.txt".format(self.title.text)
        if wwwa ==None:
            print("标题为空")
        with open(wwwa, 'w') as f:
            f.write('-------------------------'+self.title.text+'-------------------------'+'\n'+texts)
            f.close()

    def go(self):
        htmls = self.fiction()
        anchors=self.analysis(htmls)
        anchors=list(self.__refine(anchors))
        anchors = self.__sort(anchors)
        anchors=self.__show(anchors)
        self.__open(anchors)
        print(str(datetime.datetime.now())+"-----------------------------------------------------------------")
        # time.sleep(3600)
        # timer = threading.Timer(0,Demo.go(self))#定时更新
        # timer.start()
if __name__ == '__main__':
    demo = Demo()
    demo.go()



