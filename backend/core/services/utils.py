import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from jinja2 import Template
from email.mime.multipart import MIMEMultipart
from core.app import MAIL_USER, MAIL_PASSWORD, MAIL_PORT, MAIL_SENDER, MAIL_SERVER


def get_mailer():
    '''Send mail config'''

    mailer = smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT)
    mailer.login(MAIL_USER, MAIL_PASSWORD)
    return mailer


def add_attachments(attachment, msg: MIMEMultipart):
    '''Add Attachment Function'''

    part = MIMEBase('application', 'octet-stream')
    attach_name = os.path.basename(attachment.name)
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
        'Content-Disposition',
        f'attachment; filename={attach_name}'
    )
    msg.attach(part)


def send_mail(subject, recipients: str, filename_template: str):
    '''Send mail using mailer'''

    try:
        mailer = get_mailer()

        with open(filename_template, 'r') as file_template:
            template_str = file_template.read()
        
        jinja_template = Template(template_str)

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = MAIL_SENDER
        msg['To'] = recipients
        


        mailer.sendmail(MAIL_SENDER, recipients, msg.as_string())
        mailer.quit()
        
    except Exception as ex:
        return f'There was an error while trying to send the email {str(ex)}'
