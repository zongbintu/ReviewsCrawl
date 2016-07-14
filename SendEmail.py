import smtplib


def sendEmail(subject, text):
    TO = 'enum@foxmail.com'

    sender = 'pythontu@163.com'
    passwd = 'abc1234567'

    server = smtplib.SMTP('smtp.163.com')
    server.ehlo()
    server.starttls()
    server.login(sender, passwd)

    BODY = '\r\n'.join(['To: %s' % TO,
                        'From: %s' % sender,
                        'Subject: %s' % subject,
                        '', text])
    isSccuss = False

    try:
        server.sendmail(sender, [TO], BODY)
        isSccuss = True
        print('email sent')
    except:
        print('error sending mail')

    server.quit()

    return isSccuss
