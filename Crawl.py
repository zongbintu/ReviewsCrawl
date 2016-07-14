import datetime
import json
import urllib.request

import DataSource
from Review import Review


# ----------- 加载处理应用宝 -----------
class CrawlModel:
    def __init__(self):
        self.page = 1
        self.enable = False
        self.contextData = ''
        self.total = 0
        self.crawlCount = 0

    def getPage(self, page):
        myUrl = 'http://android.myapp.com/myapp/app/comment.htm?apkName=com.msxf.loan&apkCode=15701&p=' + page + '&contextData=' + self.contextData
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent': user_agent}
        req = urllib.request.Request(myUrl, headers=headers)
        myResponse = urllib.request.urlopen(req)
        myPage = myResponse.read()
        # encode的作用是将unicode编码转换成其他编码的字符串
        # decode的作用是将其他编码的字符串转换成unicode编码
        unicodePage = myPage.decode("utf-8")

        jsondata = json.loads(unicodePage)
        if (not jsondata == None) and 'obj' in jsondata:
            obj = jsondata['obj']
            if not obj == None:
                if self.total == 0:
                    if 'total' in obj:
                        self.total = obj['total']
                if 'commentDetails' in obj:
                    commentDetailes = obj['commentDetails']
                if 'contextData' in obj:
                    self.contextData = obj['contextData']

                self.crawlCount += len(commentDetailes)
                reviews = []
                for comment in commentDetailes:
                    review = Review()
                    review.appStore = 'myapp'
                    review.packageName = 'com.msxf.loan'

                    if 'content' in comment:
                        review.content = comment['content']
                    if 'nickName' in comment:
                        review.nickName = comment['nickName']
                    if 'score' in comment:
                        review.score = comment['score']
                    if 'versionCode' in comment:
                        review.versionCode = comment['versionCode']
                    if 'createdTime' in comment:
                        review.reviewTime = datetime.datetime.fromtimestamp(int(comment['createdTime'])).strftime(
                            '%Y-%m-%d %H:%M:%S')
                    reviews.append(review)
                DataSource.insert(reviews)

        self.enable = self.crawlCount <= self.total

    def loadPage(self):
        # 如果用户未输入quit则一直运行
        while self.enable:
            # 如果pages数组中的内容小于2个
            try:
                print('u开始加载第' + str(self.page) + '页')
                self.getPage(str(self.page))
                self.page += 1
            except BaseException as e:
                print('无法链接应用宝！')
                print(e)
                # self.enable = False

    def start(self):
        self.enable = True

        print(
            u'正在加载中请稍候......')

        # 新建一个线程在后台加载段子并存储
        # _thread.start_new_thread(self.LoadPage, ())
        self.loadPage()


print(
    u"""
    ---------------------------------------
       crawling myapp
    ---------------------------------------
    """)

crawlModel = CrawlModel()
DataSource.initDB()
crawlModel.start()
