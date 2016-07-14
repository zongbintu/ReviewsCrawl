import sqlite3
import DbUtils
from Review import Review


def initDB():
    conn = sqlite3.connect('reviews.db')
    c = conn.cursor()
    # if not DbUtils.checkTableExists(conn, 'reviews'):
    c.execute("""create table if not exists reviews (
                id     integer     primary key autoincrement ,
                nickName        text,
                content        text,
                reviewTime        datetime,
                appStore        text,
                versionCode        int,
                packageName        text,
                score        float,
                createTime    datetime default (datetime('now', 'localtime'))
                )""")
    conn.commit()
    c.close()


def insert(reviews):
    conn = sqlite3.connect('reviews.db')

    # c.executemany()
    for review in reviews:
        try:
            c = conn.cursor()
            c.execute("INSERT INTO reviews (nickName,content,reviewTime,appStore,versionCode,packageName,score) \
                VALUES (\'" + review.nickName + '\' , \'' + review.content + '\' , \'' + review.reviewTime + '\' , \'' + review.appStore + '\' , ' + str(
                review.versionCode) + ' , \'' + review.packageName + '\' , ' + str(review.score) + ")")
        except BaseException as e:
            print('sql error : ' + e.__cause__)

    conn.commit()
    c.close()
    print('insert ' + str(len(reviews)) + ' row.')
