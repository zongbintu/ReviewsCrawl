import sqlite3
import hashlib

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
                createTime    datetime default (datetime('now', 'localtime')),
                hexdigest   text UNIQUE
                )""")
    conn.commit()
    c.close()


def insert(reviews):
    conn = sqlite3.connect('reviews.db')

    # c.executemany()
    for review in reviews:
        try:
            print(review.nickName+'   '+review.content+'   '+review.reviewTime)
            c = conn.cursor()
            c.execute("INSERT INTO reviews (nickName,content,reviewTime,appStore,versionCode,packageName,score,hexdigest) \
                VALUES (\'" + review.nickName + '\' , \'' + review.content + '\' , \'' + review.reviewTime + '\' , \'' + review.appStore + '\' , ' + str(
                review.versionCode) + ' , \'' + review.packageName + '\' , ' + str(
                review.score) + ' , \'' + hashlib.md5(
                (review.nickName + review.content + review.reviewTime).encode('utf-8')).hexdigest() +'\''+ ")")
        except Exception as e:
            print('sql error : ' + e)
            continue

    conn.commit()
    c.close()
    print('insert ' + str(len(reviews)) + ' row.')


def queryTodayReviews(reviews):
    conn = sqlite3.connect('reviews.db')

    try:
        c = conn.cursor()
        for row in c.execute(
                "select nickName,content,reviewTime,appStore,versionCode,packageName,score from reviews WHERE date(reviews.reviewTime) = date('now')"):
            review = Review()
            review.appStore = 'myapp'
            review.nickName = row[0]
            review.content = row[1]
            review.reviewTime = row[2]
            review.appStore = row[3]
            review.versionCode = row[4]
            review.packageName = row[5]
            review.score = row[6]
            reviews.append(review)
    except BaseException as e:
        print('sql error : ' + e.__cause__)

    c.close()
    print('queryTodayReviews ' + str(len(reviews)) + ' row.')
