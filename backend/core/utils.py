import os
import ssl
import base64
import smtplib
from core.app import app
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from flask.templating import render_template
from email.mime.multipart import MIMEMultipart


def send_mail(subject: str, to: list, plantilla: str, params: dict, attachments: list = []):
    '''
    Envia un correo electronico
    :param subject: asunto del correo electronico
    :param to: destinatarios del correo electronico
    :param plantilla: plantilla utilizada para el correo electronico
    :param params: parametros de la plantilla
    '''

    with app.app_context():
        try:
            is_tls = os.getenv('MAIL_TLS', 'true') == 'true'
            smtp_server = os.getenv('MAIL_SERVER')
            port = int(os.getenv('MAIL_PORT', '587'))
            sender_email = os.getenv('MAIL_SENDER')
            user_email = os.getenv('MAIL_SENDER')
            password_email = os.getenv('MAIL_PASSWORD')

            msg = render_template(plantilla, **params)

            message = MIMEMultipart('related')
            message['Subject'] = subject
            message['From'] = sender_email
            message['To'] = ','.join(to)
            message.attach(MIMEText(msg, 'html'))

            # SOE Latam Logo
            msg_image = MIMEImage(base64.b64decode('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'))
            msg_image.add_header('Content-ID', '<logo_soe>')
            message.attach(msg_image)

            # Attachments
            for attachment in attachments:
                part = MIMEBase('application', 'octet-stream')
                path = attachment['path']

                with open(path, 'rb') as file:
                    part.set_payload(file.read())

                encoders.encode_base64(part)
                part.add_header('Content-Disposition',
                                f'attachment; filename={attachment['filename']}')
                message.attach(part)

            send = send_mail_by_tls if is_tls else send_mail_by_ssl
            send(smtp_server, port, user_email, password_email, to, message)
        except Exception as ex:
            print('There was an error while trying to send the email: ', str(ex))


def send_mail_by_ssl(smtp_server, port, user_email, password_email,
                     to, message):
    '''
    Envio de correo electronico por ssl
    :param smtp_server: servidor de correo electronico
    :param port: puerto del servidor de correo electronico
    :param sender_email: usuario del servidor de correo
    :param password_email: contraseña del usuario del servidor de correo
    :param to: destinatarios del correo electronico
    :param message: cuerpo del correo electronico
    '''
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(user_email, password_email)
        server.sendmail(user_email, to, message.as_string())


def send_mail_by_tls(smtp_server, port, user_email, password_email,
                     to, message):
    '''
    Envio de correo electronico por tls
    :param smtp_server: servidor de correo electronico
    :param port: puerto del servidor de correo electronico
    :param sender_email: usuario del servidor de correo
    :param password_email: contraseña del usuario del servidor de correo
    :param to: destinatarios del correo electronico
    :param message: cuerpo del correo electronico
    '''

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(user_email, password_email)
        server.sendmail(user_email, to, message.as_string())


if __name__ == '__main__':
    send_mail(
        'Testing', ['juandiego14012003@gmail.com'], '',
        {
            'id': '1',
            'equipment': 'Videoline 308-RP - EEBS805A',
            'serial': '123123123',
            'installed_date': 'August, 3, 2025',
            'distributor': 'All For Tires',
            'client': 'Prodynamics'
        }
    )
