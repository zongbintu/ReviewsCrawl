import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(subject, content, to, cc):
    sender = 'pythontu@163.com'
    passwd = 'abc1234567'
    smtp = 'smtp.163.com'

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    msg['Cc'] = cc

    partHtml = MIMEText(content, 'html')
    msg.attach(partHtml)

    server = smtplib.SMTP(smtp)
    server.ehlo()
    server.starttls()
    server.login(sender, passwd)

    isSccuss = False

    try:
        server.sendmail(sender, to, msg.as_string())
        isSccuss = True
        print('tuemail sent')
    except BaseException as e:
        print('error sending mail')
        print(e)

    server.quit()

    return isSccuss


send_email('test', 'title', 'enum@foxmail.com', 'zongbin.tu@msxf.com')
