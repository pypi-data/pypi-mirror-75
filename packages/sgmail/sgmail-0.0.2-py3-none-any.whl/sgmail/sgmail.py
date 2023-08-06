import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_gmail(gmail, password, to_email_addresses, subject='', head='', body='', html=None):
    if html is None:
        html = '''
        <html>
            <head>{}</head>
            <body>{}</body>
        </html>
            '''.format(head, body)

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = gmail
    msg['To'] = to_email_addresses

    msg.attach(MIMEText(html, 'html'))

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail, password)
        try:
            server.sendmail(gmail, to_email_addresses, msg.as_string())
        finally:
            server.quit()
    except():
        print("Something went wrong sending the email")
