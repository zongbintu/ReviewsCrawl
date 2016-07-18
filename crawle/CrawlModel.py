import time

from data import ReviewsDataSource
from tuemail import SendEmail


class CrawlModel:
    def __init__(self):
        self.page = 1
        self.enable = False
        self.contextData = ''
        self.total = 0
        self.crawlCount = 0

    def get_page(self, page):
        print('get page is called')

    def load_reviews(self):
        while self.enable:
            try:
                print('u开始加载第' + str(self.page) + '页')
                self.get_page(str(self.page))
                self.page += 1
            except BaseException as e:
                print(e)
                # self.enable = False
        if not self.enable:
            self.today_reviews()

    def start(self):
        self.enable = True
        ReviewsDataSource.initDB()
        print(
            u'正在加载中请稍候......')

        # 新建一个线程在后台加载
        # _thread.start_new_thread(self.LoadPage, ())
        self.load_reviews()


    def today_reviews(self):
        todayReviews = []
        ReviewsDataSource.queryTodayReviews(todayReviews)
        html = """\
        <html>
            <head></head>
            <body>
            <p>
            <table border="1">
                 <tr>
                     <th>ID</th>
                     <th>评分</th>
                     <th>评论</th>
                     <th>版本</th>
                     <th>包名</th>
                     <th>来源</th>
                     <th>评论时间</th>
                     <th>昵称</th>
                </tr>
            """
        index = 1;
        for todayReview in todayReviews:
            tr = """ <tr>
                     <td>""" + str(index) + """</td>""" + """
                     <td>""" + str(todayReview.score) + """</td>
                     <td>""" + todayReview.content + """</td>
                     <td>""" + str(todayReview.versionCode) + """</td>
                     <td>""" + todayReview.packageName + """</td>
                     <td>""" + todayReview.appStore + """</td>
                     <td>""" + todayReview.reviewTime + """</td>
                     <td>""" + todayReview.nickName + """</td>
                </tr>"""
            html += tr
            index += 1
        html += """ </table></p></body>
            </html>"""

        SendEmail.send_email("Daily reviews(" + time.strftime("%Y-%m-%d", time.localtime()) + ")", html, 'enum@foxmail.com',
                            'cc@cc.com;cc2@cc.com')