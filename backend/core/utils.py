import math
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
from flask_babel import force_locale
from email.mime.multipart import MIMEMultipart
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
import filetype
from flask_babel import gettext


def send_mail(subject: str, to: list, plantilla: str, params: dict, attachments: list = [], language: str = 'es', with_soe_logo: bool = True):
    '''
    Envío de correo
    :param subject: asunto del correo
    :param to: destinatarios del correo
    :param plantilla: plantilla utilizada para el correo
    :param params: parámetros de la plantilla
    '''

    with app.app_context():
        try:
            is_tls = os.getenv('MAIL_TLS', 'true') == 'true'
            smtp_server = os.getenv('MAIL_SERVER')
            port = int(os.getenv('MAIL_PORT', '587'))
            sender_email = os.getenv('MAIL_SENDER')
            user_email = os.getenv('MAIL_SENDER')
            password_email = os.getenv('MAIL_PASSWORD')

            message = MIMEMultipart('related')
            with force_locale(language):
                msg = render_template(plantilla, **params)

            message['Subject'] = subject
            message['From'] = sender_email
            message['To'] = ','.join(to)
            message.attach(MIMEText(msg, 'html'))

            if with_soe_logo:
                # SOE Latam Logo
                msg_image = MIMEImage(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAKYAAAAxCAYAAABQ69KMAAAACXBIWXMAAAsSAAALEgHS3X78AAAQAElEQVR4Acx9B2BVVfL3zL3vpRMgVBERFEHRBTQI0kMnAQSBQKiKHQT976oItmVddVUEbGAHFOkSSkhCQhdCFVQQFESadEhCh+S9e873m/veS17KI4m7n3o5v3PmzJmZM3PaLUnUoP9/F8fUrh0yediwG6YMH95wyqhR97w/cmRLweQRI1q9N2p46w+eeKLNlOGj2gqEFgj9HniBMbyttIncO9AH3TogRo1qjX7Rz1NtxLZg4vDhrUXv2HPPtXojOrp8WcOPIXI83rlz1fcee6zBOyMeufvdESNa2PEMHyV+tP3wmWdifn755XZ63Ivt9bhx7fXLL3fQSQs76IXAokUd9YwZnfT06Z0FLpSuadM6CfTULzrqL4BZszrppKTOeVi0tIvQF+cldkp/6622U4Y/3HBs06aV4LcBlDqJ30mjHmukv5reQX/1WQedOK+9Hj++/dZx42I+eeWVtlNeGttWytmow+8Y/fK/2nnwcjsX4vABbZ64EI8rKQmxeeBCjDaWLGnvgl3EjTFA/P96ud2+f/2r3af/ln5eajsfpf43+FOntteLF7c7jb7ff/bZlp+8Oq7FqQ8+aKPnz249DuNbpuBKMwojYmIiNnw0uevxdavHp69bkzL8vbfXPz5p/JrHx7+Z/sT4N9KeePvNtOETxy8bOf7t1BETxqc8PvFNQfKIt8eneOvJIye+CbzhBehJXtj8CckjUX8ceBI6kE0dOfENL95E6Ye33kxFv6kj3n49FbZTn3h7fOr/TZiwbNSbb6RWf+aZr+J69LiuNDE9SuRc99JLzXanpLy0/MCviZNnfbXuiQlvrR05YdKKkRPGpw1/G/F4fEh59NVXkus9PzZZP/fSUj36haV67AtJukvXJB3XZYmK7bxE9euzWA3ot0gDZv/+i8yEhMVmwgDU+y/W/YDevRfrTp0W5aFrx4WqY8dFoT1iF3ccNTLlsQkTV7+atnTlie+2vr35lVeaxxOZpYnhn6NfaBL7xhvJVny/JBU/IEl3i12qnxy5NHrs6OSHxzyb8tiLLyU/PPqZlH5jRifrMc8l6+efW2pj7PNLzefGJPmgx4xZaiM2donZudMS3bkz0GmJ2Ql1G52SHKNGJdHzzy+lsWOTaMzzS28eM3rpQ6PRz+ixyX2ehf1nRyfpgQlJumvHpVGj/5E84tVxyx5+9tm0yg8/kKK795jTd+hdNxqlCao0Ms1r1gw9PG1mwgezpibdPWzwwsotWjxtXlezHYVWqEVBYRUpKKQcBYeGcwEEh3NIUBgFB4VTsDOcggApg6UeHE7BAtBBXth8Ly08X92WCxZbQDD0IOOzExQcboUEh6lgDiOnGaZAU3BwmPts1qYPkpJ+LSE248cxT989ZfeOL1o+/+zyurEdXnHUvrGHUalSPQ4rV9kIDotEPBF2XEEh4WKXg4LCdHBQqA5xhlKoI5RCHKHscISS0xnGTmeo4YXQFAwZGw6MgRdBZigJgh2hBOggKZ2hDDkN390hEVFWhahGlRo1+nv06P9bMvmb9OfkzlRCHHx7x7bt3aGh11lBwaHkCAtlZzjgDBV/2eEIY4cznIPER0cYBXnAwY4wHyjYDLMRBH88CCMneIB2mJCDbjAQ4oScwBGGOMLgf5h2gnaCF+QMpyC7RJsT/GCUQeHsDIkgR2gEO4LCc06f2jf/9SU//U8W5rguXaIWzv3qjZr94j5W1WvEaGdYiEEOYjZIGZrkYmZi1ImYKA/SvWx4Xym0QOq/B/66frQ2SLzQZJAbfSvWFn27Pf2TbdtcFOCKIXIcSpz90K1jnp7LdW9JYGdYOYdyQNpnF6QvISSN+Aj2BQZKA/0w2hm0JpPIC6F9ILQVhUeWIe+BWDJI5BhxOBGIQ8OCdpB2RFSu2Kz5mDkT3x54rZPzwZYtIyreVLezU7NhkoJnMMcCT18afRGb5Ck9MTLq5OVLm01LnTy+kF2KvkFsyxowKPDwyJYFDZ/zaB/Pr4RL0GNSiEspS7mzs9f9a/fuS2IJDb8/jRtyX9XnP35vctTdTUZaoaGRCg47MGiGOMREMmHMIK7RBTMT838Hf/PM/rbIHgaCXzLwllLEVy+cmJqevslfx5+Or1IlYvqypWOrdev8LpWrXIc5hC178BkBeSSZOaDPHon8nNkjKxxmD8187VJkBcx+csIA3IwMcFiMxRlerkq79v/XsXfvquAWm+LvuaeRWa1qY62IDM3wOy8MW55ZeAVhN/hlzAXbmfPrfmJFSOZ8OeaCtMEac8MkDjFo0rkXj61ft4zg3n+1MOMbNIh45rmxb9L1tfuQI9QgdhIxdhz6IoCRGfTHXMwcsCNMH0LFiQAZeEfq6LGMTatX7y9OATEFTZ057R8127Udo53lQllOSZiWk1+AkIpTKxWPGYZKJVm8ENYUWQbjzDMARWRPpiYKDqvdsvHtN1HxF8d06dDZCg2ONA0HVJigAUAfefEqZeMye+LSOMnLpinSHl1GRHzx4vcvfjV3m3D/m3VjvDbpzeGh9e4c5MSDgwMnpEMZ9g5Q6Auk2McO9XZh14rPJKD/JQr0gllAItmdWJ3kcLvcZ7d9lzL94MGrBeS8lZdGjOgY3rbtc3juCXNik2kHgjE0OXHcyOB5xYotJIaiDdK7P2RB+FBU+loceEIOqAbJCsVi0E5F2rQIzOByDW6JKk4XGy3ceccdXS0DI2AvHFjxpCLixfuPUYOetP0eFOnEy/CMiCaxqXAftyyXdWXXTyvnb9x4RUQMyX4PZo54pOFNrVo+SYbp1IzRwuTJaSKFz6iMn/BKss/MxPy/Q+H+FDFYmkyyiHOvZm/9Yfd2MIqk15o1q9ag972v5DpCwpiwybDDDEyKaJNtwxcZBbxkoIsCCwgLW9vwTIaGXUFAQ8U2YDphg+EXwT/GALOwsOhCQsOCilO5t0fHhhxV8XZxnzE5eL62z0kuTrgYns9HZibmsqMYkwVYsCiRkHZb5y9v3bbO11jySPsk/Up5Mejz+IjhFBxSA76SRsBuhGsxRglgDLoYRg1c7DjoSoAKfMIznpQYX9KgkUFAFYBGY2GQ6AryLYrVfECHioMtL2IGueGb61TmlhUzZ+4Dp0gaMOL+HlS58t8Yz5OMSYdTRAjQDWg27NNfYiKvHzZNuFDH0iNGGNKGpQcmEgQ8dgy0YQpwV2GAiEkD2CYibkNUwZRkg/wuDfs2cLtTpibLJGhrQhWHpUmsDXXueGaxd4C7mjdvQaYZKhvMY4O8F3yACZsH+8JkZingjwIs2Afwnggx1NGE8fXJS0lkt0gD2oUGx7Yl0XgBfcKBQOKs0ALQDBDG2EKfbun20qW9r6ev+gHG7GTYeRmzuEfvvzHo5hvjTG0YGoYNDBOeLnEiSQ8AeGLSkEyAo5rEbzQRCFnACkGyJqUt7daWctlQygWOC1G67FJplCRwawU5pT1yllfeUm75B123lnbUbdq/VG63YeW62VIWua0rJzfvTJ505EiRSZQvC7U6dX1EEQfhfZc0fBWgwPcFQoTwHBUJg2RQMdiKPBQhFpkPrfHOn3vJTZfPnlLnsn61zmb9Yp3L3KdBq/PZv6pz2ftRP6DOZx2g82ePGjlXrmrLDVVtWyQxLoBd/8TMxAzgbNGAtBnoXxsWafDJcl29fOTwaeH7Izo62lm7/h1tNAexqRlNJrQZIFyGxyb0maUNrLwEJyCvcXCw5ba0pd1Ky9y4MReYAwVaa5eyBAqlcmmlASkV6hqQEsEp5RZ9bXlp1JXb7VYutxt+WwLDyrHcu3avnZSWlu1zwfARZSiNhD7xCVZQ0HX2g7gdk50VawKLDzsaTThODIkXJwa7rrrp2IGMq9+sHXd2WfoD51NSBqnU9AFq+YoEa8WKASp9+SDXggWDXfMTh2Qmpw49kbb8fhsrlj9wIi3tgRNLlgyT8mh6+gNXFi8a6lq2bIjr66+HuCa9N9iDSYNXT5o0cMm77w5Qc+YNzlmY/ODFBYmPnIfMi+/+Zx68gSfI/VK7tvfcQ+UrN9T4oGLvZrQxF4xLavaACYHpldggRpYwMfp09syunAWrnvry6edbvRrXo2m7mHbNYtq2b9q2Tbu727YVxDRBPbp1y5gmUx5/ounPE8f3tk4cWqutXG0qsUTEBNewVCnAJV0LCJKEowDSxDlXj23dvvMQFboejY6+NfT6GtHM7GnxlZ5awFxDLhfx5br1lbMZGU/Tl9P7UVLSQFq2PEGlr+inFyzop1JTE/TCxEGgB7sxV3rB14N1YuIQG18vHKoXLgISh6jERYNVcsoQtXK1B+krILdo0OnlK4ZeXLzoUeg+pRYvfvS9yR9OhkMSDgpC73ZR+uz1pk0rXt+0ST/LDDJF3Z4czTAgQFEoSZMbkloERURrzb8cTH2v/5B7Q9u3fzWqR9zMCj17znfc222BIzY20dG1q5Tzg/v3nxc8oN/cKj27z6nRressG12l7DarRu/eM2t06zbrhri4mRF9+84O7t59TnBCwpzg0U/P9WD03A6jR8/v9cwzXzsGD54b2q/PjMiEhGmVBg5Z8OWWLZmFXCR5NGnYoUNXFRwebOKWTTpvfKjAJWwA5yJpLAzsNVtU42Qxzp7asfX5f/YOGdzrw2Eff/zLuI0bs9bv3JldHDbu2pU1as6cY7e/8M/UTR9Ofcq4mnuOYDHXUJQrRkEX6LdAhdGzjyG00u7Dh7dl7NgBGz6+XXKvHt1iVUh4VakxsxTE7CntSoDMwMkfhLuAIyvr+xf+9ernjoceWujo1etr7t490RHXZZEDP7FyCB0fPx/0PJkrKR39+s21kRA/xxEvSJhj13v2nOPo0sWDuLi5Ilu9W7fZkX37TwvpP2BKEMox8+cf9ndH9rp/vUS6cqtW9VVEZF0HdquBGLHmPDraUxSXG1idAo0J17mXM08lJb31D0wcZK+hhdbfl8qs1XHgwOsjb2sYy3iJMAlBYXEyoyzGkjisRQYxaXsBKTKvXL3imr/o1WaffroXKhoodXp/w4b95Haf99kyFOMOE2ha0Oa1bI8lHpF0riv32NqMRHxlyPE22UV8zZohVW67vT0bTgcz27xSZ4hN4dJHTqRNWbPmUqn1yi4oY+VDAe1AI1BAyK9iDB3cv48ynKEygHl832mYx8gnpMmQrhWmHCeLOnns24mzZn2XL/HnUx06tYvm0PA68oIgJxdRycMiL3iYP5yYbnIfO7H5n1/NXvl7Inm2a6+7KCSsCgyRExvXIUavYUjGU3y0QMjBYFy6cDxt1Sr5YYGMcp7m2H6D6lG16s18a5KZiZnz2q9FaHaSdrkuLElJToNcAbuo/yGp5BnwcwM/2gp33lSrOxOGBO5aODHkFo1NTv6X7Oa8OgbQMhS5MCaW26Vyf/p509s7dtjfqvJk/lyCb7/zrs7EpsmMiOBvQHcQg6wbe9CwiCR2rS3t3rEn5Y31688G1AvcYDTscE93Mh3BIiLjqEwmZXcgnOIhxtGYMwAAEABJREFUp6vnkVSROpv9w+ysrCIvPhU6xXS2QpzlNV6SmOF48aaKcO25w3uicfncr3vWr/6liMAfxChhCAp6MSAmppEOLl9LTguCpkk4BYlBSuACsi/mfFrjWYUtRaywz11XL25blpoKIdSQ/wXSOwMGVI2ofUMX8c9ixGMj3//CLsrpz4gZX2iQW8Ru96Xvvl2zBnLYqsjLkCbFxEQ6rq/WUpsYQoPIlFHB7TmQCU0K/7B5ZHcQvh24cty/fLN67po1a9z+OvJz8+tuvinGMEzma200fyUvrbHhlKWtC99/N/v5lSvz3pK9zX9YgeEodV9Gow7t4gyHM9g0DDkrocjAtZOMtQV5N2ZUZWfv27xn/65ra/yxrY0b3dpU43ss4SZQcjRYe96JZjLwXZOIs8/9+OmmbTvpd1z1Wreuz+Ui62ssccVMFhxgRhbQFqNXAphMLCDKuXTsq/TU9VTouueRoTcHVakcrWCXbFCpLlmUAnZfPbt947fLoaSAPyWVemG+17p1pYoNb++kjWuOXJEgMH2En9CS3KuMi+7M5NzcAg/pRRT+QIa8jUe3bRXHziCnxkgYMtkl9C8zxZBRWB7acuvcH3Yumr5mTZHvohApKXFMt05xFBZWkcWWwD6tNSgq9pJ+SRYaCANvzpSVue38t7tOUcGLh3fuGMehYZUYL3Eax3HB5sA1ZibDYOKrF3YtS0vbT3/ihekoXe9dYmNvNcLK30LEJBczEzMLeU3Ic5iFZzcLJybXqHzz01273v5ojx5h8gvFAjy3lhMMio2NzEcz0M0iH+3YsbxgUDPUfYhtFinyAp/+35s3D5XbFxwp2SEI+VKLLl2qhNW/pbXShtzJEQ/ZdwKtUUrmE8wr2V40cmhakGHLdTlxbXqRE4tKccU3aOAMrXNzO80O3H40TkCCbZaOoQ3jyH1JTjEPiBRElDS4Xa6LGzclvb9vX65UfYitWzcoqEmzNuRwODDkiCnwFHtsevoSWmwoS1kXD+1PfSsj46LU/ywE9rqgR1yrVZt2+PJQjpkRrAcFRYqvSQcOjCZ+SEFWZGSduH88uf7DeTN//WDJ4j2Tk5J++WzZsr2fpabunTF33p4Z8+bt+Wre/L1fzVux96v5y/d+tChxz0cLE/d8tSJ974wV6XtmrAS+Tt/zWXrq3s+Wp/z8QfLiPZ8tS941ISVp69zjhxZd2bDqpXmPDWsgJ2Hx3hTkPnBv3+YqomJdQ35Zw16SihAZIUSACwr7avbzHeSw2SjzzO6UdSt3+5rKUrbr1KkOlavQhAn/sIJknAyxLavez5BvwXhYCi/vGlBEFy8eT16evgJ8z8oCISn6tttqGJWq3S0vUQwfJRbh+0NsCoTHzLDnMeHlKXf5apGHv5rX7/jMOfH7Pp3a/8BHnw4QHPz444EHP/lw0G9Tpgw++OGHg+y68D78BLyPBh/6yIMjH3w45MjkyUOPTJly/5EpH9+/f/KMoQc+++L+i8kLB+x85pmG0m9JkPEoSYbimzcPcTao310xjpYSpQsKKJwDyjCJ2SAHOZiMkAh3cHh1CouoocLDqwt0RER1HRFeXaOuw8Oq6bDwajo0ohoJwiJQL1eNw8pVp1AgBHKh4dVVCPRDw2vosIgbVLnyt1Ol67o77m7+Uu/x45MXLkt5GSdSBF374pp339GWcB9n2TiaCOnaGmjFsiBiRYxb6ZWdu1Nmrd9Z+MM2leZq365pL3Y4Q6VXNxajbRcO4HWKlNeAd6F4a0RMhH4tnK6K1KmsnV+u+7bIbfzZIUO6aYwvJMjNbtJ4+SS/S/vdCZjFIhFz/uJkw3CWv7HO6OsTes+oGt97Zu1hQ2bc+OCwL2o99MAXtYY9OL3WsIenXf/II1NrPfzItFoPPjzdxsMPTav5yINTaz0kGDbt+scenHr9o498DrnPrn/kgc9qPZ7wec2hgz4Latf580pt2/6NSnGVamFWv+66SioirIE2cNeBUf/gUA2YbDkMhF1i8GUYBFimRAYTIWGkUWJG0C603PoJXmEdkz80eNJOzMREENF2ycxkiC2HiWUf4jDDomqXb9Nm9NT3330OizOIAlwfdOgQFVz3ls6GIZuFCGZg3u6EAl3anmRFFp7b8IKQu2nN6nTI+tYRyNKlHtHRYTc3vDNOi99k2P88mhKTQYyKxrihKJC0nKj4EqKsXPeprRsXp+7bV+B5PaZ27eCQRg1jDTYdGnKmcpCscrHlg88gs/TiqxHG0LArhgF/DKx9g5zsMJxk4qOmg5wktMA0wfPy0aYhJzLaNJweoG/T4dAO00EOwwGew1SwBJ9Mw8yZmbZ4A5Xi8nhTguCAdu1uZ8MMJZwsIsrMUpQIZrYHOb8TTYQKkq1roNUEwygEBp8KoSjPgIRBhJwYG4aJhIQpohBncHh0k0ceaN++PgW4buvWtQ2HR9zEomvAL1tOjNhEsRnOFRLI0cpnz+5OSlv1u27jXe+6q55ZueptZCByNsiEVelQ1p0nonw/mAvSLAFeunxy63fbVlOha3CrVjUdVSo19phjFAYxcyEpKsLzX7Q2jT4MgABTvGMTlAE9AXtLHy11gQm+D2iDhmcjGWR/vsCbJZ8/u27VsjXHqBQXtEqWCqtW5UZyODF9jM65ZAU/CWa2dZjzS2lmZinKBGYuYosZPGIMAw4HRGMxSnIQfppSuVlM81ZU/GU0ad2qHZlmkK+ZmYmZfdUAJZNS6ERb6tKOXYve+f7733Mb5wH3dulEIREVGYvS1xEzEzP7qjbN7Kkzs10nQqkVuU+e3LlwYcoRKnS16d0tjsNDq3p+LY5Jy4ns1WWGrheF1Owqc347cz5tN14jY+ZrtEoTk8IGJO1yZW/+dWHhU14kigNGuTh2QR4OymA5U+zbbMGm31VjLimY32XWqwTbOHq04TCCa9aoByYYyP3SuObNK4TdWLuV9lsYfs0BSY2FQZhsI/fq+XWr1hd58Qio6NfwaHR0aORdTe61TKf8TZlfyzVJuxFh4Zkx1zq47btl0w8eLHAbl19xq3Nnw67acDoIfopxJlx2hvJPSMzoXBMefdB5zuWTP6bO3ASqVKlUC9O8dOmYacmPbwh3MfRUKtN/sJBi+44hP5ViuMikMIkaFBW5OvXu3dyIrFCfZOCKtAZmiDFLW6ROn9i7cmP6nsCSgVsS7rqrjlmxQiNNmLTAYsW34LTUl8+f/Hj23K8hoIG8dN+NjWuYVavfzYaDZFI91guI5MkWJpg90sKXW7mUAqELQ/ilhehiwRApi/TRY5tWb95c5FfzAtmSGAK15fHXr12/ha/mZhuWRdKRdCjIEwhAiIwPAUTy2KWVy1MoTPgGF2Os8ZmESGmdffYsxArPDtdtclc7djhCsXLRXPokhvA0S5e/371owpptWaXXzJPkJrEdumiHE18MYE12UF7TtQkZH8LZoE6d3vLN8eOF38apb78ucSoorKLS3imVcYBJ9IL82klsC0SKGYpCAMz5NKplTszQhzuGUtbB735IHrdtW6l/RwJqJfd3etq0oznbtk9kt+uKltWvtaxP0gql0DhFNGFX2FAwiAWME4sgpQASGrtdSo3SB7sNuqTc0JGaBUkBaNuuxz7ZNmSIBRAtLmEM7FsdZA0ZEO22ftj9y47CoqOaNSsXVb9uW/jAuOxmX2lXfJm3K4mG4IuA0QfGIGfpqlXJELObUJY6Na9ZMyQ0+s5uxE48REDd20dRA4g7j+knp5T7wg8/pW8r9PfwDRo0CKrTpGF3MkyTZUbhJ7RggTEaKAIk6UVjDpXMG3yxMA0KPzlQsgGED9gG0CYlpo7weE22DmQ0ZG1ATstvjgnAt/VRCk9WAib1fMY3GRvhhlhCUXKSMEqUGkekej458t1Ta9c+qy+eP6yUCz+M0+TGAIjDbK8IDAK6VXBOywsCgiTcXqVN4+aicevSkNN2b5BFHXERCQ8z7gZI5BQENKQYTVKimp/Az68UpKTJHjlFjP711dzTrq0bdxYUIhre+95mZoXKt7KJDkgTs5QFpbS3Kt3bAyt1RST+8vnL+9asX79PWGXF0O5dbjYrX9eYyHO7DaiPONCdDABpbFwNRxTBz8sXjyWlLS/y63VP/e1vNzgqVW1okCkjKJIoIY8OPDmIYhLMEiPTKsdFp0/+aGRlb+esk9/xmRPf8skTW/TJE5vVyWNbyIOt4G+lrBPfUubxbZx1fBv5kHnyW8o8hfbTWzj79GbOOrOJs89sobOZ33J21hY6fGDenLS0Ut/GxVVDstIgfceOSwO6dvt4+7h/97y87pvXnWeOrjNyLh7V1tWzOjfnAuXkXmCXdYHd1gVyoe6SOnD1ynnOyTlPuVcvUA7o3NwLlJt7ngGHy3VO5+ScQ/0cu3LOcq7rnOlSl8hSSmMXMvuGVUrBNdz1riaZHJlIzszcOXffb8cLxWZUbxbdkRyOcDemT1REVlBQTlrspYCp9rTIHZK1W13Z89OST8pwS/Joe/J2MTEdtNNZwcKm0PbR5uEXzSVWD5exxBTGwcICUidPfP/19u2F38a5X1yXVhwSWoUQk4Icea98K16GXyER2lXsPDPr7I41L7zYfcLjD8V+/Nj9XT8Y9nDclCeeiPvoiSe6ffTEqLgpQ2zETnzksbiJDz0e+8ETDwOPAA/HTnzq8a4Tn/pH7JQBI2KnPD48bsqjw7u988TIblMefTxu4gMPxb7zwLBuz97/4N9L+zZu+4TsGjON1kJpDZG76TvvfF++fedx/aNbdHm6/33Ri3r1bfxj3/jG2/r2bbztn70bb/+8T+OtL77UaEv/no129ItvtDMhofHOfv0a/9gnHnL97vyxD+T79LlzZ3x84519+975w8CBjX9IGNj4l4S+jX8eOLDRxomvN+GTRxYwKZylyvag6MKx2YUyi6CAU4ZJk8t1eOPm+YUX0NgOHSpWaHBbJ83MChNOmEgKdHlnFd/IYA9mCRquq+dPrlouv7anA6kF4o+qWze4XpsW/bTpNGTtcCn6FlsacvZJrVzu3J0/rE4qtCkewEf18m1a9cNza5DIEuTJvmTsFGrarhWXiV1IKH0qa12Hzz//7dmFC08NX5h+6snU1NMjFy7MzMNK0MAzSUlnBE/OTz3twzOzwZs9+8xItPvk/zF/fpbQIiuYtHFjqZ8tfX6WaWH6lFCq+UeOXHl3ycqTfVJSDjVMTt5/t+ANlCOS9zd7++0DzZLSDzRKSsqDyPjD13bnokUHBQ0SUw41SEw81OL5cT8f2rkzEX24PQsSQ4fhRT0vCV/gY9g0lpoCQ8syunLhzJq1a9fYVWS+NLh/n6ZcIaoB47RygMlAccnD9+TSbuF2SvgRJF+4+MvSjWt+Fl5Z0TI6+kYqX/E2jQ0hg85YL9gfxZpBE/jIkSQc2Wp85dLZVavXF/mN8p6NG1enqKrRZJi2OTuDNpH4D03YkPEpFmJcWVcOrV0nm03RX+iSMfoLuWO7wjWvv6ERKY8aZ7YAABAASURBVMtkDK5MoM0tlOVPgKdBsQFpwI2fDx87ujN5/frfPC15Odducve9ygwLxiOo59NSXlNhAhMKa5Jk7hhOsNuts3fvSXkydV2RP2YrrF1MnRt179SZHaHlDZaoPCdwMXJeljyQMBE2m0gaWDJmdub2JZs3F3m2rd+rWxsKCalC8FEA8+S5oI9F6aGLz+ULA5/P2peSmLiteIk/j2v8eV0X3/PH0T1CuVL5Jmg1qNDY+saZGQ0QKJA0FhPuTayUdfjHHV/P3727wK+DPdOwYVjI9dVba5xYCqtNThBCB8xMzEwFLukIQCKNCWdGu1aXd2zasgxyCihTurd+/Yi6LZr10IbDsBVhjgzJ7FrADCGhTWETuVXW/l9X4dHEBUZeiiFy1GrWoq/bYeKJQ6LywBbQyGGAiUF4EnM+TXieMPEKm3vst61rV66Uz2oeob9IbvxF/Mhzo06Xv9XjqKoNteEkTXAPJ6FvbP2GNU/eJtAgLwgGngOV+9zp3bMXr7T5flmP3vHNdGSFOgYWmhNvMmya5LNLhS4Fe0iERY4WjRI3/qs5h3euWfO7fjbep3XrOka16xor+dEcvrEa9ls3YoP1QEkhFhJI/K4rJzJSUxcVlm2bkFA1tHqNxliVCIWJNWxiMdpyjBxVNBAz2wAnL7FQlvvi8c0ZC+YTvhdJ/S8Ecf0v5A5xu7jOcSoouBKzPXRFBrQ4ZxmTYWI1sbaIz134ccnBgycKyRktOraK1Q5HiMV4CgUsQllIyFf19IyaEHI7xcc6derMCrwU/K5fnu3YsnUrHRQcZcgiIzGKxQ7zgZJIGIjJllKaKDNr65p1Wwr83bXotm16x90UHITbuEyjaBExe0oKcDF723Fi0qWLe79YuX5LANE/lS0R/akO+Hc+BLdbs94t3U1y4DjzbymZttcPKdfl7d+n4JZ31V9D3sbNm2q1ZcPE4xom2pP8RQrQjJNKYfFqTCJESetcl/vAgeUQUkCZEh4hwqt2bjuMDKeD8KhBxEiM000sU+BLM9pwUmvlvnDg4Gq82RaIKR4f1Zt37txPOx3BWmxCmll0QJQiaba0O/O3Tbvmz/89v4hSih5KFLmmwF9pYRojH7w/jiOiGnNZB5px08NS1rmXz3ydlpaOiAssoIGxne/SFSvcamiTTNiGOJkaUgGT50aKQxUSIojjxTTK/MlDngGfe/65QUbVyncyO+yeGTlhATEsB06K5NlWeiZ3TvZvq9ashaxdRWmn7k2aVAmucUMLMgw2iPHPZpc6Y61dv27bsfqveBuXIAzJ/GC+HhtbZdbDD1f78r77qiZ26FBpyt/+VjGmceMKhdEK/G6tWlWc17x5VOLQoZVmDRhQeV58fBV/fDlkSFWxJUiEPf+68OY98ED1zx98sIb8OcSFGdMfi3546CQV5AyVX13z86lEUl5kLHlMyszetWHT9gOFFPjW9m26a0dwhEyfYU+vJnn34EKC+VW2J5pxaskHa204nLpWnUEPxXeJggwD10ocH0/m4507V12ZlDgiqkfcf5QZgv0ANXSOHLrI2XYEdIAEEUMpoqzM7z7esuWnwlKN69W7i8LL1yDS8FVQWCJw3R6vK67soBxjby/MbZfbb4+Kb94F8zi20qxHH608b9iwKl8Oua+qrAGZs3mjhlWZFR1d2YMBdjm26dBKXZrfHmWvA6yFwutjTKvhFec99PeoWU8/jXXRsbz3b7ICO1WopcDCXD1lUo8xs6avT3jrrY2Dpn26oeeCORseW79qw6pvVmxYviotY+UKL1Ytz1i7fm1GUurSjD5pqRk9338/o/+HUzL6fPphRp9PgE8/3gB646APJm3o//YbGQlvj8/oNfXzDYPee3dD//FvZdh4442MPhPGb7h/wpsb+r42fl14fP93VXD56wkeyUsMM2amkLPFVTUOM4Ghclynv/1+EW7jBU42eTwwrq/aio0gHBKwALNYb5hO0H5JbAh8LIjJnBPBD02GEXxj7cGffvJl6oXvt793cGPGawcz1v37YEbGvw+uW/uqYH/G+teOf7/tTX3owKRZb/4y+/3Z09fpLl3e1sHlokwJCj1aeJAgXNoLFMUm8UMeTchtuS/+tCf9/dTUAl8Y5CSu2ymmpzacQUr8E2GUxRorhsnMZISEVrqxd99FC1av2JzyzepNc1Pmbez17tgNCW+9mdFn4njM1acbBk0F3p+U0eff4zckrFy+0YPJGxNWLd/42vJ3NqWkrNq09psVm5asXbFx1ap0wYaVK5ZtXLl82cbXl7664b6JL2T0f3FsRt9Pvkxv/9CQ26gMl+GTlRXdOqZzZx0ZVY8jI+pwuaibqVylehQRdasOr3ibUb5yA6oAVKyEMqoBlSt/G4VH3maER95qRJSrb5QrD72oW7g8EFmhLkdG3Sw27DKy/M1UvsLN7I8otFeoVIfLV7qRKkZFaWeI02E6SGPQmO1l4XMtr9SEf3jBkcPRnlwsSsKHbyI3GRezfp3x2dQFEJYmFJ40+J57buDwyJvdjOXuYDzbIWTQnlXnkZGF4KHAFZtkYikxIQMFmk3STqdDlY9qGtKw0cgb7rnn+Zr3NH+xVvN7XqzVstULtVq0fKEWeFUbNh6ta9zwlKPWTfFGhar1yBHiZOkLHjHJP8Puhr25wrMserQTQvOWCiVjTeIecPHM3i/mzJQfNsCCrWRn/bt3rxZyS/2OBhx0gBNguNASOLFpOLhc+E26fMV6umLFW6h8uXoaoEh7Hj3zJ3MYGSV0XSpXwQZLGeGly1fBfFepxxWq1FcVqtyqKla5jaOq3WpEVb2VIyreaoRH3WphDVmO4Mgdew4cDexN0RbPSIF/y70dKuuKUffIDiTZ2Rg9CZiZidkLgyHJJP8MNoiZiYTnBTPbPGaGnF9CnZntNj8uMfQMBt8AvLc2kwyIMFA0MTFpNkgbMk+KcvHpRclpYblzr+z6ec7olJQivw5m3lz7DnaERjigy16TDFoD3mrggglSBiAlwTOTTPTPoNiAH/BdNpIGzTafiUzwDSYiJkMAmgUsy0j4ZF8sbfJ5B6ViIvlaYCEeF7vxjqQh43LnbNj8xajPZhxCpUCq0bx5Yx0eVl3UGfpkgwJesvEEPgFmtknJxUcTz7/CYJJ+QUmDD6jayVvX3lJ4zFIRimwP7JpkgMjhkR4NWhvHTiw/s379eSrDZfhk+8XedzeXL1fXQheaTB87r2RmYs5HXkMAgpnzWmRQfGDmPDt5AiCYPXyQBZLo+RgybOIf4YRknUMGTjfDTaQzM79767XXPoacAgokZTqchB/XGZh9Q+HElcGHIU0MCnXYEAXm4vv3b2NmqdoQimHDriBjwD8xMzGzP6soDW893SvEYpEJ/wzMqMZJyidPbpzx/ofToQQp5PnJ6B7XqZdymEFubAjFOM2xBXR+e6koZo9vzPklM9s+M5eu9O/I/ukYGAxo6Hs2DSEm14XVyWnzy/qS5VuYfGtMi85GUFC4U8uE+djopVBi5kKc/GphipmLBFpYpjR1WZwCfLchz9s0EyknOdy49bvdJ3ctTHz9XylrThZrKzfnHG6ZFoCFSDiZMM9YDbAAcU8OIi8xF+XlNYKQVoEYk9IgxrJgYs4HeS/bZy9dXCGTRzBkwCW2sMCUiUcN7KMrV47t/mrOK8PT04vcAcbFxETpWjU6ajbRI0Ge0D9KKvvFzGVXCqihiRGLNCMcm2JsNL568dDP65LL/IMJQwyN6datQlCN2u1xshhyChG6IO/F/L903mu0DAVzwf4leDk13YZJFrkvuFaufv2pEf+XApMaKJK2bP52J125kqkw+7JQNGLTsGloAgWAZi7YB5XiYg6sw8zE7EEgU+ieFG7dEo/4k2sSuU1MqfvqpWNpy17699ixq4vT7demxZ0UHn4dY1WLOGOTkRgrTtjLY873RcbAy/6fFMz5tm2DPl/w0y1yu3TuqVMrvs62ztltZcjshflgl47tKCzyFpa9JzNGnouZPUSA3D9IoQUiKqXAR0v530LsyacbCwHjlqeNS9lH96ck/iOkR4/JazCngey/uHjx0ZyDhxK1ynWzRjyAwkxqeTYNpFQCX3wRlCBWQrMmhh+Etai0nJsubZw/dejUvK8frNW3//Tibn3yglqnY4f78FIVRIiDoSea2kME7E98FYgAM8ZAiP85YBc++cwy5oks69LmRSlfr1lT8L9G55O5Vmmg0ajZsmVrrQ2nVogUA8UYMmYMG3ajLyDI2Ukm1QfxAxqk8c9uLJQV1pVm4flgq3kMYHxBoD9bBg1aZgwlGnAHh1M4H0nlkum6eoWOH03bNuH9gfV7JUyDvAVcK6n1b054h86c3qqVfUcXk7BpkcZ3QtsXaKN3O9fo0+bBl0AlhoeYPeMjYyE6UC6QfLrSmbRLBII8Pn4KxLh1a7hk5Fy6wof2ph4Y91rv64YMkT80E9EC9qQS27NnjaDbGnQyGC/77LMs1gEsBF0sNEHUhmjYQGxSapRlAYZG1MQVG3JQaFACZS8GoQjPy16m6/K+hevWlfk2Dm0yujRvXiHkpjpt3YZmhZ2n0YEMNsnf4WjMOcCEcUJJAFsW+YPkD0XAI0wyY2Aw23juEfl8aLElgD75QeMlRqDwyUeDrwQipxCgqGvGvIFpWVf40uVD7l/3L1j1+us9e/bq06fpuHHfIAALKDF1njXrl2mjRidc3bfrC4fr8nGtlYu1oUn6ccsChRn4rrUmG4hXYyNou1SkbRoyKAm+SszacqFfC7FCHzxL/gcbcFUJEIPEQ5BHAFKQxkKU/jT6IGVhqK2rdOniIevQgSVrX3+td9+WXeJveWey/P+HEDlMF5PadOwYzRGR12v0x+QiZbhIs/L4IH0VA/KOsZYSekr8FF3QcAoLzSo1pF8bEh/AgLZySbtdxJh/hdhzxAeZPsaN/NDRtHcWLSrT27gvbKPPHXdUpovnD5injy0zTh5JptPHU3C6pOpT2al0OjuFTp9N1qfOLtVnPKAzZ5OBFMo8mwos8wCymVmp+kx2qj6NUnRPZaWSrxT+mbNogxxK2EwBkulk9lI6kZ3MJzNBZ6bwieylfOz04qu79y64+uPuuTk/7vzEtW3bS6mv/+feXrHdWrQcNHRAx1deX560bdtlXwClLR+bP/9wm6EPPfbyQ4+2zU5Oevzy9h/evbpzx4wru3bO5yO/LabfDiXTkaOpfPi3ZXz4+DI+cjKVj55cZuPIqTQG6MipdDp6ejkdO72Cjp1ZQcdRnji9gk9kLTdOZKXz8cw0Pp6VhrognY5mpkMmjY6dTDWOHlvq2r1rQe6OHdNc27/957dv/efegbGxLe4ZMKBvu1ffWJZ07FhJMXG5y5fD6Xj2dj6WtcY4nrXKOJG9ho9lrqYjZ1bw0cxl4CcDGMMsKQUpdCKrAPhEtoxzMp/IkjHPB+bZnpPTZ2VuUijzfHIeskD7I/PcUso8l0THsxa7fjq8yPXzgYWO8MXqAAAAJUlEQVSuXXsS3fv3Lww6dWIpnzix1Dp8+LOkGTM/x/wooMzp/wEAAP//c40MEgAAAAZJREFUAwDQl5U0Rej2aAAAAABJRU5ErkJggg=='))
                msg_image.add_header('Content-ID', '<logo_soe>')
                message.attach(msg_image)

            # Attachments
            for attachment in attachments:
                part = MIMEBase('application', 'octet-stream')

                if 'path' in attachment:
                    with open(attachment['path'], 'rb') as file:
                        payload = file.read()
                elif 'content' in attachment:
                    payload = attachment['content']
                else:
                    continue

                part.set_payload(payload)
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
    Envío de correo por ssl
    :param smtp_server: servidor de correo
    :param port: puerto del servidor de correo
    :param sender_email: usuario del servidor de correo
    :param password_email: contraseña del usuario del servidor de correo
    :param to: destinatarios del correo
    :param message: cuerpo del correo
    '''

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(user_email, password_email)
        server.sendmail(user_email, to, message.as_string())


def send_mail_by_tls(smtp_server, port, user_email, password_email,
                     to, message):
    '''
    Envío de correo por tls
    :param smtp_server: servidor de correo
    :param port: puerto del servidor de correo
    :param sender_email: usuario del servidor de correo
    :param password_email: contraseña del usuario del servidor de correo
    :param to: destinatarios del correo
    :param message: cuerpo del correo
    '''

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(user_email, password_email)
        server.sendmail(user_email, to, message.as_string())


def get_file_size(file: FileStorage):
    '''Get file size'''

    file.seek(0, os.SEEK_END)
    file_size_bytes = file.tell()
    file.seek(0, os.SEEK_SET)
    return file_size_bytes


def process_file(file: FileStorage):
    '''Get mimetype, extension and filename from file'''

    mimetype = file.mimetype
    size = get_file_size(file)
    filename = secure_filename(file.filename)
    extension: str = os.path.splitext(filename)[1]
    extension = extension.lower()
    return mimetype, extension, filename, size


def format_file_size(bytes_size):
    '''Format File Size'''

    if not bytes_size or bytes_size <= 0:
        return '0 Bytes'

    k = 1024
    decimals = 2
    sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
    i = math.floor(math.log(bytes_size) / math.log(k))
    i = min(i, len(sizes) - 1)
    valor = round(bytes_size / (k ** i), decimals)
    if valor == int(valor):
        valor = int(valor)

    return f"{valor} {sizes[i]}"


def is_allowed_extension(filename: str, allowed_extensions: set[str]):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def validate_files_size(files_list: list[FileStorage], max_size_mb: int = 50):
    '''Validate file size'''

    invalids = []
    for file_obj in files_list:
        max_size_bytes = max_size_mb * 1024 * 1024
        file_obj.seek(0, 2)
        file_size = file_obj.tell()
        file_obj.seek(0)
        if file_size > max_size_bytes:
            invalids.append(file_obj.filename)
    return invalids


def validate_file_types(allowed_extensions: set[str], allowed_mimetypes: set[str], files_list: list[FileStorage]) -> list:
    '''Validate files types'''

    invalids = []
    for file in files_list:
        if not file or not file.filename:
            invalids.append(gettext("Archivo desconocido/sin nombre"))
            continue

        extension_valida = is_allowed_extension(
            file.filename, allowed_extensions)
        mimetype_valido = file.mimetype in allowed_mimetypes
        header_bytes = file.read(2048)
        file.seek(0)
        real_file_type = filetype.guess(header_bytes)

        if real_file_type is None or not extension_valida or not mimetype_valido or real_file_type.mime not in allowed_mimetypes:
            invalids.append(file.filename)

    return invalids
