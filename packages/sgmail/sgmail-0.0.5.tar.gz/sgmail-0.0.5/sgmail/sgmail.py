import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_gmail(from_address, password, to_addresses, subject='', html_head='', html_body='', html=None):
    if html is None:
        html = '''
        <html>
            <head>{}</head>
            <body>{}</body>
        </html>
            '''.format(html_head, html_body)

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = ', '.join(to_addresses)

    msg.attach(MIMEText(html, 'html'))

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(from_address, password)
        try:
            server.send_message(msg, from_addr=from_address, to_addrs=to_addresses)
        finally:
            server.quit()
    except():
        print("Something went wrong sending the email")
